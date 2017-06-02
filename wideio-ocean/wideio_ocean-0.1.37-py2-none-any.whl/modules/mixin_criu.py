import json
import logging
import os
import re
import subprocess


class MixIn(object):
    @classmethod
    def criu_prep(cls):
        """
        Prepare CRIU to be usable with ocean.
        """
        os.system("getent group | grep -q criu || (sudo groupadd criu; sudo usermod -a -G criu $(whoami))")
        os.system("sudo /bin/sh -c 'chgrp criu $(which criu); chmod 4711 $(which criu)'")
        p = subprocess.Popen("sudo gcc -O2 -x c -o /usr/sbin/criu_tty -", shell=True, stdin=subprocess.PIPE)
        p.communicate("""#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <limits.h>
#include <errno.h>


int main(int argc, char ** argv) {
    struct stat str;
    char path[PATH_MAX+1];
    unsigned int rdev, dev;

    if (argc<=1) {
        fprintf(stderr,"criu_tty <pid>\\n");
        return -1;
    }

    snprintf(path,PATH_MAX,"/proc/%d/fd/0",atoi(argv[1]));
    if (stat(path,&str)!=-1) {
        rdev=str.st_rdev;
        dev=str.st_dev;
        printf("tty[%x:%x]\\n", rdev,dev);
        return 0;
    }
    else {
        fprintf(stderr,"%s\\n", strerror(errno));
        return -1;
    }

}
""")
        os.system(
            "sudo /bin/sh -c 'chown root /usr/sbin/criu_tty;chgrp criu /usr/sbin/criu_tty; chmod 4751 /usr/sbin/criu_tty'")

    @classmethod
    def _criu_compute_externals(cls, mounts, pid, mode="dump"):
        res = []
        for m in mounts:
            res.append("--ext-mount-map %s:%s" % (m["Destination"], m["Destination"]))
            # res.append("--skip-mnt %s"%(m,))
        for f in ["/etc/hosts", "/etc/hostname", "/dev/console", "/etc/resolv.conf"]:
            res.append("--skip-mnt %s" % (f,))
        for f in ["/sys/fs/cgroup/perf_event", "/sys/fs/cgroup/cpuset", "/sys/fs/cgroup/cpu,cpuacct",
                  "/sys/fs/cgroup/memory",
                  "/sys/fs/cgroup/pids", "/sys/fs/cgroup/freezer", "/sys/fs/cgroup/systemd", "/sys/fs/cgroup/devices",
                  "/sys/fs/cgroup/blkio", "/sys/fs/cgroup/hugetlb", "/sys/fs/cgroup/net_cls,net_prio"
                  ]:
            res.append("--skip-mnt %s" % (f,))
        res.append("-l")
        res.append("--tcp-established")
        res.append("--evasive-devices")

        try:
            o, e = subprocess.Popen(["/usr/sbin/criu_tty", "%d" % (pid,)], stdout=subprocess.PIPE).communicate()
            res.append("--external '%s'" % (o.strip(),))
        except Exception as e:
            logging.warning(e)

        return " ".join(res)

    @classmethod
    def criu_dump(cls, srv, n):
        cfgp = cls._ocean._get_cfgp(srv)
        cpd = os.path.join(cfgp, "checkpoints", n)
        if not os.path.exists(cpd):
            os.makedirs(cpd)
        o, e = subprocess.Popen("docker inspect %s" % (srv,), stdout=subprocess.PIPE, shell=True).communicate()
        pid = json.loads(o)[0]["State"]["Pid"]
        if pid == 0:
            logging.error("Invalid PID")
            raise ValueError(pid)
        externals = cls._criu_compute_externals(json.loads(o)[0]["Mounts"], pid)
        cmd = "criu dump --tree %d %s --images-dir %s/checkpoints/%s  --leave-running --track-mem" % (
            pid,
            externals,
            cfgp,
            n
        )
        logging.debug(cmd)
        subprocess.Popen(cmd, shell=True
                         ).communicate()

    @classmethod
    def criu_idump(cls, srv, n, pn):
        cfgp = cls._ocean._get_cfgp(srv)
        cpd = os.path.join(cfgp, "checkpoints", n)
        if not os.path.exists(cpd):
            os.makedirs(cpd)
        o, e = subprocess.Popen("docker inspect %s" % (srv,), stdout=subprocess.PIPE, shell=True).communicate()
        pid = json.loads(o)[0]["State"]["Pid"]
        if pid == 0:
            logging.error("Invalid PID")
            raise ValueError(pid)
        externals = cls._criu_compute_externals(json.loads(o)[0]["Mounts"], pid)
        cmd = ("criu dump --tree %d %s --images-dir %s/checkpoints/%s "
               " --prev-images-dir %s/checkpoints/%s  --leave-running --track-mem" % (
                   pid,
                   externals,
                   cfgp,
                   n,
                   cfgp,
                   pn
               ))
        logging.debug(cmd)
        subprocess.Popen(cmd, shell=True
                         ).communicate()

    @classmethod
    def criu_restore(cls, srv, n):
        cfgp = cls._ocean._get_cfgp(srv)
        deo = cls._ocean.dockerenv_options(srv, joined=False)
        # print(deo)
        externals = [re.sub("-v ([^:]+):([^:]+)", lambda m: "--ext-mount-map %s:%s" % (os.path.abspath(m.group(2)),
                                                                                       m.group(1)), o)
                     for o in deo if o.strip().startswith("-v")]
        cmd = "criu restore  %s --images-dir %s/checkpoints/%s" % (
            " ".join(externals),
            cfgp,
            n,
        )
        logging.debug(cmd)
        subprocess.Popen(cmd, shell=True).communicate()
