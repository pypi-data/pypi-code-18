# Copyright (c) 2017 Massimo Mund <massimo.mund@lancode.de>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import setuptools

setuptools.setup(
    name="gitant",
    version='0.0.1',
    author="Massimo Mund",
    author_email="massimo.mund@lancode.de",
    url="https://github.com/masmu/gitant/",
    description="Gather essential git information",
    long_description="Gather essential git repository information, not relying on git binarys",
    packages=setuptools.find_packages(),
    license="GPLv3",
    platforms="Debian GNU/Linux",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[
    ],
)
