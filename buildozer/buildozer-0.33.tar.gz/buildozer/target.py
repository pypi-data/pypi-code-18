from sys import exit


def no_config(f):
    f.__no_config = True
    return f


class Target(object):
    def __init__(self, buildozer):
        super(Target, self).__init__()
        self.buildozer = buildozer
        self.build_mode = 'debug'
        self.platform_update = False

    def check_requirements(self):
        pass

    def check_configuration_tokens(self, errors=None):
        if errors:
            self.buildozer.info('Check target configuration tokens')
            self.buildozer.error(
                '{0} error(s) found in the buildozer.spec'.format(
                len(errors)))
            for error in errors:
                print(error)
            exit(1)

    def compile_platform(self):
        pass

    def install_platform(self):
        pass

    def get_custom_commands(self):
        result = []
        for x in dir(self):
            if not x.startswith('cmd_'):
                continue
            if x[4:] in self.buildozer.standard_cmds:
                continue
            result.append((x[4:], getattr(self, x).__doc__))
        return result

    def get_available_packages(self):
        return ['kivy']

    def run_commands(self, args):
        if not args:
            self.buildozer.error('Missing target command')
            self.buildozer.usage()
            exit(1)

        result = []
        last_command = []
        while args:
            arg = args.pop(0)
            if arg == '--':
                if last_command:
                    last_command += args
                    break
            elif not arg.startswith('--'):
                if last_command:
                    result.append(last_command)
                    last_command = []
                last_command.append(arg)
            else:
                if not last_command:
                    self.buildozer.error('Argument passed without a command')
                    self.buildozer.usage()
                    exit(1)
                last_command.append(arg)
        if last_command:
            result.append(last_command)

        config_check = False

        for item in result:
            command, args = item[0], item[1:]
            if not hasattr(self, 'cmd_{0}'.format(command)):
                self.buildozer.error('Unknown command {0}'.format(command))
                exit(1)

            func = getattr(self, 'cmd_{0}'.format(command))

            need_config_check = not hasattr(func, '__no_config')
            if need_config_check and not config_check:
                config_check = True
                self.check_configuration_tokens()

            func(args)

    def cmd_clean(self, *args):
        self.buildozer.clean_platform()

    def cmd_update(self, *args):
        self.platform_update = True
        self.buildozer.prepare_for_build()

    def cmd_debug(self, *args):
        self.buildozer.prepare_for_build()
        self.build_mode = 'debug'
        self.buildozer.build()

    def cmd_release(self, *args):
        error = self.buildozer.error
        self.buildozer.prepare_for_build()
        if self.buildozer.config.get("app", "package.domain") == "org.test":
            error("")
            error("ERROR: Trying to release a package that starts with org.test")
            error("")
            error("The package.domain org.test is, as the name intented, a test.")
            error("Once you published an application with org.test,")
            error("you cannot change it, it will be part of the identifier")
            error("for Google Play / App Store / etc.")
            error("")
            error("So change package.domain to anything else.")
            error("")
            error("If you messed up before, set the environment variable to force the build:")
            error("export BUILDOZER_ALLOW_ORG_TEST_DOMAIN=1")
            error("")
            if "BUILDOZER_ALLOW_ORG_TEST_DOMAIN" not in os.environ:
                exit(1)

        if self.buildozer.config.get("app", "package.domain") == "org.kivy":
            error("")
            error("ERROR: Trying to release a package that starts with org.kivy")
            error("")
            error("The package.domain org.kivy is reserved for the Kivy official")
            error("applications. Please use your own domain.")
            error("")
            error("If you are a Kivy developer, add an export in your shell")
            error("export BUILDOZER_ALLOW_KIVY_ORG_DOMAIN=1")
            error("")
            if "BUILDOZER_ALLOW_KIVY_ORG_DOMAIN" not in os.environ:
                exit(1)

        self.build_mode = 'release'
        self.buildozer.build()

    def cmd_deploy(self, *args):
        self.buildozer.prepare_for_build()

    def cmd_run(self, *args):
        self.buildozer.prepare_for_build()

    def cmd_serve(self, *args):
        self.buildozer.cmd_serve()
