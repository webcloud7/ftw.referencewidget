from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five import BrowserView
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.schema import List
import json


class GeneratePathbar(BrowserView):

    def __call__(self):
        widget = self.context
        mtool = getToolByName(widget.context, 'portal_membership')

        originpoint = self.request.get('origin', None)
        if not originpoint:
            originpoint = widget.get_start_path()

        if isinstance(originpoint, unicode):
            originpoint = originpoint.encode('utf-8')

        obj = widget.context.unrestrictedTraverse(originpoint)
        results = []

        root_path = self._get_path_from_source(widget.field)

        while True:
            clickable = mtool.checkPermission('View', obj)
            path = '/'.join(obj.getPhysicalPath())
            results.insert(0, {'title': obj.Title(),
                               'path': path,
                               'clickable': bool(clickable)})

            if root_path and root_path == path:
                break
            elif IPloneSiteRoot.providedBy(obj):
                break
            else:
                obj = aq_parent(obj)
        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(results)

    def _get_path_from_source(self, field):
        if isinstance(field, RelationList) or isinstance(field, List):
            value_type = getattr(field, 'value_type', None)

            if isinstance(value_type, RelationChoice):
                source = value_type.source(self.context)
                return source.root_path

        elif isinstance(field, RelationChoice):
            source = field.source(self.context)
            return source.root_path

        else:
            return None
