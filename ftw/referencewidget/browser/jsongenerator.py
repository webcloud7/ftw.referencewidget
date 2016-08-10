from ftw.referencewidget.interfaces import IReferenceSettings
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component import getUtility
import json


class ReferenceJsonEndpoint(BrowserView):

    def __call__(self):
        widget = self.context
        if 'start' in widget.REQUEST['POST'].keys():
            effective_path = widget.REQUEST['POST']['start']
            effective_context = widget.unrestrictedTraverse(effective_path)
        elif not widget.start:
            effective_context = widget.form.context
        else:
            effective_context = widget.unrestrictedTraverse(widget.start)

        current_depth = len(effective_context.getPhysicalPath())

        query = {'portal_type': self.get_traversal_types(),
                 'query': {'path': '/'.join(effective_context.getPhysicalPath()),
                           'depth': 2},
                 'is_folderish': True
                 }
        catalog = getToolByName(self.context, 'portal_catalog')
        results_folderish = catalog(query)

        selectable_types = self.get_selectable_types()
        query = {'portal_type': selectable_types,
                 'query': {'path': '/'.join(effective_context.getPhysicalPath()),
                           'depth': 2},
                 'is_folderish': False
                 }

        results_content = catalog(query)

        results = results_folderish.extend(results_content)
        result = {}
        for item in results:
            obj_dict = {'path': item.getPath(),
                        'id': item.id,
                        'title': item.Title,
                        'folderish': item.is_folderish,
                        'selectable': item.portal_type in selectable_types,
                        'children': {}}
            depth = len(item.getPath().split('/')) - current_depth

            if depth == 1:
                result[item.id] = obj_dict
            else:
                phys_path = item.getPath().split('/')
                parent = result[phys_path[current_depth]]
                for counter in range(1, depth - 1):
                    parent = parent['children'][phys_path[current_depth + counter]]
                parent['children'][item.id] = obj_dict
        return json.dumps(result)

    def get_traversal_types(self, widget):
        if widget.override:
            return widget.allow_traversal

        registry = getUtility(IRegistry)
        referencesettings = registry.forInterface(IReferenceSettings)
        portal_props = getToolByName(self.context, 'portal_properties')

        non_selectable = set(portal_props.site_properties.types_not_searched)
        non_selectable = non_selectable.union(
            set(referencesettings.block_traversal_additional))

        non_selectable = non_selectable.difference(
            set(referencesettings.traverse_additional))

        non_selectable = non_selectable.union(set(widget.block_traversal))
        non_selectable = non_selectable.difference(set(widget.allow_traversal))
        return self.remove_blacklist_from_types(non_selectable)

    def remove_blacklist_from_types(self, blacklist):
        portal_types = getToolByName(self.context, 'portal_types')
        types_to_search = portal_types.keys()
        for item in blacklist:
            if portal_types.get(item):
                types_to_search.remove(item)
        return types_to_search

    def get_selectable_types(self, widget):
        if widget.override:
            return widget.selectable

        registry = getUtility(IRegistry)
        referencesettings = registry.forInterface(IReferenceSettings)
        portal_props = getToolByName(self.context, 'portal_properties')

        non_selectable = set(portal_props.site_properties.types_not_searched)
        non_selectable = non_selectable.union(
            set(referencesettings.block_additional))
        non_selectable = non_selectable.difference(
            set(referencesettings.select_additional))

        non_selectable = non_selectable.union(set(widget.nonselectable))
        non_selectable = non_selectable.difference(set(widget.selectable))
        return self.remove_blacklist_from_types(non_selectable)
