# allow to save current versions in the manifest
# and or to fetch specific versions from the docker-repo

import copy
import hashlib
import itertools
import json


class MixIn(object):
    _vc = None

    @classmethod
    def raw_freeze(cls, stage="ready"):
        """ Give freeze information for all installed images and containers on the system"""
        dc = cls._ocean._docker
        res = {}
        for c in itertools.chain(dc.containers(), dc.images(all=True)):
            if c is None:
                continue

            version = (c.get("Labels") or {}).get("VERSION", "latest")
            name = None
            if "RepoTags" in c:
                name = c["RepoTags"][0].split(":")[0]
                if name == "<none>":
                    name = None
            if name is None and "Names" in c:
                name = c["Names"][0].split('/')[-1]
            if name in res:
                continue
            if version == "latest":
                if "RepoTags" in c:
                    for t in c["RepoTags"]:
                        v = c["RepoTags"][0].split(":")[-1]
                        if v.startswith(stage + "-"):
                            version = v[len(stage) + 1:]
                            if version != "latest":
                                break
            if name is not None:
                res[name] = version
#        for i in dc.images(all=True):

        return res

    @classmethod
    def get_version(cls, srv, stage="ready"):
        """ Give freeze information for all installed images and containers on the system"""
        if cls._vc is None:
            cls._vc = cls.raw_freeze()
        return cls._vc.get(srv, "latest")  # get_commitid

    @classmethod
    def freeze(cls, srv=None, version_only=False, stage="ready"):
        """ Give freeze information for all installed images and containers on the system"""
        res = {}
        if srv and len(srv):
            imanifest = cls._ocean.submanifest(srv)
        else:
            imanifest = cls._ocean.manifest
        for sn, sv in imanifest.items():
            for srv, srvd in sv.items():
                if not version_only:
                    res.setdefault(sn, {})[srv] = copy.copy(srvd)
                # print  sn, srv,               res[sn][srv]
                res.setdefault(sn, {}).setdefault(srv, {})["version"] = cls.get_version(srv)
        return res

    @classmethod
    def freeze_hash(self, srv):
        """Returns the freeze hash associated with a specific version of the manifest"""
        return hashlib.md5(json.dumps(self.freeze(srv)).encode('utf-8')).hexdigest()
