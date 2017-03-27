from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource
from zope.interface import implements
from ftw.referencewidget.browser.utils import get_selectable_types_by_source


class ReferenceWidgetPathSource(object):

    implements(ISource)

    def __init__(self, context, selectable, nonselectable, override,
                 allow_nonsearched_types):
        self.context = context
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.override = override
        self.allow_nonsearched_types = allow_nonsearched_types

    def __contains__(self, value):
        return value.portal_type in get_selectable_types_by_source(self)


class ReferenceWidgetPathSourceBinder(object):
    implements(IContextSourceBinder)

    def __init__(self, selectable=None,
                 nonselectable=None,
                 override=None,
                 allow_nonsearched_types=None):
        self.selectable = selectable or []
        self.nonselectable = nonselectable or []
        self.override = override or False
        self.allow_nonsearched_types = allow_nonsearched_types or False

    def __call__(self, context):
        return ReferenceWidgetPathSource(context,
                                         self.selectable,
                                         self.nonselectable,
                                         self.override,
                                         self.allow_nonsearched_types)
