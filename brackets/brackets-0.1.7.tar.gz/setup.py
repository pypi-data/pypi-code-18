from distutils.core import setup

setup(
    name='brackets',
    version='0.1.7',
    author='Pooya Eghbali',
    author_email='persian.writer@gmail.com',
    packages=['brackets'],
    url='https://github.com/pooya-eghbali/brackets',
    license='BSD',
    description="""Use brackets instead of indentation.""",
    classifiers= ['Intended Audience :: Developers',
                  'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                  'Operating System :: OS Independent',
                  'Programming Language :: Python :: 2',
                  'Programming Language :: Python :: 3'],
    keywords = 'brackets, indentation, indent, indenting, parser, encoding',
	platforms = ["Any"],
	long_description=open('README.txt').read()
)
