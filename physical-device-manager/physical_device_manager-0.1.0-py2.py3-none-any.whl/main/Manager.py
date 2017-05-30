from sdk.softfire.main import start_manager

from core.manager import PDManager


def start():
    start_manager(PDManager(), '/etc/softfire/physical-device-manager.ini')


if __name__ == '__main__':
    start()
