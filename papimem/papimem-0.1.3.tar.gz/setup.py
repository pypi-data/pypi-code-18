from setuptools import setup, find_packages


setup(
    name="papimem",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        'click',
        'flask',
        'redis',
        'dsnparse',
        'mitmproxy',
    ],
    dependency_links=[
        'https://github.com/mitmproxy/mitmproxy/tarball/2.0.x#egg=mitmproxy-dev'
    ],
    entry_points={
        'console_scripts': [
            'papimem = papimem.cli:run',
        ],
    },
    author="Tomasz Czekanski",
    author_email="t.czekanski@gmail.com",
    description="Python API Request-Response Memorizer",
    long_description="""
    Tool which allows to memorize requests and corresponding responses
    made by your python application to external APIs.
    """,
    license="GPL",
    keywords=[
        "memorize requests", "api cache", "proxy", "analyze request-response"
    ],
    url="https://github.com/czekan/papimem",
    zip_safe=False,
    package_data={'papimem': ['web/templates/*.html']},
)
