'''This module defines the ModifyJarBuilder class.'''
from buildsystem.java import JavaBuilder, task

class ModifyJarBuilder(JavaBuilder):
    '''The ModifyJarBuilder is used to modify an existing jar file (replace some contents, etc).'''
    skip = ['compile', 'crypt', 'resources', 'copy_meta_inf', 'jar', 'exe']
    overwrite_dir = None
    version_properties = None

    @task('version_properties')
    def do_version_properties(self):
        '''Write a .properties file with version information, if conf string
        `version_properties` is given.'''
        if self.version_properties and self.version:
            with open(self.version_properties, 'w') as file:
                file.write('VERSION=%s' % self.version)

    @task('overwrite')
    def do_overwrite(self):
        '''Copies all files under `overwrite_dir` into `bindir`/classes if
        `overwrite_dir` is set.'''
        if self.overwrite_dir:
            self.copytree(self.overwrite_dir + '/', self.bindir + '/classes/', compare_date=False)

    @task('re-jar')
    def re_jar(self):
        '''This executes the `do_jar` method of the JavaBuilder in order to
        create the resulting jar file.'''
        self.do_jar()

    @task('re-exe')
    def re_exe(self):
        '''This task wrapps the jar file into a windows executable.'''
        self.do_exe()
