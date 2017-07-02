from distutils.core import setup
# from setuptools import setup

setup(
    name='bgp_visualize',
    version='0.1',
    packages=['bgp_visualize',
              ],
    url='https://github.com/TheNetworker/visualize_bgp_asns',
    license='MIT License',
    author='Bassim',
    author_email='basim.alyy@gmail.com',
    keywords = ['bgp', 'network', 'autonomous system','visualize'],
    description='This package is used to visualize the BGP Autonomous Systems and draw the interconnections between them. Also it colors the operators ASN in each country and the upstreams and downstreams services providers.'
)
