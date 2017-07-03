from setuptools import setup

setup(  name='methrafo',
		version='1.0.0',
		description='MeDIP-Seq Methylation Level Random-forest based Estimator',
		author='Jun Ding',
		author_email='jund@andrew.cmu.edu',
		url="https://github.com/phoenixding/methrafo",
		license='MIT',
		packages=['methrafo'],
		entry_points={'console_scripts':['methrafo.predict=methrafo.meth_predict:main','methrafo.train=methrafo.meth_train:main',
											'methrafo.download=methrafo.download_genomes:main', 'methrafo.bamScript=methrafo.bamScripts:main']},
		install_requires=['scipy','numpy','scikit-learn','pyBigWig'],
		data_files=[('model',['model/rr.pkl'])]
		#install_requires=['scipy >=0.9','numpy >=1.6.1','scikit-learn >=0.18.1']
		)
