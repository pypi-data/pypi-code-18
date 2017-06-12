"""This module defines the JavaBuilder class."""
import os
import shutil
import zipfile
from concurrent.futures import ThreadPoolExecutor
from buildsystem.base import BaseBuilder, task
from buildsystem.dependency_resolver import FileDependencyResolver

class JavaBuilder(BaseBuilder):
    """Builds Java projects."""
    def __init__(self):
        BaseBuilder.__init__(self)
        self.libdir = 'lib'
        self.srcdir = 'src'
        self.bindir = 'bin'
        self.allatori_version = '5.3'
        self.jar2exedir = 'cfg'
        self.version_in_filename = True
        self.version = None
        self.pack_all_in_one_jar = True
        self.dependency_resolver = FileDependencyResolver('/Lib/Java')
        self.cleandirs = []
        self.depends = []
        self.main_class = None
        self.crypt = []

    def initbuild(self):
        """Defines some initialization steps such as setting up `cleandirs`."""
        self.cleandirs = [self.bindir, self.libdir]

    def unpack(self, jar_file, out):
        '''Unpack single jar file `jar_file` to `out` directory.'''
        with open(jar_file, 'rb') as file:
            zipf = zipfile.ZipFile(file)
            for name in zipf.namelist():
                zipf.extract(name, out)

    @task('clean')
    def do_clean(self):
        '''Cleaning up all `cleandirs`'''
        [shutil.rmtree(d) for d in self.cleandirs if os.path.exists(d)]

    @task('dependencies')
    def do_dependencies(self):
        '''Get required dependencies from specified `dependency_resolver`.'''
        if not os.path.exists(self.libdir):
            os.mkdir(self.libdir)
        for dep in self.depends:
            self.dependency_resolver.resolve(dep, self.libdir)

    @task('compile')
    def do_compile(self):
        '''Compile Java files.'''
        if not os.path.exists(self.bindir):
            os.mkdir(self.bindir)
        if not os.path.exists(self.bindir + '/classes/'):
            os.mkdir(self.bindir + '/classes/')
        classpath = ';'.join([self.libdir + '/' + s for s in self.depends])
        if hasattr(self, 'main_class') and self.main_class is not None:
            main = '%s/%s.java' % ('src', self.main_class.replace('.', '/'),)
            cmd = ['javac', '-encoding', 'utf8', '-sourcepath', self.srcdir, '-cp',
                   classpath, '-d', self.bindir + '/classes', main]
            self.run(cmd)
        else:
            with ThreadPoolExecutor(max_workers=4) as executor:
                files = []
                for (path, _, files) in os.walk(self.srcdir):
                    for file in files:
                        if file[-5:] == '.java':
                            file = path + '\\' + file
                            file = file.replace('\\', '/')
                            files.append(file)
                            if len(files) >= 100:
                                cmd = ['javac', '-sourcepath', self.srcdir, '-cp',
                                       classpath, '-d', self.bindir + '/classes']
                                cmd.extend(files)
                                executor.submit(self.run, cmd)
                                files = []

                # feet the compiler with the rest of the java files
                if len(files) > 0:
                    cmd = ['javac', '-sourcepath', self.srcdir, '-cp', classpath, '-d',
                           self.bindir + '/classes']
                    cmd.extend(files)
                    self.run(cmd)

    @task('crypt')
    def do_crypt(self):
        '''Crypt all class files and jars that are specified in `crypt`.
            To do that it uses the Allatori Obfuscator. It tries to get this dependency
            from the `dependency_resolver`.
        '''
        self.output('\n   ')
        shutil.copytree(self.bindir + '/classes/', self.bindir + '/classes_temp/')
        shutil.rmtree(self.bindir + '/classes/')
        for crypt in self.crypt:
            self.output('   -> ' + crypt + ' ... ')
            self.unpack('lib/%s' % crypt, self.bindir + '/classes_temp/')
            os.remove('lib/%s' % crypt)
            self.output('Ok\n   ', ok=True)
        if not os.path.exists('buildlibs'):
            os.mkdir('buildlibs')
        self.dependency_resolver.resolve('allatori-%s.jar' % self.allatori_version, 'buildlibs')
        self.output('   crypt all ... ')
        self.run(['java', '-jar', 'buildlibs/allatori-%s.jar' % self.allatori_version,
                  'cfg/allatori.xml'])
        shutil.rmtree(self.bindir + '/classes_temp/')

    @task('resources')
    def do_resources(self):
        '''Copies all resources under `srcdir` dictionary, excluding *.java files.'''
        self.copytree(self.srcdir + '/', self.bindir + '/classes/', exclude_ext=['.java'])

    @task('lib_classes')
    def do_lib_classes(self):
        '''If `pack_all_in_one_jar` is True it extracts all dependencies into
            the class folder.
        '''
        if self.pack_all_in_one_jar:
            self.output('\n      ')
            for dep in self.depends:
                lib = '%s/%s' % (self.libdir, dep,)
                if os.path.exists(lib):
                    self.output('-> ' + dep + ' ... ')
                    self.unpack(lib, self.bindir + '/classes/')
                    self.output('Ok\n      ', ok=True)
        else:
            self.output('Skipped\n      ', warn=True)

    @task('copy_meta_inf')
    def do_copy_meta_inf(self):
        '''Copies the contents of the META-INF folder if any into the `bindir`.'''
        src = '%s/META-INF/' % self.srcdir
        dest = '%s/classes/META-INF/' % self.bindir
        if os.path.exists(src):
            if os.path.exists(dest):
                shutil.rmtree(dest)
            self.copytree(src, dest)

    @task('jar')
    def do_jar(self):
        '''Create jar file.'''

        if self.version_in_filename:
            name = '%s/%s-%s.jar' % (self.bindir, self.product_title, self.version,)
        else:
            name = '%s/%s.jar' % (self.bindir, self.product_title,)

        if hasattr(self, 'main_class') and self.main_class is not None:
            self.run(['jar', 'cfe', name, self.main_class, '-C', '%s/classes/' % self.bindir, '.'])
        else:
            self.run(['jar', 'cf', name, '-C', '%s/classes/' % self.bindir, '.'])

    @task('exe')
    def do_exe(self):
        '''Create exe file.'''
        cwd = os.getcwd()
        os.chdir(self.jar2exedir)
        minus = 0
        if self.jar2exedir is '.':
            minus = 1
        if self.version_in_filename:
            self.run(['jar2exe.exe', '../' * (len(self.jar2exedir.split('/')) - minus) +
                      '%s\\%s-%s.jar' % (self.bindir, self.product_title, self.version,)])
        else:
            self.run(['jar2exe.exe', '../' * (len(self.jar2exedir.split('/')) - minus) +
                      '%s\\%s.jar' % (self.bindir, self.product_title,)])
        os.chdir(cwd)
