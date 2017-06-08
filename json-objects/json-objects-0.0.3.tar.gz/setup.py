from setuptools import setup


setup(
    name='json-objects',
    version='0.0.3',
    py_modules=['json_objects'],
    zip_safe=False,
    url='https://github.com/fraglab/json-objects',
    download_url='https://github.com/fraglab/json-objects/archive/0.0.3.tar.gz',
    entry_points={
        'kombu.serializers': [
            'json_objects = json_objects:register_args'
        ]
    }
)
