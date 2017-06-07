import logging


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(FORMAT)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    logger.addHandler(sh)

    return logger
