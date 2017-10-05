from collective.z3cform.datagridfield.datagridfield import DataGridFieldObjectSubForm
from ftw.referencewidget.browser.utils import extend_with_batching
from ftw.referencewidget.browser.utils import get_root_path_from_source
from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.browser.utils import get_sort_options
from ftw.referencewidget.browser.utils import get_sort_order_options
from ftw.referencewidget.browser.utils import get_traversal_types
from ftw.referencewidget.browser.utils import is_traversable
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.component._api import getMultiAdapter
import json


class ReferenceJsonEndpoint(BrowserView):

    def __call__(self):
        widget = self.context

        if isinstance(self.context.form, DataGridFieldObjectSubForm):
            widget.context = self.context.__parent__.context

        result = {
            'items': [],
            'sortOnOptions': get_sort_options(self.request),
            'sortOrderOptions': get_sort_order_options(self.request)
        }

        search_term = widget.request.get('term', None)
        effective_path = widget.request.get('start', None)

        if search_term == '':
            # If search request but no term set, send no items
            return json.dumps(result)

        is_search = search_term is not None
        root_path = get_root_path_from_source(self.context)
        if not effective_path:
            effective_path = widget.get_start_path()
        if root_path and root_path not in effective_path:
            effective_path = root_path
        current_depth = len(effective_path.split('/'))

        results = self.search_catalog(widget, effective_path, search_term,
                                      is_search)
        results, batch_html = extend_with_batching(widget, results)
        selectable_types = get_selectable_types(widget)

        result.update({'batching': batch_html})

        plone = getMultiAdapter((self.context, self.request), name="plone")
        for item in results:
            depth = len(item.getPath().split('/')) - current_depth
            if depth == 0:
                continue
            contenttype = item.portal_type.replace('.', '-').lower()

            path = item.getPath()
            title = item.Title or item.id

            title += ' (%s)' % plone.toLocalizedTime(item.start) if item.start else ''
            title += ' (%s)' % path if is_search else ''

            obj_dict = {'path': path,
                        'id': item.id,
                        'title': title,
                        'folderish': item.is_folderish,
                        'traversable': is_traversable(widget, item),
                        'selectable': item.portal_type in selectable_types,
                        'content-type': 'contenttype-' + contenttype}

            result['items'].append(obj_dict)

        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(result)

    def search_catalog(self, widget, effective_path, search_term=None,
                       is_search=False):
        catalog = getToolByName(self.context.context, 'portal_catalog')
        selectable_types = get_selectable_types(widget)
        traversel_types = get_traversal_types(widget)

        search_term = search_term if search_term is not None else ''
        if search_term != '' and not search_term.endswith('*'):
            search_term += '*'

        if is_search:
            path = ''
        else:
            path = {
                'query': effective_path,
                'depth': 1
            }

        default_query = {
            'Title': search_term,
            'portal_type': traversel_types,
            'path': path,
            'sort_order': self.request.get('sort_order', u'ascending').encode('utf-8'),
            'sort_on': self.request.get('sort_on', u'').encode('utf-8')
        }

        if not default_query['sort_on']:
            # Show the grouped result for easier browsing
            folderish_query = default_query.copy()
            folderish_query.update({'is_folderish': True})
            folderish_query.update(widget.traversal_query)
            folderish_result = catalog(folderish_query)

            content_query = default_query.copy()
            content_query.update({
                'portal_type': selectable_types,
                'is_folderish': False
            })
            content_query.update(widget.traversal_query)
            content_result = catalog(content_query)

            folderish_selectable = set(selectable_types).difference(
                set(traversel_types))
            folder_select_query = default_query.copy()
            folder_select_query.update({
                'portal_type': list(folderish_selectable),
                'is_folderish': True
            })
            folder_select_query.update(widget.traversal_query)
            folder_select_result = catalog(folder_select_query)

            results = folderish_result + content_result + folder_select_result
        else:
            all_query = default_query.copy()
            all_query.update({
                'portal_type': selectable_types + traversel_types,
            })
            all_query.update(widget.traversal_query)
            results = catalog(all_query)

        return results
