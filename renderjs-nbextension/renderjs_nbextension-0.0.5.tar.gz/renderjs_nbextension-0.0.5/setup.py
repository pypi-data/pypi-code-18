# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='renderjs_nbextension',
    version='0.0.5',
    packages=['renderjs_nbextension'],
    package_data = {
        '': ['*.js', '*.html', '*.json']
    },

    # PyPI Data
    author='Sebastian Kreisel',
    author_email='sebastian.kreisel@nexedi.com',
    description='RenderJS gadgets for jupyter (frontend-part)',
    keywords='renderjs jupyter nbextension',
    license='GPL 2',
    url='https://lab.nexedi.com/Kreisel/renderjs_extension'
)
