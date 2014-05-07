import ckan.plugins as p
import ckan.plugins.toolkit as tk
import json

class SearchAutocomplete(tk.BaseController):

    def autocomplete(self):
        data = [
            { "label": "annhhx10", "category": "" },
            { "label": "annk K12", "category": "" },
            { "label": "annttop C13", "category": "" },
            { "label": "anders andersson", "category": "History" },
            { "label": "andreas andersson", "category": "History" },
            { "label": "andreas johnson", "category": "History" },
        ];
        tk.response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return json.dumps(data)
