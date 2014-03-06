#!/usr/bin/env python

import sys
import shutil
from datetime import datetime
import xml.etree.ElementTree as ET

path = '/var/lib/tomcat7/webapps/geonetwork/WEB-INF/config.xml'
path = 'config.xml'
shutil.copy(path, path.replace('.xml', '.{0}.xml'.format(datetime.now().isoformat())))

tree = ET.parse(path)
tree.find('.//resources/resource[@enabled="true"]').set('enabled', 'false')
for resource in tree.findall('.//resources/resource'):
    driver = resource.find('config/driver')
    if driver is not None and driver.text == 'org.postgresql.Driver':
        resource.set('enabled', 'true')
        resource.find('config/user').text = 'geonetwork'
        resource.find('config/password').text = sys.argv[1]
        resource.find('config/url').text = 'jdbc:postgresql://localhost:5432/geonetwork'

with open(path + '2', 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree.getroot()))
