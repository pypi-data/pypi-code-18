from os.path import expanduser


DASHBASE_CLI_VERSION = "1.0.0rc5"  # match version in setup.py


class DashbaseService(object):
    TABLE = "table"
    WEB = "web"
    API = "api"
    MONITOR = "monitor"
    AUTH = "auth"


def list_services(monitor=False):
    services = [DashbaseService.TABLE, DashbaseService.WEB, DashbaseService.API, DashbaseService.AUTH]
    if monitor:
        services.append(DashbaseService.MONITOR)
    return services


DASHBASE_EXTENSIONS = "dashbase-extensions"
ZOOKEEPER = "zookeeper"
DASHBASE_MONITOR_CONFIG = "system_config.yml"
DASHBASE_PROCESS_NAME_PREFIX = "dashbase"
DASHBASE_PROCESS_PREFIX = "-Dprocessname=dashbase"
DEFAULT_MIRROR = "https://s3-us-west-1.amazonaws.com/dashbase-builds/dashbase/release"
DEFAULT_ZOOKEEPER_MIRROR = "https://s3-us-west-1.amazonaws.com/dashbase-builds/zookeeper/"
DASHBASE_DEFAULT_HOME = expanduser("~") + "/.dashbase/"
DASHBASE_DEFAULT_CLI_CONFIG = "dashbase-cli.yml"
DASHBASE_DEFAULT_APP_CONFIG = "dashbase.yml"
DASHBASE_REMOTE_CONFIG_PATH = "/tmp/"
DASHBASE_DEFAULT_CONF_DIR = DASHBASE_DEFAULT_HOME + "conf/"

# Connection RETRY for health check
NUM_TRIES = 5
DELAY_IN_SECONDS = 5
RPC_BACK_OFF_FACTOR = 1
