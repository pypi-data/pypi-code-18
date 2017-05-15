"""Duke data service command line project management utility."""
import sys
from ddsc.ddsclient import DDSClient


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    client = DDSClient()
    try:
        client.run_command(args)
    except Exception as ex:
        if client.show_error_stack_trace:
            raise
        else:
            sys.stderr.write(str(ex))
            sys.exit(2)


if __name__ == '__main__':
    main()
