from Acquisition import aq_parent
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import json


class GeneratePathbar(BrowserView):

    def __call__(self):
        mtool = getToolByName(self.context, 'portal_membership')
        originpoint = self.request.get('origin', None)
        if not originpoint:
            obj = self.context.context
        else:
            obj = self.context.context.unrestrictedTraverse(
                originpoint.encode("utf8"))
        results = []
        while True:
            clickable = mtool.checkPermission('View', obj)
            results.insert(0, {'title': obj.Title(),
                               'path': '/'.join(obj.getPhysicalPath()),
                               'clickable': clickable})
            if IPloneSiteRoot.providedBy(obj):
                break
            else:
                obj = aq_parent(obj)
        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(results)
