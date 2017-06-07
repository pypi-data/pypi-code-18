""" Module containing the backend implementation for consul """

import re
import urllib.parse
import time

import requests
import consul
import prometheus_client.core
from dotmap import DotMap

from rancon.tools import tag_replace, getLogger
from . import BackendBase


_URL_DEFAULT = 'http://%HOST%:8500'

PROM_REGISTER_SERVICE_TIME = prometheus_client.core.Summary(
    'rancon_register_service_seconds',
    'Number of seconds register_service takes')


class ConsulBackend(BackendBase):
    """ Implementation of consul backend """

    required_opts = ()
    additional_opts = ('url', 'id_schema', 'cleanup_id')

    def __init__(self,
                 url=_URL_DEFAULT,
                 id_schema='%NAME%_%HOST%_%PORT%',
                 cleanup_id='default'):
        self.log = getLogger(__name__)
        # instance vars
        self.consul_url = url
        self.id_schema = id_schema
        self.cleanup_id = cleanup_id.lower()
        # consul instance cache
        self.consul_inst_cache = {}
        # log output
        self.log.info("CONSUL INIT: url={}".format(url))
        self.log.info("CONSUL INIT: id_schema={}".format(self.id_schema))
        self.log.info("CONSUL INIT: cleanup_id={}".format(self.cleanup_id))
        # internal variables
        self.service_cache = None
        # no consul instance here now, cause we need to allow for dynamic
        # URLs (http://%HOST%:1234)

    def _get_consul_for(self, service) -> consul.Consul:
        # no replacments -> always the same cache_str :)
        consul_url = tag_replace(self.consul_url, service)
        if consul_url not in self.consul_inst_cache:
            # extract host and port separately, just for the constructor call
            # of consul.Consul()
            parsed_url = urllib.parse.urlparse(consul_url)
            port = 8500             # default from consul.Consul
            host = parsed_url.netloc
            if ":" in parsed_url.netloc:            # port specified?
                items = host.split(":")             # extract and use
                host, port = (items[0], int(items[1]))
            # create consul instance and put in cache
            self.consul_inst_cache[consul_url] = \
                consul.Consul(host=host, port=port, scheme=parsed_url.scheme)
            self.log.debug("CREATE consul instance for {}".format(consul_url))
        self.log.debug("GET consul instance for {}".format(consul_url))
        return self.consul_inst_cache[consul_url]

    def _get_managed_services(self, cached=False) -> list:
        """
        Calls consul to build a list of all services managed by this rancon
        instance. Will return a list of dicts, whereas the dicts are in the
        "consul format" (i.e. not the format we use to pass services around
        between front- and backend, but the format that comes out of the
        consul API).
        :param cached: Whether to use the cache or not
        :return: [consul_service_0, ...]
        """
        if len(self.consul_inst_cache) == 0:
            # no services registered, so we don't have any consul instance.
            # if we dont have one, just return (cause we can't connect to
            # anything, right?)
            return []

        if cached and self.service_cache is not None:
            return self.service_cache

        # take any consul instance to get the service list, py3 style
        con = next(iter(self.consul_inst_cache.values()))
        check_tag = self._get_cleanup_tag()

        # one call to consul. returns (INDX, {SVC_NAME:[SVC_TAGS,...], ...})
        # so we want only the dict: {SVC_NAME: SVC_TAGS, ...}
        _tmp = con.catalog.services()[1]
        # ... and from that we constract a list of service names only
        chk_svc_names = [
            svc_name for svc_name, svc_tags in _tmp.items()
            if check_tag in svc_tags
            ]

        # now, get the consul service dict for each service name.
        # catalog.service() returns (INDX, [NODE1, ...]), where NODEx is a dict
        chk_svcs = []
        for svc_name in chk_svc_names:
            chk_svcs += con.catalog.service(svc_name)[1]

        # now we have the consul "service" dicts in a list. let's filter them -
        # again - by check_tag (kinda super kinky, but *in theory* we can have
        # a service which is created by rancon, and an alternative which is
        # not. we only want to remove the one fro rancon, right?
        filtered = filter(
            lambda x: 'ServiceTags' in x and check_tag in x['ServiceTags'],
            chk_svcs
        )

        # now we have a list of consul service dicts of all rancon-managed
        # services. yaay!
        self.service_cache = list(filtered)
        return self.service_cache

    def register(self, service) -> (bool, str):
        """Register the service in consul.
        :return: (BOOL(success), STR(svc_id))
        """
        # lower everything, consul should not have upper/lower case distinction
        svc_id = self._get_service_id(service)
        svc_name = service.name.lower()

        start = time.time()
        catched = None
        try:
            con = self._get_consul_for(service)
            success = con.agent.service.register(
                svc_name,
                svc_id,
                address=service.host, port=int(service.port),
                tags=self._get_tags(service),
            )
        except requests.exceptions.ConnectionError as e:
            success = False
            catched = e

        PROM_REGISTER_SERVICE_TIME.observe(time.time() - start)

        if success:
            self.log.info("REGISTER: "
                          "{} NAME={} ID={} CLEANUP_ID={} CONSUL_URL={}"
                          .format(service, svc_name, svc_id,
                                  self._get_cleanup_tag(),
                                  con.http.base_uri))
        else:
            if catched:
                additional_message = " MESSAGE={}".format(str(catched))
                logger = self.log.error
            else:
                logger = self.log.warn
            logger("REGISTER_FAIL: "
                   "{} NAME={} ID={} CLEANUP_ID={} CONSUL_URL={}{}"
                   .format(service, svc_name, svc_id,
                           self._get_cleanup_tag(),
                           con.http.base_uri,
                           additional_message))
        return success, svc_id

    def cleanup(self, keep_services):
        """
        Starts the cleanup procedure, which is basically get all services
        and remove all which fit the following criteria:
        * have the check_tag of rancon set
        * their id is not in the list of the keep_services parameter
        :param keep_services: A list of service ids [id1, id2, ...]
        :return: None
        """
        managed_services = self._get_managed_services()
        check_tag = self._get_cleanup_tag()

        for chk_svc in managed_services:
            # fields: Service{Port,Tags,ID,Name,Address}
            # The 'Address' field (withOUT 'Service' prefix!) depicts the
            # responsible consul node it seems!! So let's use this for
            # de-registering, maybe??
            if chk_svc['ServiceID'] not in keep_services:
                self.log.warn("CLEANUP: de-registering service id {}/{}:{}"
                              .format(chk_svc['ServiceID'],
                                      chk_svc['ServiceAddress'],
                                      chk_svc['ServicePort']))
                # okay. we convert the *consul* service back to a *service*
                # that we get as input from the "source", originally. now,
                # for consul we don't use the service host to register or
                # unregister, but we have to use the correct consul instance.
                # IF we use a dynamic consul service (i.e. %SOMETHING% in the
                # consul url), most probably the %HOST% is used to determine
                # the consul instance. so we override the host= field in the
                # converted service, thus a dynamic consul url would be
                # replaced using the correct host (the CONSUL host) instead
                # of the SERVICE host. although they should not, the MIGHT
                # differ.
                # STEP 1 - conversion with host= override
                svc_tmp = self._convert_to_service(
                    chk_svc,
                    host=chk_svc['Address'])
                # STEP 2 - get consul instance from service
                consul_inst = self._get_consul_for(svc_tmp)
                # STEP 3 - unregister service
                res = consul_inst.agent.service.deregister(chk_svc['ServiceID'])
                # FINALLY - log
                rs = "" if res else "_FAIL"
                lf = self.log.info if res else self.log.warn
                ls = "UNREGISTER{}: " \
                     "{} ID={} CLEANUP_ID={} CONSUL_URL={}" \
                     .format(rs, svc_tmp.name, svc_tmp.id,
                             check_tag, consul_inst.http.base_uri)
                lf(ls)

    def _get_tags(self, service):
        tag_list_str = service.get('tag', '')
        tag_list = tag_list_str.split(",") if tag_list_str else []
        rv = [tag_replace(x, service).strip().lower() for x in tag_list]
        rv.append(self._get_cleanup_tag())
        return rv

    def _get_cleanup_tag(self):
        return "rancon-{}".format(self.cleanup_id)

    def _get_service_id(self, service):
        tmp = tag_replace(self.id_schema, service).lower()
        return re.sub(r"[^a-z0-9-]", "-", tmp)

    @staticmethod
    def _convert_to_service(consul_service, **override_values):
        tmp = {
            'host': consul_service['ServiceAddress'],
            'port': consul_service['ServicePort'],
            'name': consul_service['ServiceName'],
            'tags': consul_service['ServiceTags'],
            'id':   consul_service['ServiceID'],
        }
        return DotMap({**tmp, **override_values})


def get():
    """ returns this model's main class """
    return ConsulBackend
