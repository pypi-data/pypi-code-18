import os

import delegator


class ProcessRunner():
    def __init__(self, cmd):
        self.cmd = cmd
        self.args = []
        self.env = os.environ.copy()

    def add_arg(self, arg):
        self.args.append(arg)

    def add_env(self, env):
        self.env.update(env)

    def get_env(self):
        return self.env

    def build_cmd(self):
        return [self.cmd] + self.args

    def __str__(self):
        return ' '.join(self.build_cmd())

    def do_run(self):
        proc = delegator.run(self.__str__(), block=False)
        return proc


class JavaProcessRunner(ProcessRunner):
    def __init__(self):
        ProcessRunner.__init__(self, "java")

    def add_system_env(self, name, value):
        self.add_arg("-D{}={}".format(name, value))

    def add_heap_opt(self, heap_min, heap_max):
        self.add_arg("-Xms{}".format(heap_min))
        self.add_arg("-Xmx{}".format(heap_max))

    def add_gc_opts(self, gc_opts):
        if gc_opts is not None:
            for opt in gc_opts:
                self.args.append("-XX:+{}".format(opt))

    def add_debug_opts(self, debug_opt):
        if debug_opt is not None:
            self.args.append("-Xdebug")
            self.args.append("-X{}".format(debug_opt))


class JavaClassRunner(JavaProcessRunner):
    def __init__(self, main_class):
        JavaProcessRunner.__init__(self)
        self.main_class = main_class
        self.classpath = []

    def add_classpath(self, path):
        self.classpath.append(path)

    def set_classpath(self, classpath):
        self.classpath = classpath

    def build_cmd(self):
        c = ProcessRunner.build_cmd(self)
        if len(self.classpath) > 0:
            c.append("-classpath")
            c.append(":".join(self.classpath))
        c.append(self.main_class)
        return c


class JavaJarRunner(JavaProcessRunner):
    def __init__(self, jar_file):
        JavaProcessRunner.__init__(self)
        self.jar_file = jar_file

    def build_cmd(self):
        c = ProcessRunner.build_cmd(self)
        c.append("-jar")
        c.append(os.path.abspath(self.jar_file))
        return c


class DefaultDashbaseServiceRunner(JavaJarRunner):
    def __init__(self, home_dir, svc_name, version):
        self.svcLocation = "{}/dashbase-{}".format(os.path.abspath(home_dir), svc_name)
        jar = "{}/target/dashbase-{}-{}.jar".format(self.svcLocation, svc_name, version)
        JavaJarRunner.__init__(self, jar)

    def build_cmd(self):
        c = JavaJarRunner.build_cmd(self)
        c.append("server {}/conf/config.yml".format(self.svcLocation))
        return c
