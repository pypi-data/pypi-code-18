import asyncio
import sys

from microscopic import loader


def main():
    config_filename = sys.argv[1]
    config = loader.load_config(config_filename)
    context = loader.evaluate_config(config)
    executor = loader.build_executor(context, config)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(executor())


if __name__ == '__main__':
    main()
