import logging
import os
import re


class MixIn(object):
    """
    MixIn to allow to run program in dev mode.

    Characteristics of dev mode are :
    - connected with databases and other requrired services...
    - ability to run editor/debugger with UI from the container (hence host network ?)
    """

    @classmethod
    def dev(cls, srv, *options, **kwargs):
        """
        Runs devmode in a service

        -n : specifc suffix for the instances
        -c : command to be run
        """
        skip_required = False
        command = "/bin/bash --noprofile --norc"
        name = "dev"
        if "-n" in options:
            name = options[options.index("-n") + 1]
        if "-c" in options:
            command = options[-1]

        # TODO: use getent
        if not os.path.isdir(os.path.join(cls._ocean.CFGL, srv)):
            os.makedirs(os.path.join(cls._ocean.CFGL, srv))

        devpasswd = os.path.join(cls._ocean.CFGL, srv, "devpasswd")
        devpass = open(devpasswd, "w+")
        devpass.write("{U}:x:{uid}:{uid}:{U},,,:/home/{srvt}:/bin/bash\n".format(U=os.getlogin(),
                                                                                 srvt=srv,
                                                                                 uid=str(os.getuid())
                                                                                 )
                      )
        devpass.close()

        section, srv, tag = cls._ocean._find_section_new(srv)
        srvp = cls._ocean._get_srcp(srv, section)

        #
        # start required database, servers, etc...
        #
        if "requires" in cls._ocean.manifest[section][srv] and not skip_required:
            for ss in cls._ocean._get(srv)["requires"]:
                cls._ocean._call_with_eh("start", ss)

        cls._ocean._alt_fullyconnect()

        # start dev container if not started
        logging.debug("starting container if not started:" + name)
        cls._ocean.shell(srv, "-d", "-v", "-n", name, command="/bin/bash -c 'sleep infinity'", xtraargs=[
            "--net=host",
            #                      "--device /dev/snd/pcmC0D0c"
            #                      "--device /dev/snd/pcmC0D0p"
            #                      "--device /dev/snd/controlC0"
            #                      "--device /dev/snd/timer"
            "-v /tmp:/tmp",
            "-v " + os.path.join(cls._ocean.MPL, "hosts") + ":/etc/hosts",
            ("-u {uid} -e DISPLAY={DISPLAY} -e TERM={TERM}").format(dockerip=cls._ocean.dockerip,
                                                                    uid=str(os.getuid()),
                                                                    DISPLAY=os.environ["DISPLAY"],
                                                                    TERM=os.environ["TERM"]),
            "-e PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin"
            ":/usr/lib/jvm/java-7-openjdk-amd64/bin:/usr/local/pycharm/bin",
            "-e PS1={U}/\\$\\(id\\ -u\\)@\\\h:\\\w\\>\\ ".format(U=os.getlogin()),
            # "-v %s/pycharm-community-5.0.1:/usr/local/pycharm" % (os.environ["HOME"],),
            "-v %s/.PyCharm50:/home/%s/.PyCharm50" % (os.environ["HOME"], srv,),
            # "-v %s/PycharmProjects:/home/%s/PycharmProjects" % (os.environ["HOME"], srv,),
            "-v %s/.gitconfig:/home/%s/.gitconfig" % (os.environ["HOME"], srv,),
            # "-v %s/.ionic:/home/%s/.ionic" % (os.environ["HOME"], srv,),
            # "-v %s:/etc/passwd" % (devpasswd,)
        ], transform=lambda x: re.sub("--link=([^ ]+)", "", re.sub("-h ([^ ]+)", "", x)))
        logging.debug("started:" + name)

        # run automated tasks
        if os.path.exists(os.path.join(srvp, "ocean-dev.sh")):
            logging.debug("running ocean-dev.sh script")
            # note the script need to run in the same container as the main session
            # as we want to share files
            p = cls._ocean._subprocess_popen("konsole --noclose -e 'ocean exec_ %s -n dev -c ./ocean-dev.sh' &" % (srv,),
                                             shell=True, cwd=srvp)
            p.communicate()
        else:
            logging.debug(os.path.join(srvp, "ocean-dev.sh") + " not found")

        # run a normal shell to work
        logging.debug("running developer shell")
        cls._ocean.exec_(srv, "-v", "-n", name, command=command)
