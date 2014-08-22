import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import datetime
import json
import re

CATEGORIES = [
    {'name': 'biota', 'title': 'Biota', 'short_title': 'Biota'},
    {'name': 'boundaries', 'title': 'Boundaries', 'short_title': 'Boundaries'},
    {'name': 'climatologyMeteorologyAtmosphere', 'title': 'Climatology / Meteorology / Atmosphere', 'short_title': 'Climatology'},
    {'name': 'economy', 'title': 'Economy', 'short_title': 'Economy'},
    {'name': 'elevation', 'title': 'Elevation', 'short_title': 'Elevation'},
    {'name': 'environment', 'title': 'Environment', 'short_title': 'Environment'},
    {'name': 'farming', 'title': 'Farming', 'short_title': 'Farming'},
    {'name': 'geoscientificInformation', 'title': 'Geoscientific information', 'short_title': 'Geoscientific information'},
    {'name': 'health', 'title': 'Health', 'short_title': 'Health'},
    {'name': 'imageryBaseMapsEarthCover', 'title': 'Imagery / Base Maps / Earth Cover', 'short_title': 'Imagery'},
    {'name': 'inlandWaters', 'title': 'Inland Waters', 'short_title': 'Inland Waters'},
    {'name': 'intelligenceMilitary', 'title': 'Intelligence / Military', 'short_title': 'Intelligence'},
    {'name': 'location', 'title': 'Location', 'short_title': 'Location'},
    {'name': 'ocean', 'title': 'Ocean', 'short_title': 'Ocean'},
    {'name': 'planningCadastre', 'title': 'Planning / Cadastre', 'short_title': 'Planning'},
    {'name': 'society', 'title': 'Society', 'short_title': 'Society'},
    {'name': 'structure', 'title': 'Structure', 'short_title': 'Structure'},
    {'name': 'transportation', 'title': 'Transportation', 'short_title': 'Transportation'},
    {'name': 'utilitiesCommunication', 'title': 'Utilities / Communication', 'short_title': 'Utilities'},

    # Custom values, not part of the original vocabulary
    {'name': 'Copernicus', 'title': 'Copernicus', 'short_title': 'Copernicus'},
]


def get_categories():
    '''Return a list of all categories with counts for each one

        Returns a list of dicts, each one as follows::

            {'name': 'intelligenceMilitary',
             'title': 'Intelligence / Military',
             'short_title': 'Intelligence',
             'count': 3}

        These can be used to build the categories selector on the front page
    '''


    # Get counts
    data_dict = {
        'rows': 0,
        'facet.field': ['topic-category'],
    }

    search = p.toolkit.get_action('package_search')({}, data_dict)

    categories = search.get('search_facets', {}) \
                       .get('topic-category', {}) \
                       .get('items')

    if not categories:
        return []

    available_categories = {}
    for category in categories:
        available_categories[category['name']] = category['count']

    all_categories = CATEGORIES
    for category in all_categories:
        category['count'] = (available_categories[category['name']]
                             if category['name'] in available_categories
                             else 0)

    return all_categories

def get_default_slider_values():
    '''Returns the earliest collection date from package_search'''

    data_dict = {
            'sort': 'begin-collection_date asc',
            'rows': 1,
            'q': 'begin-collection_date:[* TO *]',
    }
    result = p.toolkit.get_action('package_search')({}, data_dict)['results']
    if len(result) == 1:
        date = filter(lambda x: x['key'] == 'begin-collection_date',
                result[0].get('extras', []))
        begin = date[0]['value']
    else:
        begin = datetime.date.today().isoformat()

    data_dict = {
            'sort': 'end-collection_date desc',
            'rows': 1,
            'q': 'end-collection_date:[* TO *]',
    }
    result = p.toolkit.get_action('package_search')({}, data_dict)['results']
    if len(result) == 1:
        date = filter(lambda x: x['key'] == 'end-collection_date',
                result[0].get('extras', []))
        end = date[0]['value']
    else:
        end = datetime.date.today().isoformat()
    return begin, end

def format_data_costs(package):
    data = h.get_pkg_dict_extra(package, 'access_constraints')
    data_list = json.loads(data)
    return ', '.join(data_list)

def format_frequency(package):
    freq = h.get_pkg_dict_extra(package, 'frequency-of-collection')
    unit = h.get_pkg_dict_extra(package, 'frequency-of-collection-units')
    # Remove the surrounding curly braces from both the strings
    freq_num = run_format_regex(freq)
    freq_float = None
    try:
        freq_int = int(freq_num)
    except ValueError:
        freq_float = float(freq_num)
    # Most values are ints, but some are floats and some of these floats are
    # just the same number as the int. This complicated and ugly logic makes
    # sure floats are used *only* when needed.
    if freq_float is not None:
        if freq_float == int(freq_float):
            freq_num = int(freq_float)
        else:
            freq_num = freq_float
    else:
        freq_num = freq_int
    unit_str = run_format_regex(unit)
    if freq_num > 0:
        unit_str = '{0}s'.format(unit_str)
    return '{0} {1}'.format(freq_num, unit_str)

def run_format_regex(string):
    r = re.compile('{(.*)}')
    return r.match(string).group(1)

def get_date_url_param():
    params = ['', '']
    for k, v in tk.request.params.items():
        if k == 'ext_begin_date':
            params[0] = v
        elif k == 'ext_end_date':
            params[1] = v
        else:
            continue
    return params

def remove_public(item):
    '''
    Function to remove "Public - " from the labels for search facet.
    '''
    if item['display_name'].startswith('Public - '):
         item['display_name'] = item['display_name'][9:]
    return h.truncate(item['display_name'], 22)
