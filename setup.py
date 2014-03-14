from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
    name='ckanext-tsbsatellites',
    version=version,
    description="CKAN customizations for the Catapult Satellites Data Catalog",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='CKAN team at Open Knowledge',
    author_email='info@ckan.org',
    url='http://ckan.org',
    license='AGPL v3.0',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.tsbsatellites'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        tsbsatellites=ckanext.tsbsatellites.plugin:TSBSatellitesPlugin
    ''',
)
