from ftw.referencewidget.browser.utils import get_selectable_types_by_source
from plone import api
from zope.interface import implements
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import ISource


def default_filter(source, value):
    """"
    Return ``True`` when the object is selectable, ``False``
    when it is not selectable.

    """
    valid_type = value.portal_type in get_selectable_types_by_source(source)

    valid_path = True
    if source.root_path:
        path = '/'.join(value.getPhysicalPath())
        valid_path = path.startswith(source.root_path)

    return valid_type and valid_path


class ReferenceObjPathSource(object):

    implements(ISource)

    def __init__(self, context, selectable_function, selectable, nonselectable,
                 override, allow_nonsearched_types, root_path):
        self.context = context
        self.selectable_function = selectable_function
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.override = override
        self.allow_nonsearched_types = allow_nonsearched_types
        self.root_path = root_path

    def __contains__(self, value):
        return self.selectable_function(source=self, value=value)


class ReferenceObjSourceBinder(object):
    implements(IContextSourceBinder)

    def __init__(self,
                 selectable_function=None,
                 selectable=None,
                 nonselectable=None,
                 override=None,
                 allow_nonsearched_types=None,
                 root_path=None):
        self.selectable_function = selectable_function or default_filter
        self.selectable = selectable or []
        self.nonselectable = nonselectable or []
        self.override = override or False
        self.allow_nonsearched_types = allow_nonsearched_types or False
        self.root_path = root_path

    def __call__(self, context):
        self.context = context
        return ReferenceObjPathSource(context,
                                      self.selectable_function,
                                      self.selectable,
                                      self.nonselectable,
                                      self.override,
                                      self.allow_nonsearched_types,
                                      self._get_root_path())

    def _get_root_path(self):
        if callable(self.root_path):
            return self.root_path(self.context)
        elif isinstance(self.root_path, basestring):
            portal_path = '/'.join(api.portal.get().getPhysicalPath())
            return portal_path + self.root_path
        else:
            return None
