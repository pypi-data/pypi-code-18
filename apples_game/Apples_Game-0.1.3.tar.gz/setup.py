from distutils.core import setup

setup(
	name='Apples_Game',
        version= '0.1.3',
        author='Mahnoor Imran',
        author_email='mimran2@gmu.edu',
        packages=['applesGame'],
        url='http://pypi.python.org',
        license='MIT',
        description='Guess the color of the Apple!',
        long_description=open('README.txt').read(),
	classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    	],
        entry_points={
		'console_scripts': [
			'play = applesGame:main'    
		]},
)


