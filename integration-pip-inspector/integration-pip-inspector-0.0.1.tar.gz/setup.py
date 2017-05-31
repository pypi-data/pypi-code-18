import os

from setuptools import setup, find_packages

package_name = "integration-pip-inspector"
package_version = "0.0.1"

setup(
    name=package_name,
    version=package_version,
    author="Black Duck Software",
    author_email="bdsoss@blackducksoftware.com",
    description=(
        "Generates and deploys Black Duck I/O files for use with the Black Duck Hub"),
    license="Apache 2.0",
    keywords="integration_pip_inspector blackduck hub",
    url="https://github.com/blackducksoftware/hub-pip",
    install_requires=["configparser", "six", "docopt"],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        '': ['*.md', '*.ini'],
    },
    entry_points={
        "console_scripts": [
            "integration_pip_inspector=hub_pip.Main:cli",
        ],
        "distutils.commands": [
            "integration_pip_inspector=integration_pip_inspector.BlackDuckPlugin:BlackDuckCommand",
        ]
    },
)
