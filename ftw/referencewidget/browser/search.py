from ftw.referencewidget.browser.utils import get_selectable_types
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import json


class SearchView(BrowserView):

    def __call__(self):
        search_term = self.request.get('term')
        if not search_term:
            return json.dumps([])

        if not search_term.endswith("*"):
            search_term += "*"
        search_types = get_selectable_types(self.context)

        query = {'portal_types': search_types, 'Title': search_term}
        catalog = getToolByName(self.context.context, 'portal_catalog')
        results = catalog(query)
        json_prep = []

        for item in results:
            label = '{0} ({1})'.format(item.Title, item.getPath())
            json_prep.append({'label': label, 'value': item.getPath()})

        return json.dumps(json_prep)
