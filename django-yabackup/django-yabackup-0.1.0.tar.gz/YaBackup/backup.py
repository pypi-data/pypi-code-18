# -*- coding: utf-8 -*-
import os
import zipfile
import datetime
import logging
from .models import Backup
from django.conf import settings
from six.moves import configparser
from YaDiskClient.YaDiskClient import YaDisk
from django.db import connection


class ZipUtilities(object):
    def zip(self, path, zip_file):
        if os.path.isfile(path):
            zip_file.write(path)
            print('File added: ' + str(path))
        else:
            self.add_folder_to_zip(zip_file, path)

    def add_folder_to_zip(self, zip_file, path):
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                print('File added: ' + str(full_path))
                zip_file.write(full_path)
            elif os.path.isdir(full_path):
                print('Entering folder: ' + str(full_path))
                self.add_folder_to_zip(zip_file, full_path)


class DatabaseUtilities(object):

    def parse_mysql_cnf(self, dbinfo):
        """
        Attempt to parse mysql database config file for connection settings.
        Ideally we would hook into django's code to do this, but read_default_file is handled by the mysql C libs
        so we have to emulate the behaviour
        Settings that are missing will return ''
        returns (user, password, database_name, database_host, database_port)
        """
        read_default_file = dbinfo.get('OPTIONS', {}).get('read_default_file')
        if read_default_file:
            config = configparser.RawConfigParser({
                'user': '',
                'password': '',
                'database': '',
                'host': '',
                'port': '',
                'socket': '',
            })
            config.read(os.path.expanduser(read_default_file))
            try:
                user = config.get('client', 'user')
                password = config.get('client', 'password')
                database_name = config.get('client', 'database')
                database_host = config.get('client', 'host')
                database_port = config.get('client', 'port')
                socket = config.get('client', 'socket')

                if database_host == 'localhost' and socket:
                    # mysql actually uses a socket if host is localhost
                    database_host = socket

                return user, password, database_name, database_host, database_port

            except configparser.NoSectionError:
                pass

        return '', '', '', '', ''

    def dump(self, output_directory, zip_file):
        """
        Create a default database dump and add it to archive
         TODO: add support for PostgreSQL and SqlLight
        """
        engine = connection.vendor
        if engine == 'mysql':
            (user, password, database_name, database_host, database_port) = self.parse_mysql_cnf(settings.DATABASES)
            user = settings.DATABASES.get('USER') or user
            password = settings.DATABASES.get('PASSWORD') or password
            database_name = settings.DATABASES.get('NAME') or database_name
            sql_file_name = "%s.sql" % database_name

            cmd = "%(mysqldump)s -u %(user)s --password=%(password)s %(database)s > %(log_dir)s%(file)s" % {
                'mysqldump': 'mysqldump',
                'user': user,
                'password': password,
                'database': database_name,
                'log_dir': output_directory,
                'file': sql_file_name
            }
            logging.debug("Backing up with command %s " % cmd)
            os.system(cmd)
            print(cmd)

            full_sql_path = os.path.join(output_directory, sql_file_name)

            if os.path.exists(full_sql_path):
                utilities = ZipUtilities()
                utilities.zip(full_sql_path, zip_file)
                os.remove(full_sql_path)


class YaBackup(object):
    """
    Main object to work with backups
    TODO: backup Media folder as a single option    
    """
    DATETIME_FORMAT = settings.YABACKUP_SETTINGS['DATE_TIME_FORMAT']
    disk = YaDisk(settings.YABACKUP_SETTINGS['YADISK_LOGIN'], settings.YABACKUP_SETTINGS['YADISK_PASSWORD'])

    def run_backups(self, queryset=None, manual=False):
        """        
        Main function to run backups (manual or ron based)
        """
        if manual:
            backup_list = queryset
        else:
            backup_list = Backup.objects.all()

        for backup in backup_list:
            # Add a slash to output directory path if it's not there and create this folder
            output_directory = os.path.join(backup.output_directory, '')
            if not os.path.exists(output_directory):
                os.mkdir(output_directory)
                print('Root folder created: ', output_directory)

            backup_date = datetime.datetime.now().strftime(self.DATETIME_FORMAT + '_')
            file_name = output_directory + backup_date + backup.file_name
            paths_list = backup.paths.all()
            zip_file = zipfile.ZipFile(file_name, 'w', compression=zipfile.ZIP_DEFLATED)

            for path in paths_list:
                if os.path.exists(path.path):
                    utilities = ZipUtilities()
                    utilities.zip(path.path, zip_file)
                else:
                    print("File or folder doesn't exist: ", path)

            if backup.mysqldump:
                utilities = DatabaseUtilities()
                utilities.dump(output_directory, zip_file)

            zip_file.close()

            if backup.upload:
                self.disk.upload(file_name, settings.YADISKBACKUPS_SETTINGS['YADISK_BACKUP_ROOT'] + backup_date + backup.file_name)
                print(file_name, ' successfully uploaded')

                if backup.delete_after_upload:
                    os.remove(file_name)
                    print(file_name, ' was removed')

