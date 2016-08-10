from Products.Five import BrowserView
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Acquisition import aq_parent
import json


class GeneratePathbar(BrowserView):

    def __call__(self):
        originpoint = self.context.REQUEST['POST']['origin']

        obj = self.context.unrestrictedTraverse(originpoint)
        results = []

        while True:
            results.insert(0, {'title': obj.Title(), 'url': obj.absolute_url()})
            if IPloneSiteRoot.providedBy(obj):
                break
            else:
                obj = aq_parent(obj)
        return json.dumps(results)
