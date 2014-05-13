import ckan.model
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import json

class SearchAutocomplete(tk.BaseController):

    def autocomplete(self):
        term = tk.request.GET.get('term')
        context = {'model': ckan.model, 'user': tk.c.user}
        data = []
        search_results = tk.get_action('package_search')(context, {'q': term})
        search_dict = map(lambda x: {'label': x['title']},
                          search_results['results'])
        data.extend(search_dict)
        if tk.c.user:
            history = tk.get_action('search_history_list')(context, {})
            history_list = [{'label': x['params']['q'], 'category': 'history'}
                            for x in history]
            history_list = filter(lambda x: term.lower() in x['label'].lower(),
                                  history_list)
            data.extend(history_list)
        tk.response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return json.dumps(data)
