import json
import os
import re
import subprocess


class MixIn(object):
    """
    Handles modification and manipulation of manifest files.
    """

    @classmethod
    def create_manifest(cls, *options):
        """
        Create a new manifest branch an specify which version of the api to use
        """
        so = 0
        doupdate = False
        while options[so][0] == "-":
            if options[so] == "-u":
                doupdate = True
                so += 1
        branch = options[so]
        so += 1
        o, e = cls.process_run("git checkout master", shell=True, cwd=cls._ocean.manifest_PATH).communicate()
        cls._read_manifest()
        for i in zip(options[so::2], options[(so + 1)::2]):
            processed = False
            for mk in list(cls._ocean.omanifest.keys()):
                for k in list(cls._ocean.omanifest[mk].keys()):
                    if re.match(i[0], k):
                        cls._ocean.omanifest[mk][k]["version"] = i[1]
                        processed = True
            if not processed:
                raise ValueError("Unknown service " + i[0])

        _o, _e = cls._ocean.process_run("git branch -D %s" % (branch,),
                                        shell=True, cwd=cls._ocean.manifest_PATH).communicate()
        _o, _e = cls._ocean.process_run("git branch %s" % (branch,),
                                        shell=True, cwd=cls._ocean.manifest_PATH).communicate()
        _o, _e = cls._ocean.process_run("git checkout %s" % (branch,),
                                        shell=True, cwd=cls._ocean.manifest_PATH).communicate()
        open(os.path.join(cls._ocean.manifest_PATH, "manifest.json"), "wb").write(
            json.dumps(cls._ocean.omanifest, indent=2, sort_keys=True)
        )
        _o, _e = cls.process_run("git commit -a -m 'updated manifest %s'" % (
            str(list(zip(options[so::2], options[(so + 1)::2]))).replace("'", "")), shell=True,
            cwd=cls._ocean.manifest_PATH).communicate()
        if doupdate:
            _o, _e = cls.process_run("git push --set-upstream origin %s" % (branch,), shell=True,
                                     cwd=cls._ocean.manifest_PATH).communicate()

    @classmethod
    def manifest_update(cls, *options):
        """
        TBC: Read current anifest and update ?
        """
        so = 0
        doupdate = False
        mergefrom = None
        while options[so][0] == "-":
            if options[so] == "-u":
                doupdate = True
                so += 1
            if options[so] == "-m":
                mergefrom = options[so + 1]
                so += 2

        branch = options[so]
        so += 1
        cls.process_run("git checkout %s" % (branch,), shell=True, cwd=cls._ocean.manifest_PATH).communicate()
        if mergefrom:
            cls.process_run("git merge -X theirs --no-commit --no-ff %s" % (mergefrom,), shell=True,
                            cwd=cls._ocean.manifest_PATH).communicate()
        cls._read_manifest()
        for i in zip(options[so::2], options[(so + 1)::2]):
            processed = False
            for mk in list(cls.omanifest.keys()):
                for k in list(cls.omanifest[mk].keys()):
                    if re.match(i[0], k):
                        cls.omanifest[mk][k]["version"] = i[1]
                        processed = True
            if not processed:
                raise ValueError("Unknown service " + i[0])

        cls.process_run("git branch %s" % (branch,), shell=True, cwd=cls._ocean.manifest_PATH).communicate()
        cls.process_run("git checkout %s" % (branch,), shell=True, cwd=cls._ocean.manifest_PATH).communicate()
        open(os.path.join(cls._ocean.manifest_PATH, "manifest.json"), "wb").write(json.dumps(cls.omanifest, indent=2,
                                                                                             sort_keys=True))
        cls.process_run("git commit -a -m 'updated manifest %s'" % (
            str(list(zip(options[so::2], options[(so + 1)::2]))).replace("'", "")), shell=True,
            cwd=cls._ocean.manifest_PATH).communicate()
        if doupdate:
            cls.process_run("git push --set-upstream origin %s" % (branch,), shell=True,
                            cwd=cls._ocean.manifest_PATH).communicate()

    @classmethod
    def checkout_manifest(cls, srv=None, *options):
        """Pull existing service(s).

         Also set sources to match at the cls._ocean.manifest version.
        """
        if srv is None:
            for k in list(cls._ocean.manifest.keys()):
                for s in cls._ocean.manifest[k]:
                    cls.checkout_manifest(s)
            return
        section = cls._ocean._find_section(srv)

        if "url" in cls._ocean.manifest[section][srv]:
            assert (os.path.exists(cls._ocean.SRC))
            srvp = os.path.join(cls._ocean.SRC, section, cls._src_folder(srv))
            assert (os.path.exists(srvp))
            if "-u" in options:
                _o, _e = subprocess.Popen("git pull", shell=True, cwd=srvp).communicate()
            if "version" in cls._ocean.manifest[section][srv]:
                v = cls._ocean.manifest[section][srv]["version"]
                if v[0].isdigit():
                    _o, _e = subprocess.Popen(
                        "git checkout master;git branch -d %s||true;git checkout tags/%s -b %s" % (v, v, v), shell=True,
                        cwd=srvp).communicate()
                else:
                    _o, _e = subprocess.Popen("git checkout master; git checkout %s" % (v,), shell=True,
                                              cwd=srvp).communicate()
            if "-u" in options:
                cls.update_requirements(srv)
