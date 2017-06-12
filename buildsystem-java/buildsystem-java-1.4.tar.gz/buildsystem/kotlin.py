'''This module defines the KotlinBuilder.'''
import os
from buildsystem.java import JavaBuilder, task

class KotlinBuilder(JavaBuilder):
    '''Builds kotlin projects.'''
    kotlinpath = 'Y:/Bin/kotlinc'

    @task('compile', 4)
    def kotlin_compile(self):
        '''Compile Kotlin files.'''
        if not os.path.exists(self.bindir):
            os.mkdir(self.bindir)
        if not os.path.exists(self.bindir + '/classes/'):
            os.mkdir(self.bindir + '/classes/')
        classpath = ';'.join([self.libdir + '/' + s for s in self.depends])
        kotlinc = os.path.join(self.kotlinpath, 'bin', 'kotlinc.bat')
        cmd = [kotlinc, '-nowarn', '-cp', classpath, '-d', self.bindir + '/classes', self.srcdir]
        self.run(cmd)
