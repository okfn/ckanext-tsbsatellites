#!/bin/sh

# Setup PostGIS
sudo -u postgres psql -d geonetwork -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
sudo -u postgres psql -d geonetwork -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
sudo -u postgres psql -d geonetwork -c 'ALTER TABLE geometry_columns OWNER TO geonetwork'
sudo -u postgres psql -d geonetwork -c 'ALTER TABLE spatial_ref_sys OWNER TO geonetwork'

# Setup GeoNetwork
sudo -u postgres psql -d geonetwork -f /var/lib/tomcat7/webapps/geonetwork/WEB-INF/classes/setup/sql/create/create-db-postgis.sql
sudo -u postgres psql -d geonetwork -f /var/lib/tomcat7/webapps/geonetwork/WEB-INF/classes/setup/sql/data/data-db-default.sql
sudo -u postgres psql -d geonetwork -f /var/lib/tomcat7/webapps/geonetwork/WEB-INF/classes/setup/sql/data/loc-eng-default.sql
sudo -u postgres psql -d geonetwork -c 'GRANT ALL PRIVILEGES ON DATABASE geonetwork TO "geonetwork"'
sudo -u postgres psql -d geonetwork -c 'GRANT ALL PRIVILEGES ON SCHEMA public TO "geonetwork"'
sudo -u postgres psql -d geonetwork -c 'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "geonetwork"'
sudo -u postgres psql -d geonetwork -c 'GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "geonetwork"'


