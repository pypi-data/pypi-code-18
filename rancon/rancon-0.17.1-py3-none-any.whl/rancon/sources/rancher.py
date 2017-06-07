""" source definition for rancher source """
import time

import prometheus_client.core
from cattleprod import poke
from dotmap import DotMap

from rancon.service import Service
from rancon.tools import getLogger
from . import SourceBase

class RancherSource(SourceBase):
    """ describes a source for rancher """

    required_opts = ('url',)
    additional_opts = ('accesskey', 'secretkey', 'default_name_scheme')

    def __init__(self, url, accesskey=None, secretkey=None,
                 default_name_scheme='%NAME%'):
        self.log = getLogger(__name__)
        self.log.info("RANCHER INIT: url={}".format(url))
        self.log.info("RANCHER INIT: accesskey={}".format(str(accesskey)))
        self.log.info("RANCHER INIT: secretkey={}".format('<SET>' if secretkey
                                                   else None))
        self.log.info("RANCHER INIT: default_name_scheme={}".format(
            default_name_scheme))
        self.url = url
        self.accesskey = accesskey
        self.secretkey = secretkey
        self.default_name_scheme = default_name_scheme
        self.cache = DotMap()
        self.get_services_summary = prometheus_client.core.Summary('get_services_seconds', 'Number of seconds get_services takes', ())

    def is_rancon(self, service):
        """ Checks if service has a rancon label """
        labels = service.launchConfig.labels
        self.log.debug("EVAL: service '{}' (labels: '{}'".format(
            service.name, ",".join(labels.keys())))
        for label in labels:
            if label == 'rancon' or label.startswith("rancon."):
                self.log.debug("EVAL: found matching service '{}' "
                               "by label '{}'"
                               .format(service.name, label))
                return True
        return False

    def get_services(self, **_):
        start = time.time()
        starting_point = self._poke(self.url)
        routable_services = []

        # get all services with rancon(\..+) labels
        services = [spoint for spoint in starting_point.get_services() if self.is_rancon(spoint)]

        # create service instances
        self.log.debug("EVAL: found {} potential services by tag, "
                       "checking for endpoints"
                       .format(len(services)))

        for service in services:
            endpoints = service.publicEndpoints or []
            labels = service.launchConfig.labels
            for endpoint in endpoints:
                meta = {k.split(".", 1)[1].replace(".", "_"): v
                        for k, v in labels.items()
                        if k.startswith('rancon.')}
                meta['host'] = endpoint['ipAddress']
                meta['port'] = endpoint['port']
                meta['service'] = service.name
                meta['stack'] = self._get_name_for(service.links.environment)
                meta['environment'] = self._get_name_for(service.links.account)
                if 'name' not in meta:
                    meta['name'] = service.name
                svc = Service(source=service, **meta)
                routable_services.append(svc)

        # return service instances
        self.log.info("EVAL: found {} routable services".format(
            len(routable_services)))
        self.get_services_summary.observe(time.time() - start)
        return routable_services

    def _get_name_for(self, url):
        if not self.cache[url]:
            self.cache[url] = self._poke(url).name
        return self.cache[url]

    def _poke(self, url, **kwargs):
        """
        Wrapper around cattleprod.poke() so we never forget the credentials
        if given.
        :param url: The URL to poke
        :param kwargs: Other arguments for the API
        :return: The return value of cattleprod.poke()
        """
        return poke(url,
                    accesskey=self.accesskey, secretkey=self.secretkey,
                    **kwargs)


def get():
    """ returns this modules class """
    return RancherSource
