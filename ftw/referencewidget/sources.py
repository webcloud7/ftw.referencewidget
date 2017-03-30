from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource
from zope.interface import implements
from ftw.referencewidget.browser.utils import get_selectable_types_by_source


def default_filter(source, value):
    """"
    Return ``True`` when the object is selectable, ``False``
    when it is not selectable.

    """

    return value.portal_type in get_selectable_types_by_source(source)


class ReferenceObjPathSource(object):

    implements(ISource)

    def __init__(self, context, selectable_function, selectable, nonselectable,
                 override, allow_nonsearched_types):
        self.context = context
        self.selectable_function = selectable_function
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.override = override
        self.allow_nonsearched_types = allow_nonsearched_types

    def __contains__(self, value):
        return self.selectable_function(source=self, value=value)


class ReferenceObjSourceBinder(object):
    implements(IContextSourceBinder)

    def __init__(self,
                 selectable_function=None,
                 selectable=None,
                 nonselectable=None,
                 override=None,
                 allow_nonsearched_types=None):
        self.selectable_function = selectable_function or default_filter
        self.selectable = selectable or []
        self.nonselectable = nonselectable or []
        self.override = override or False
        self.allow_nonsearched_types = allow_nonsearched_types or False

    def __call__(self, context):
        return ReferenceObjPathSource(context,
                                      self.selectable_function,
                                      self.selectable,
                                      self.nonselectable,
                                      self.override,
                                      self.allow_nonsearched_types)
