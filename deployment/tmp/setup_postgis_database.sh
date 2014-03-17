#!/bin/sh

# Setup PostGIS
sudo -u postgres psql -d {{ ckan_db }} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
sudo -u postgres psql -d {{ ckan_db }} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
sudo -u postgres psql -d {{ ckan_db }} -c 'ALTER TABLE geometry_columns OWNER TO {{ ckan_user }}'
sudo -u postgres psql -d {{ ckan_db }} -c 'ALTER TABLE spatial_ref_sys OWNER TO {{ ckan_user }}'
