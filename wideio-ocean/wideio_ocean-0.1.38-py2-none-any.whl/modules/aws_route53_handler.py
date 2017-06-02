import logging
import os
import socket
from functools import reduce

import boto


class AWSRoute53Handler(object):
    """
    Module to add CNAME to a host when a specified container starts
    """

    default_action = "upsert"
    ttl = 500

    @classmethod
    def on_ocean_start(cls, ocean):
        cls._ocean = ocean

    @classmethod
    def on_post_start(cls, name, *args):
        """
        Add cnames to a host that starts a specified container

        :param name: name of the container
        :param manifest_description: manifest record for the service.
        :return:
        """
        pass

    @classmethod
    def register_cnames(cls):
        """
        Register cnames associated with containers to local machine IP or OCEAN_HOSTNAME
        :return:
        """
        cls.btc = boto.connect_route53()
        cls.zones = cls.btc.get_zones()
        rrss = {}
        for c in cls._ocean.manifest.items():
            for sn, s in c[1].items():
                if "cnames" in s:
                    try:
                        rrss = cls._add_cnames_for_service(sn, s, rrss)
                    except Exception as e:
                        logging.warning("Error registering domain %s : %s" % (sn, e,))
        for rrs in rrss.values():
            if len(rrs[0].__dict__["changes"]):
                rrs[0].commit()
            if len(rrs[1].__dict__["changes"]):
                rrs[1].commit()

    @classmethod
    def _add_cnames_for_service(cls, name, manifest_description, rrss=None):
        if manifest_description.get("cnames"):
            hostfqn = manifest_description.get("cname-target", os.environ.get("OCEAN_HOSTNAME", socket.getfqdn()))
            for fqn in manifest_description.get("cnames"):
                hz = None
                for cz in cls.zones:
                    if fqn.endswith("." + cz.name[:-1]) or fqn == cz.name[:-1]:
                        hz = cz
                        break
                if hz is None:
                    raise ValueError("Could not find hosted zone for cname:" + fqn)
                hzid = hz.id
                if hzid not in rrss:
                    rrss[hzid] = (boto.route53.record.ResourceRecordSets(cls.btc, hzid),
                                  boto.route53.record.ResourceRecordSets(cls.btc, hzid)
                                  )

                # we make the name point to our host
                fqnd = fqn
                if not fqnd.endswith("."):
                    fqnd += "."
                cls._filter_out_rr(cls.btc, hzid, rrss[hzid][0], name=fqnd, type="CNAME")
                cls._new_rr(rrss[hzid][1], fqn, "CNAME", hostfqn)
        return rrss

    @classmethod
    def _all_rr(cls, btc, hzid):
        """Return and list all resource records."""
        return btc.get_all_rrsets(hzid)

    @classmethod
    def _find_rr(cls, btc, hzid, **kwargs):
        """Find specific resource recorfs."""
        return filter(lambda x: reduce(lambda b, c: b and (getattr(x, c[0]) == c[1]), kwargs.items(), True),
                      cls._all_rr(btc, hzid)
                      )

    @classmethod
    def _filter_out_rr(cls, btc, hzid, rrs, **kwargs):
        """Add changes to remove record set from zone."""
        crl = cls._find_rr(btc, hzid, **kwargs)

        for ccr in crl:
            kwargs2 = {"type": ccr.type, "ttl": ccr.ttl, "name": ccr.name}
            change = rrs.add_change("DELETE", **kwargs2)
            for v in ccr.resource_records:
                change.add_value(v)

    @classmethod
    def _new_rr(cls, rrs, name, cname, *values):
        """Add new record with multiple values."""
        change = rrs.add_change("CREATE", name, type=cname, ttl=cls.ttl)
        for v in values:
            change.add_value(v)


__handler__ = AWSRoute53Handler
