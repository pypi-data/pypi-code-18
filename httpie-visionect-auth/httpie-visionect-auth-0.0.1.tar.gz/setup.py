from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='httpie-visionect-auth',
    description='HMAC Auth plugin for Joan Visionect and HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='0.0.1',
    author='Pierre Coueffin',
    author_email='pcoueffin@gmail.com',
    license='MIT',
    url='https://github.com/pcoueffin/httpie-visionect-auth',
    download_url='https://github.com/pcoueffin/httpie-visionect-auth',
    py_modules=['httpie_visionect_auth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_visionect_auth = httpie_visionect_auth:HmacAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
