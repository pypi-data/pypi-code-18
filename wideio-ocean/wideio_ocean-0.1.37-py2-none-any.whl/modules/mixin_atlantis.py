import logging
import os
import re


class MixIn(object):
    """
    Allow to call ocean in ocean to create virtual cluster and tests environments.
    """

    @classmethod
    def clean_atlantis(cls, srv=None, *options):
        """
        Remove all the images and containers associated with an atlantis session.

        :param srv: service (unused)
        :param options:
        :return:
        """
        conts = cls._ocean._docker_ps()
        for i in conts:
            if re.match("atl", i[0]):
                logging.info("removing container %d" % (i,))
                os.system("docker rm -f %s" % (i[0],))

        images = cls._ocean._docker_images()
        for i in list(images.keys()):
            if re.match("atl", i) and i != "atlantis":
                logging.info("removing container image %d" % (i,))
                os.system("docker rmi %s" % (i,))
        for i in conts:
            if re.match("glci", i[0]):
                logging.info("removing container %d" % (i[0],))
                os.system("docker rm -f %s" % (i[0],))

        images = cls._ocean._docker_images()
        for i in list(images.keys()):
            if re.match("glci", i):
                logging.info("removing container image% d" % (i,))
                os.system("docker rmi %s" % (i,))
