from datetime import datetime
import json
import logging
import re
from routes.mapper import SubMapper

import ckan.plugins as p

from ckanext.spatial.interfaces import ISpatialHarvester
from ckanext.tsbsatellites.iso import CustomISODocument
import ckanext.tsbsatellites.helpers as satellites_helpers

log = logging.getLogger(__name__)

def _sanitize_org_name(name):

    # Convert spaces and separators to hyphens
    name = re.sub('[ .:/]', '-', name.strip())

    # Remove non-allowed characters and lower-case
    name = re.sub('[^a-zA-Z0-9-_]', '', name).lower()

    # Pad with extra characters if too small
    if len(name) < 3:
        name += '_' * (3 - len(name))

    return name

class TSBSatellitesPlugin(p.SingletonPlugin):

    p.implements(ISpatialHarvester, inherit=True)
    p.implements(p.IFacets)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IConfigurer)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.IRoutes, inherit=True)


    _site_user = None


    # IConfigurer

    def update_config(self, config):

        p.toolkit.add_template_directory(config, 'theme/templates')
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_resource('theme/resources', 'satellites-theme')

    # IPackageController

    def before_index(self, data_dict):

        data_dict['topic-category'] = json.loads(data_dict.get('topic-category', '[]'))

        # Format facets
        data_dict['topic-category_facets'] = []
        for category in data_dict['topic-category']:
            for category_def in satellites_helpers.CATEGORIES:
                if category_def['name'] == category:
                    data_dict['topic-category_facets'].append(category_def['title'])

        # Do not index the collection date fields if the date is null
        # This should be fixed in core in ckan/ckan#1701
        package_dict = json.loads(data_dict['data_dict'])
        for field in ('begin-collection_date', 'end-collection_date',):
            for extra in package_dict.get('extras', []):
                if extra['key'] == field and not extra['value']:
                    data_dict.pop(field, None)

        return data_dict

    def before_search(self, search_params):

        def parse_date(date_string):
            '''
            Parse a date string or throw a nice error into the log. Re-raises
            the error for the plugin to catch.
            '''
            try:
                return datetime.strptime(date_string, '%Y-%m-%d')
            except ValueError as e:
                log.debug('Date {0} not in the right format. Needs to be YYYY'
                          '-MM-DD'.format(date_string))
                raise e

        if (search_params.get('extras', None) and 'ext_begin_date' in
                search_params['extras'] and 'ext_end_date' in
                search_params['extras']):
            try:
                begin = parse_date(search_params['extras']['ext_begin_date'])
                end = parse_date(search_params['extras']['ext_end_date'])
            except ValueError:
                return search_params
            # Adding 'Z' manually here is evil, but we do this in core too.
            query = ("begin-collection_date:[{0}Z TO {1}Z] AND "
                    "end-collection_date:[{0}Z TO {1}Z]")
            query = query.format(begin.isoformat(), end.isoformat())
            search_params['q'] = query

        return search_params

    # ISpatialHarvester

    def get_package_dict(self, context, data_dict):

        package_dict = data_dict['package_dict']
        iso_values = data_dict['iso_values']
        xml_tree = data_dict['xml_tree']

        def _get_value(d, keys):
            key = keys.pop(0)
            value = d.get(key)
            if isinstance(value, dict) and len(keys):
                return _get_value(value, keys)
            elif isinstance(value, list) and len(value) and len(keys):
                return _get_value(value[0], keys)
            elif isinstance(value, list) and len(value) and len(keys) == 0:
                return value
            else:
                return value or ''

        def _get_extra(package_dict, key):
            for extra in package_dict.get('extras', []):
                if extra['key'] == key:
                    return extra['value']

        # These values are extracted by the ISO parser but not added to the
        # package_dict by default
        for key, iso_keys in [
            ('topic-category', ['topic-category']),
            ('spatial-resolution', ['spatial-resolution']),
            ('use-constraints', ['limitations-on-public-access']),
            ('alternate-title', ['alternate-title']),
            ('purpose', ['purpose']),
            ('lineage', ['lineage']),
            ('additional-information-source', ['additional-information-source']),
            ('applications', ['usage','usage']),
            ('distributor-email', ['distributor', 'contact-info', 'email']),
            ('data-format', ['data-format', 'name']),

            # Copy the temporal extent so it can be indexed as date
            ('begin-collection_date', ['temporal-extent-begin']),
            ('end-collection_date', ['temporal-extent-end']),

        ]:
            package_dict['extras'].append(
                {'key': key, 'value': _get_value(iso_values, iso_keys)}
            )

        # Add extra elements to Topic Category that are not part of the
        # vocabulary (eg a tag)
        tags_to_include = ['Copernicus']
        tags_present = []
        for tag in package_dict.get('tags', []):
            if tag['name'] in tags_to_include:
                tags_present.append(tag['name'])
        for extra in package_dict['extras']:
            if extra['key'] == 'topic-category':
                extra['value'].extend(tags_present)

        # Fields which are not extracted by the default ISO parser
        # (ie not in iso_values), reparse the ISO doc to extract
        # them
        custom_iso_values = CustomISODocument(xml_tree=xml_tree).read_values()

        for key, custom_iso_keys in [
            ('frequency-of-collection', ['frequency-of-collection']),
            ('frequency-of-collection-units', ['frequency-of-collection-units']),
            ('parameters-measured', ['dimension', 'name']),
            ('sensor-type', ['dimension', 'type']),

        ]:
            package_dict['extras'].append(
                {'key': key, 'value': _get_value(custom_iso_values, custom_iso_keys)}
            )

        # Flatten some single-value fields returned as lists
        for key in ('use-constraints', 'begin-collection_date',
                'end-collection_date', 'alternate-title'):
            for extra in package_dict['extras']:
                if extra['key'] == key and len(extra['value']):
                    extra['value'] = extra['value'][0]

        # Dump some fields returned as lists as JSON
        for key in ('topic-category',):
            for extra in package_dict['extras']:
                if extra['key'] == key:
                    extra['value'] = json.dumps(extra['value'])

        # Default all resource formats to HTML if no format yet defined
        # We might needed to expanded this some point
        for resource in package_dict.get('resources', []):
            if not resource.get('format'):
                resource['format'] = 'HTML'

        # Extract organizations from the ResponsibleParty ISO values, check if
        # it exists and create it otherwise
        responsible_party = iso_values.get('responsible-organisation', [{}])[0]
        responsible_party_name = responsible_party.get('organisation-name',
                                    responsible_party.get('individual-name'))
        if not responsible_party_name:
            log.error('No organization defined for dataset {0}'.format(package_dict['name']))
            return None
        else:
            org_name = _sanitize_org_name(responsible_party_name)
            try:
                org_dict = p.toolkit.get_action('organization_show')({}, {'id': org_name})
                package_dict['owner_org'] = org_dict['id']
                log.debug('Organization exists, assigning dataset {0} to org {1}'.format(
                          package_dict['name'], org_dict['name']))

            except p.toolkit.ObjectNotFound:

                contact_info = responsible_party.get('contact-info', {})
                org_url = contact_info.get('online-resource').get('url') if contact_info.get('online-resource') else None

                data_dict = {
                    'name': org_name,
                    'title': responsible_party_name,
                    'extras': [
                        {'key': 'url', 'value': org_url},
                        {'key': 'email', 'value': contact_info.get('email')},
                    ]
                }

                org_dict = p.toolkit.get_action('organization_create')(context, data_dict)
                package_dict['owner_org'] = org_dict['id']
                log.debug('New organization created, assigning dataset {0} to org {1}'.format(
                          package_dict['name'], org_dict['name']))

        return package_dict

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        # We will actually remove all the core facets and add our own
        facets_dict.clear()

        facets_dict['topic-category_facets'] = p.toolkit._('Topic Category')
        facets_dict['data-format'] = p.toolkit._('Data Format')
        facets_dict['use-constraints'] = p.toolkit._('Data Cost and Access')

        #TODO: handle these as number / date
        facets_dict['spatial-resolution'] = p.toolkit._('Spatial Resolution (meters)')

        facets_dict['begin-collection_date'] = p.toolkit._('Date of Collection')

        return facets_dict

    def group_facets(self, facets_dict, group_type, package_type):
        facets_dict.clear()
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):
        facets_dict.clear()
        return facets_dict

    # ITemplateHelpers

    def get_helpers(self):

        function_names = (
            'get_categories',
            'get_default_slider_values',
            'format_data_costs',
            'format_frequency',
            'get_date_url_param',
            'remove_public',
        )
        return _get_module_functions(satellites_helpers, function_names)

    #IRoutes

    def before_map(self, map):

        map.connect('autcomplete_search', '/api/util/search',
            controller='ckanext.tsbsatellites.controllers:SearchAutocomplete',
            action='autocomplete')

        # Use publishers instead of orgs in the URLs

        map.redirect('/group/{url:.*}', '/publisher/{url}',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/group', '/publisher',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/organization/{url:.*}', '/publisher/{url}',
                     _redirect_code='301 Moved Permanently')
        map.redirect('/organization', '/publisher',
                     _redirect_code='301 Moved Permanently')

        map.redirect('/publishers', '/publisher')
        map.redirect('/publishers/{url:.*}', '/publisher/{url}')

        org_controller = 'ckan.controllers.organization:OrganizationController'
        with SubMapper(map, controller=org_controller) as m:
            m.connect('publishers_index', '/publisher', action='index')
            m.connect('/publisher/list', action='list')
            m.connect('/publisher/new', action='new')
            m.connect('/publisher/{action}/{id}',
                      requirements=dict(action='|'.join([
                          'delete',
                          'admins',
                          'member_new',
                          'member_delete',
                          'history'
                      ])))
            m.connect('publisher_activity', '/publisher/activity/{id}/0',
                      action='activity', ckan_icon='time')
            m.connect('publisher_read', '/publisher/{id}', action='read')
            m.connect('publisher_about', '/publisher/about/{id}',
                      action='about', ckan_icon='info-sign')
            m.connect('publisher_read', '/publisher/{id}', action='read',
                      ckan_icon='sitemap')
            m.connect('publisher_edit', '/publisher/edit/{id}',
                      action='edit', ckan_icon='edit')
            m.connect('publisher_members', '/publisher/members/{id}',
                      action='members', ckan_icon='group')
            m.connect('publisher_bulk_process',
                      '/publisher/bulk_process/{id}',
                      action='bulk_process', ckan_icon='sitemap')

        map.redirect('/api/{ver:1|2|3}/rest/publisher',
                     '/api/{ver}/rest/group')
        map.redirect('/api/rest/publisher', '/api/rest/group')
        map.redirect('/api/{ver:1|2|3}/rest/publisher/{url:.*}',
                     '/api/{ver}/rest/group/{url:.*}')
        map.redirect('/api/rest/publisher/{url:.*}',
                     '/api/rest/group/{url:.*}')


        return map


def _get_module_functions(module, function_names):
    functions = {}
    for f in function_names:
        functions[f] = module.__dict__[f]

    return functions

