from ftw.referencewidget.browser.utils import get_selectable_types
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import json


class SearchView(BrowserView):

    def __call__(self):
        post = self.request.get('POST', {})
        if "search" not in post.keys():
            return json.dumps([])

        search_term = post['search']
        if not search_term.endswith("*"):
            search_term += "*"
        search_types = get_selectable_types(self.context)

        query = {'portal_types': search_types, 'Title': search_term}
        catalog = getToolByName(self.context.context, 'portal_catalog')
        results = catalog(query)
        json_prep = []

        for item in results:
            json_prep.append({'title': item.Title, 'path': item.getPath()})

        return json.dumps(json_prep)
