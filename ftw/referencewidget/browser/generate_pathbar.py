from Acquisition import aq_parent
from ftw.referencewidget.browser.utils import get_path_from_widget_start
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
import json


class GeneratePathbar(BrowserView):

    def __call__(self):
        widget = self.context
        mtool = getToolByName(widget.context, 'portal_membership')
        originpoint = self.request.get('origin', None)
        obj = None
        first = True
        if not originpoint:
            if widget.start:
                obj = widget.context.unrestrictedTraverse(
                    get_path_from_widget_start(widget))
            else:
                obj = self.context.context
        else:
            obj = self.context.context.unrestrictedTraverse(
                originpoint.encode("utf8"))
        results = []
        while True:
            clickable = mtool.checkPermission('View', obj)
            results.insert(0, {'title': obj.Title(),
                               'path': '/'.join(obj.getPhysicalPath()),
                               'clickable': str(clickable and not first)})
            first = False
            if IPloneSiteRoot.providedBy(obj):
                break
            else:
                obj = aq_parent(obj)
        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(results)
