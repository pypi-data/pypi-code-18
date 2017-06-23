
class Schemas(object):

    PGDEPLOY_TABLE_NAME = 'pgdeploy_version'

    CREATE_PGDEPLOY_VERSION = """
CREATE TABLE IF NOT EXISTS {table_name} (
    migration_version INTEGER UNIQUE,
    applied_at TIMESTAMP WITHOUT TIME ZONE
)
""".format(table_name=PGDEPLOY_TABLE_NAME)

    GET_CURRENT_VERSION = """
SELECT MAX(migration_version) FROM {table_name}
""".format(table_name=PGDEPLOY_TABLE_NAME)

    APPLY_VERSION = """
INSERT INTO {table_name} (migration_version, applied_at)
VALUES (%d, now())""".format(table_name=PGDEPLOY_TABLE_NAME)

    ROLLBACK_VERSION = """
DELETE FROM {table_name} WHERE migration_version = %d
""".format(table_name=PGDEPLOY_TABLE_NAME)
