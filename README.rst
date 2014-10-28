=====================
ckanext-tsbsatellites
=====================

Installation and setup
======================

* Install CKAN 2.2 via package install in the web server

* Install Postgres and Solr 4 in the DB server. There is an Ansible script
  for installing Solr 4 in ``deployment/solr``, which also sets up the custom
  schema.

* Install `ckanext-spatial`_, including setting up PostGIS in the database
  as described in the documentation.

* Install `ckanext-harvest`_, using the Redis backend (note that you need to
  ``pip install redis`` in your virtualenv

* Install `ckanext-tsbsatellites`

* Add the following options to the configuration file, apart from the usual ones::

    ckan.plugins = spatial_metadata spatial_query harvest csw_harvester tsbsatellites

    ckan.harvest.mq.type = redis

    ckanext.spatial.search_backend = solr
    ckanext.spatial.harvest.continue_on_validation_errors=True

* TODO: Set up Solr 4 and enable the Solr backend on the spatial search

.. _ckanext-spatial: http://ckanext-spatial.readthedocs.org/en/latest/install.html
.. _ckanext-harvest: https://github.com/ckan/ckanext-harvest#installation


GeoNetwork
==========

Install
-------

GeoNetwork is installed with the Ansible script located at
``deployment/geonetwork``. This will install GeoNetwork 2.10.3 using
PostgreSQL 9.1 and PostGIS 1.5 as database backend. It has been tested on
Ubuntu 12.04 64bit.

After the installation is completed, GeoNetwork should be accessible at

http://server:8080/geonetwork

Immediately after the install please follow the first step in the next section
to change the default password.

Setup
-----

* Change the default admin password
  Login using the input fields located at the top right corner (user
  `admin`, password `admin`). Click on `Administration` on the top left corner
  menu. Go to `Users and groups` > `Change password`.

* System configuration. On the `Administration` page, go to `Catalogue Settings`
  > `System configuration`. Change the following settings:

  - Site identifier, name and organization
  - Server host
  - Enable the INSPIRE setting and INSPIRE views

* CSW configuration. On the `Administration` page, go to `Catalogue Settings`
  > `CSW configuration`. Set the relevant fields, which will be shown on the
  ``GetCapabilities`` response for the CSW service.

* Add the metadata template
    - On the `Administration` page, under `Metadata & Template` select
      `iso19139` from the `Add templates and samples` list box, and click
      `Add templates`


Adding Metadata
---------------

To add metadata you must be logged in to the GeoNetwork instance. Click on
`Administration` on the top left corner menu.

* To import an existing metadata file, go to `Import, export & harvesting` >
  `Metadata insert`. Select the XML file and leave all other options as
  default.

* To create a new metadata record, go to `Metadata & Template` >
  `New metadata`.

  - Select the `(iso19139) Template for Raster data in ISO19139` template.
    If you can not see this template, refer to the previous *Setup* section
    for instructions on how to load it.
  - Once the form is presented, make sure to select the `ISO All` option on
    the left menu, as all the fields required on the Catapult metadata
    schema are not present in the default view presented by GeoNetwork:

    .. image:: http://i.imgur.com/Ba9aBtp.png

  - Be aware that you may need to expand some sections to show a particular
    field. For example, to enter the text description of the geographical
    extent the following needs to be expanded:

    .. image:: http://i.imgur.com/mx8dQJu.png?1

  - When finished, click on `Save` or `Save and Close`.



Accessing the machines
======================

Add the following to your .ssh/config::
  
  Host s* !s*.okserver.org
      Hostname %h.okserver.org
      User <your username>
  Host tsb-web-staging
      Hostname 185.30.10.28
      User <your username>
      ProxyCommand ssh s084 netcat -w 120 %h %p
  Host tsb-db-staging
      Hostname 172.16.0.15
      User <your username>
      ProxyCommand ssh tsb-web-staging netcat -w 120 %h %p
  Host tsb-web-prod
      Hostname 172.16.0.14
      User <your username>
      ProxyCommand ssh tsb-web-staging netcat -w 120 %h %p
  Host tsb-db-prod
      Hostname 172.16.0.13
      User <your username>
      ProxyCommand ssh tsb-web-staging netcat -w 120 %h %p

Now `ssh tsb-web-staging` to access the machines.
