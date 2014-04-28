import ckan.plugins as p

from ckanext.spatial.interfaces import ISpatialHarvester

from ckanext.tsbsatellites.iso import CustomISODocument
import ckanext.tsbsatellites.helpers as satellites_helpers

class TSBSatellitesPlugin(p.SingletonPlugin):

    p.implements(ISpatialHarvester, inherit=True)
    p.implements(p.IFacets)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IConfigurer)

    # IConfigurer

    def update_config(self, config):

        p.toolkit.add_template_directory(config, 'theme/templates')
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_resource('theme/resources', 'satellites-theme')

    # ISpatialHarvester

    def get_package_dict(self, context, data_dict):

        package_dict = data_dict['package_dict']
        iso_values = data_dict['iso_values']

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
            ('alternative-title', ['alternative-title']),
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

        # Fields which are not extracted by the default ISO parser
        # (ie not in iso_values), reparse the ISO doc to extract
        # them
        xml_string = data_dict['harvest_object'].content
        custom_iso_values = CustomISODocument(xml_string).read_values()

        for key, custom_iso_keys in [
            ('frequency-of-collection', ['frequency-of-collection']),
            ('frequency-of-collection-units', ['frequency-of-collection-units']),
            ('parameters-measured', ['dimension', 'type']),
            ('sensor-type', ['dimension', 'name']),

        ]:
            package_dict['extras'].append(
                {'key': key, 'value': _get_value(custom_iso_values, custom_iso_keys)}
            )

        # Flatten some fields returned as lists
        for key in ('use-constraints', 'begin-collection_date', 'end-collection_date'):
            for extra in package_dict['extras']:
                if extra['key'] == key and len(extra['value']):
                    extra['value'] = extra['value'][0]

        # Default all resource formats to HTML if no format yet defined
        # We might needed to expanded this some point
        for resource in package_dict.get('resources', []):
            if not resource.get('format'):
                resource['format'] = 'HTML'

        return package_dict

    # IFacets

    def dataset_facets(self, facets_dict, package_type):
        # We will actually remove all the core facets and add our own
        facets_dict.clear()

        facets_dict['topic-category'] = p.toolkit._('Topic Category')
        facets_dict['data-format'] = p.toolkit._('Data Format')
        facets_dict['use-constraints'] = p.toolkit._('Data Cost and Access')

        #TODO: handle these as number / date
        facets_dict['spatial-resolution'] = p.toolkit._('Spatial Resolution')

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
        )
        return _get_module_functions(satellites_helpers, function_names)

def _get_module_functions(module, function_names):
    functions = {}
    for f in function_names:
        functions[f] = module.__dict__[f]

    return functions

