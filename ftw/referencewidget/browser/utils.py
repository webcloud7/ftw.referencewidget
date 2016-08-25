from Acquisition import aq_parent
from ftw.referencewidget.interfaces import IReferenceSettings
from plone.api import portal
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility


def get_traversal_types(widget):
    if widget.override:
        return widget.allow_traversal

    registry = getUtility(IRegistry)
    referencesettings = registry.forInterface(IReferenceSettings)
    portal_props = getToolByName(widget.context, 'portal_properties')
    non_selectable = set()
    if not widget.allow_nonsearched_types:
        non_selectable = set(portal_props.site_properties.types_not_searched)
    non_selectable = non_selectable.union(
        set(referencesettings.block_traversal_additional))

    non_selectable = non_selectable.difference(
        set(referencesettings.traverse_additional))

    non_selectable = non_selectable.union(set(widget.block_traversal))
    non_selectable = non_selectable.difference(set(widget.allow_traversal))
    return remove_blacklist_from_types(widget, non_selectable)


def remove_blacklist_from_types(widget, blacklist):
    portal_types = getToolByName(widget.context, 'portal_types')
    types_to_search = portal_types.keys()
    for item in blacklist:
        if portal_types.get(item):
            types_to_search.remove(item)
    return types_to_search


def get_selectable_types(widget):
    if widget.override:
        return widget.selectable

    registry = getUtility(IRegistry)
    referencesettings = registry.forInterface(IReferenceSettings)
    portal_props = getToolByName(widget.context, 'portal_properties')
    non_selectable = set()
    if not widget.allow_nonsearched_types:
        non_selectable = set(portal_props.site_properties.types_not_searched)
    non_selectable = non_selectable.union(
        set(referencesettings.block_additional))
    non_selectable = non_selectable.difference(
        set(referencesettings.select_additional))

    non_selectable = non_selectable.union(set(widget.nonselectable))
    non_selectable = non_selectable.difference(set(widget.selectable))
    return remove_blacklist_from_types(widget, non_selectable)


def get_path_from_widget_start(widget):
    effective_path = ""
    if not callable(widget.start):
        start = widget.start
        if (start == "parent"):
            obj = aq_parent(widget.context)
            effective_path = '/'.join(obj.getPhysicalPath())
        elif (start == "navroot"):
            obj = portal.get_navigation_root(widget.context)
            effective_path = '/'.join(obj.getPhysicalPath())
        elif (start == "ploneroot"):
            obj = portal.get()
            effective_path = '/'.join(obj.getPhysicalPath())
        else:
            effective_path = widget.start
    else:
        effective_path = widget.start()
    return effective_path
