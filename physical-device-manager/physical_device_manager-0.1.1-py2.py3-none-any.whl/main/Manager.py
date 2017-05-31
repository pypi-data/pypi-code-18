
from sdk.softfire.main import start_manager

from core.manager import PDManager


def start():
    pd_manager = PDManager('/etc/softfire/physical-device-manager.ini')
    start_manager(pd_manager)


if __name__ == '__main__':
    start()
