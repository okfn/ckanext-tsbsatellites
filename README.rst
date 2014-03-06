=====================
ckanext-tsbsatellites
=====================

TODO


GeoNetwork
==========

Install
-------

GeoNetwork is installed with the Ansible script located at
``deployment/geonetwork``. This will install GeoNetwork 2.10.3 using
PostgreSQL 9.1 as database backend.

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
