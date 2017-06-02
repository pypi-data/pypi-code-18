import json
import os
import subprocess
import webbrowser

try:
    import docker
except BaseException:
    pass


class MixIn(object):
    @classmethod
    def dockviz(cls):
        # os.system("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nate/dockviz images -t")
        os.system("curl -s http://localhost:4243/images/json?all=1 "
                  "| docker run -i --rm -v /var/run/docker.sock:/var/run/docker.sock nate/dockviz images --tree")

    @classmethod
    def browser(cls, srv):
        if "browser" in cls._ocean._get(srv):
            url = cls._ocean._get(srv)["browser"].replace("$CONTAINERIP$", str(cls._ocean.get_ip(srv)))
            print(url)
            webbrowser.get('google-chrome').open(url)

    @classmethod
    def gitinspector(cls, srv):
        section = cls._ocean._find_section(srv)
        srvp = os.path.join(cls._ocean.SRC, section, cls._ocean._src_folder(srv))
        subprocess.Popen("gitinspector -T true -m true -F htmlembedded . > /tmp/out.html", shell=True,
                         cwd=srvp).communicate()
        os.system("google-chrome /tmp/out.html")

    @classmethod
    def convert_fixme_to_tickets(cls, srv, *options):
        """
        Transforms FIXME in the code into code issues in the project.
        """
        match = "."
        so = 0
        while options[so][0] == "-":
            if options[so] == "-m":
                match = options[so + 1]
                so += 2

        srvp = cls._ocean._get_srcp(srv)

        # Look in code for FIXME, TODO, BUG and convert it to in jira
        o, e = subprocess.Popen("egrep -w -n -r -e '(FIXME|BUG|TODO):' . | grep  py:| grep %s" % (match,),
                                stdout=subprocess.PIPE, cwd=srvp).communicate()
        print(o)

    @classmethod
    def rdock_manifest(cls, cfilter=None):
        """
        Create a manifest from all the repositories currently running on the system.

        A filter can optionally be passed too.

        c['Labels'].get('OCEAN.ENVIRONMENT')=='production'

        Note: this provide the option to save a manifest based on current running containers.
        It is also possible to run docker commands against currently running containers by
        setting `OCEAN_MANIFEST=docker:.*` and running and ocean command.
        """
        cfilter = cfilter or "True"
        nmanifest = {"services": {}}
        dc = docker.Client()
        for c in dc.containers():
            s = c["Names"][0].split("/")[-1]
            labels = c["Labels"]
            if eval(cfilter):
                for f in labels.items():
                    if f[0].startswith("OCEAN."):
                        obj = json.loads(f[1])
                        nmanifest["services"].setdefault(s, {})[f[0][6:].lower()] = obj.get("@value", obj)

        return json.dumps(nmanifest, indent=2)

    @classmethod
    def dockrepo_sweep(cls):
        # https://github.com/rstudio/docker-registry-sweeper
        # https: // github.com / merll / docker - registry - util
        os.system("docker-registry-sweeper -a 7d sweep")

    @classmethod
    def requirements(cls, srv, include_ip=False, indent="", format="text"):
        """
        Describe the requirements of a server by providing a tree view of the requirements
        :param srv:
        :param indent:
        :return:
        """
        res = []

        try:
            requires = cls._ocean._get(srv).get("requires", [])
            ip = ""
            if include_ip:
                ip = cls._ocean.get_ip(srv)
                if format == "text" and ip in [None, ""]:
                    ip = "not running"
            if format == "text":
                others = ""
                if include_ip:
                    others = " (%s)" % (ip,)
                res.append(indent + srv + others)
            else:
                res.append((srv, ip))
            for x in sorted(requires):
                res += cls.requirements(x, include_ip=include_ip, indent=indent + " " * 4)
        except BaseException:
            res.append(indent + srv + "[Not found !]")
        if not (len(indent)) and format == "text":
            res = "\n".join(res)
        return res
