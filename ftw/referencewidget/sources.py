from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource
from zope.interface import implements
from ftw.referencewidget.browser.utils import get_selectable_types


class ReferenceWidgetPathSource(object):

    implements(ISource)

    def __init__(self, context, selectable, nonselectable, override):
        self.context = context

    def __contains__(self, value):
        obj = self._get_obj_by_path(value)
        if not obj:
            return False
        return obj.portal_type in get_selectable_types(self)

    def _get_obj_by_path(self, value):
        return self.context.restrictedTraverse(value, None)


class ReferenceWidgetPathSourceBinder(object):
    implements(IContextSourceBinder)

    def __init__(self, selectable=None,
                 nonselectable=None,
                 override=None):
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.override = override

    def __call__(self, context):
        return ReferenceWidgetPathSource(context,
                                         self.selectable,
                                         self.nonselectable,
                                         self.override)
