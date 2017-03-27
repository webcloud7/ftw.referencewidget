from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource
from zope.interface import implements
from ftw.referencewidget.browser.utils import get_selectable_types_by_source


def default_filter(source, value):
    return value.portal_type in get_selectable_types_by_source(source)


class ReferenceWidgetPathSource(object):

    implements(ISource)

    def __init__(self, context, filter_method, selectable, nonselectable,
                 override, allow_nonsearched_types):
        self.context = context
        self.filter_method = filter_method
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.override = override
        self.allow_nonsearched_types = allow_nonsearched_types

    def __contains__(self, value):
        return self.filter_method(source=self, value=value)


class ReferenceWidgetPathSourceBinder(object):
    implements(IContextSourceBinder)

    def __init__(self,
                 filter_method=None,
                 selectable=None,
                 nonselectable=None,
                 override=None,
                 allow_nonsearched_types=None):
        self.filter_method = filter_method or default_filter
        self.selectable = selectable or []
        self.nonselectable = nonselectable or []
        self.override = override or False
        self.allow_nonsearched_types = allow_nonsearched_types or False

    def __call__(self, context):
        return ReferenceWidgetPathSource(context,
                                         self.filter_method,
                                         self.selectable,
                                         self.nonselectable,
                                         self.override,
                                         self.allow_nonsearched_types)
