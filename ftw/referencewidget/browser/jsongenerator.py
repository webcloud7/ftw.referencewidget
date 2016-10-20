from ftw.referencewidget import _
from ftw.referencewidget.browser.utils import extend_with_batching
from ftw.referencewidget.browser.utils import get_selectable_types
from ftw.referencewidget.browser.utils import get_traversal_types
from ftw.referencewidget.browser.utils import is_traversable
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.i18n import translate
import json


class ReferenceJsonEndpoint(BrowserView):

    def __call__(self):
        widget = self.context

        effective_path = widget.request.get('start', None)
        if not effective_path:
            effective_path = widget.get_start_path()
        current_depth = len(effective_path.split('/'))

        results = self.search_catalog(widget, effective_path)
        results, batch_html = extend_with_batching(widget, results)

        selectable_types = get_selectable_types(widget)

        result = {'batching': batch_html,
                  'items': [],
                  'sortOnOptions': self.get_sort_options(),
                  'sortOrderOptions': self.get_sort_order_options()}

        for item in results:
            depth = len(item.getPath().split('/')) - current_depth
            if depth == 0:
                continue
            contenttype = item.portal_type.replace('.', '-').lower()
            obj_dict = {'path': item.getPath(),
                        'id': item.id,
                        'title': item.Title or item.id,
                        'folderish': item.is_folderish,
                        'traversable': is_traversable(widget, item),
                        'selectable': item.portal_type in selectable_types,
                        'content-type': 'contenttype-' + contenttype}

            result['items'].append(obj_dict)

        self.request.RESPONSE.setHeader("Content-type", "application/json")
        return json.dumps(result)

    def get_sort_options(self):
        sort_indexes = ['', 'sortable_title', 'created', 'modified']
        options = []

        for index in sort_indexes:
            index_title = index != '' and index or 'no sort'
            options.append(
                {'title': translate(_(index_title), context=self.request),
                 'value': index,
                 'selected': index == self.request.get('sort_on', '')}
            )

        return options

    def get_sort_order_options(self):
        sort_directions = ['', 'ascending', 'descending']
        options = []

        for direction in sort_directions:
            direction_title = direction != '' and direction or 'no direction'
            options.append(
                {'title': translate(_(direction_title), context=self.request),
                 'value': direction,
                 'selected': direction == self.request.get('sort_order', '')}
            )

        return options

    def search_catalog(self, widget, effective_path):

        # XXX This method needs heavy refactoring
        # Also merge with the search.py

        catalog = getToolByName(self.context.context, 'portal_catalog')
        selectable_types = get_selectable_types(widget)
        traversel_types = get_traversal_types(widget)

        sort_query = {
            'sort_order': self.request.get('sort_order',
                                           u'ascending').encode('utf-8'),
            'sort_on': self.request.get('sort_on', u'').encode('utf-8')}

        if not sort_query['sort_on']:
            # Show the grouped result for easier browsing
            query = {'portal_type': traversel_types,
                     'path': {'query': effective_path,
                              'depth': 1},
                     'is_folderish': True
                     }

            results_folderish = catalog(query)

            query = {'portal_type': selectable_types,
                     'path': {'query': effective_path,
                              'depth': 1},
                     'is_folderish': False
                     }

            results_content = catalog(query)

            folderish_selectable = set(selectable_types).difference(
                set(traversel_types))
            query = {'portal_type': list(folderish_selectable),
                     'path': {'query': effective_path,
                              'depth': 1},
                     'is_folderish': True
                     }

            results_folder_select = catalog(query)
            results = results_folderish + results_content + results_folder_select

        else:
            query = {'portal_type': selectable_types + traversel_types,
                     'path': {'query': effective_path,
                              'depth': 1},
                     }
            query.update(sort_query)
            results = catalog(query)

        return results
