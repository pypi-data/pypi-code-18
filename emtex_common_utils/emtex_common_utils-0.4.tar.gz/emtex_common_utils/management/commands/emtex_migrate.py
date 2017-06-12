from optparse import make_option
from emtex_common_utils.utils import Styles
from emtex_common_utils.utils import cprint


import os
from django.core.management.base import BaseCommand

from emtex_common_utils.sqlalchemy_services import run_db_query


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--for_date',
            action='store',
            dest='for_date',
            default='',
            help='Specify date for which you want to run database migrations'),
        make_option(
            '--after_date',
            action='store',
            dest='after_date',
            default='',
            help='Specify date after which you want to run database migrations'),
    )

    def handle(self, *argsv, **options):
        _for_date = options.get('for_date', None)
        _after_date = options.get('after_date', None)
        if not any((_for_date, _after_date)):
            print("""
                Rule:
                    ** Please follow the following rules to write migration SQL file
                        Create a folder under /emtex/docs/migrations/  with the date on which this
                         release is going to happen. And then put the .sql file into this folder

                    Example:
                        /emtex/docs/migrations/2017-05-05/some_example.sql

                    Then run it like this:
                        python manage.py emtex_migrate --for_date="2017-05-05"

                Usage:
                    1: To run database migrations for a particular date:
                        python manage.py emtex_migrate --for_date="YYYY-MM-DD"
                    2: To run database migrations after a particular date:
                        python manage.py emtex_migrate --after_date="YYYY-MM-DD"
            """)

            return
        path = os.getcwd() + "/docs/migrations/" + _for_date
        for root, dirs, files in os.walk(path):
            for sql_file in files:
                with open('%s/%s' % (path, sql_file,), 'r') as f:
                    sql = f.read()
                    all_sqls = sql.split(';')
                    for line in all_sqls:
                        if not line:
                            continue
                        sql_query = line.strip()

                        # Skipping comments
                        if any((
                            sql_query.startswith('#'),
                            sql_query.startswith('/*'),
                            sql_query.startswith('--'),
                            sql_query.startswith(';'),
                            not sql_query,
                        )):
                            continue

                        cprint("Running Query", Styles.f_y_b)
                        print('\t%s;' % sql_query)

                        # Warning for dangerous commands like update, drop, truncate
                        if any((
                            sql_query.startswith('update'),
                            sql_query.startswith('drop'),
                            sql_query.startswith('truncate'),
                        )):
                            _input = raw_input("\t%sAre you sure you want to run this query (y/n)? " % Styles.f_blue)
                            if _input != 'y':
                                cprint('\tTerminated', Styles.b_c_f_b_r_0)
                                continue

                        try:
                            run_db_query(sql_query)
                            cprint('\tSuccess', Styles.b_y_f_b_r_0)
                        except Exception as e:
                            cprint('\tError: %s' % e.message, Styles.b_r_f_b_r_0)
