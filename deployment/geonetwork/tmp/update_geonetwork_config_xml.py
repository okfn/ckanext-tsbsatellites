#!/usr/bin/env python

import shutil
from datetime import datetime
import xml.etree.ElementTree as ET

path = '/var/lib/tomcat7/webapps/geonetwork/WEB-INF/config.xml'
shutil.copy(path, path.replace('.xml', '.{0}.xml'.format(datetime.now().isoformat())))

tree = ET.parse(path)
tree.find('.//resources/resource[@enabled="true"]').set('enabled', 'false')
for resource in tree.findall('.//resources/resource'):
    provider = resource.find('provider')
    if provider is not None and provider.text == 'jeeves.resources.dbms.JNDIPool':
        resource.set('enabled', 'true')
        resource.find('config/url').text = 'jdbc:postgresql_postGIS://localhost:5432/geonetwork'

with open(path, 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree.getroot()))
