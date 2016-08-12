from Products.Five import BrowserView
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Acquisition import aq_parent
import json


class GeneratePathbar(BrowserView):

    def __call__(self):
        originpoint = self.request.get('origin', None)
        if not originpoint:
            obj = self.context.context
        else:
            obj = self.context.context.unrestrictedTraverse(originpoint.encode("utf8"))
        results = []
        while True:
            results.insert(0, {'title': obj.Title(), 'path': '/'.join(obj.getPhysicalPath())})
            if IPloneSiteRoot.providedBy(obj):
                break
            else:
                obj = aq_parent(obj)
        return json.dumps(results)
