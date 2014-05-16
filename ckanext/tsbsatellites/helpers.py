import ckan.plugins as p


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
