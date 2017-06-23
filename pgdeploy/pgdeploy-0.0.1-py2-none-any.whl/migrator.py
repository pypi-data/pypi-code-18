# -*- coding: utf-8 -*-
import os
import psycopg2

from pgdeploy.migration import Migration
from pgdeploy.schemas import Schemas
from pgdeploy.exceptions import (
    NoMigrationsFoundException
)


class Migrator(object):

    def __init__(self, migration_dir=None,
                 db_host=None, db_port=5432, db_name=None,
                 db_user=None, db_password=None):
        self._migration_dir = migration_dir
        self._db_args = {
            'dbname': db_name,
            'user': db_user,
            'password': db_password,
            'host': db_host,
            'port': db_port
        }

    def run_migrations(self, target_version=None):
        # Load the migrations for the given migration dir
        migrations = self._load_migrations(self._migration_dir)

        if not migrations:
            raise NoMigrationsFoundException()

        # If the target version is None, then assume we want to migrate forward
        if not target_version:
            target_version = migrations[-1].number

        # Get the current database version
        db_version = self._get_database_version()

        # Filter the migrations down to those > the current version
        migrations = [m for m in migrations if m.number > db_version]

        # Apply each migration
        for migration in migrations:
            self._apply_migration(migration)

    def _load_migrations(self, migration_dir):
        # Get a list of all the files in the directory
        migration_files = [
            os.path.join(migration_dir, f)
            for f in os.listdir(migration_dir)
            if os.path.isfile(os.path.join(migration_dir, f))
        ]

        # Read each one into a migration object
        migrations = [
            Migration.from_file(filename)
            for filename in migration_files
        ]

        # Order them by their migration number
        migrations.sort(key=lambda migration: migration.number)

        return migrations

    def _get_connection(self):
        return psycopg2.connect(**self._db_args)

    def _get_database_version(self):
        with self._get_connection() as pg_conn:
            with pg_conn.cursor() as cursor:
                cursor.execute(Schemas.CREATE_PGDEPLOY_VERSION)

            with pg_conn.cursor() as cursor:
                cursor.execute(Schemas.GET_CURRENT_VERSION)
                (version,) = cursor.fetchone()
                return version or 0

    def _apply_migration(self, migration):
        with self._get_connection() as pg_conn:
            with pg_conn.cursor() as cursor:
                migration.apply(cursor)
                cursor.execute(Schemas.APPLY_VERSION % migration.number)
                pg_conn.commit()
