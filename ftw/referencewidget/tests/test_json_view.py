from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.browser.endpoint import ReferenceJsonEndpoint
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from ftw.referencewidget.tests.views.form import TestView
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.ATContentTypes.interfaces.folder import IATFolder
from unittest2 import TestCase
import json


class TestJsonView(TestCase):
    layer = FTW_REFERENCE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        folder = create(Builder('folder'))
        create(Builder('file').within(folder))
        create(Builder('file'))

    def test_get_json_view(self):
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']
        view = ReferenceJsonEndpoint(widget, widget.request)
        resultstr = view()
        result = json.loads(resultstr)

        items = result['items']
        self.assertEquals(2, len(items))
        self.assertEquals("folder", items[0]['id'])
        self.assertEquals("file", items[1]['id'])

    def test_all_selectable(self):
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']
        view = ReferenceJsonEndpoint(widget, widget.request)
        resultstr = view()
        result = json.loads(resultstr)
        result = result['items']
        self.assertTrue(result[0]['selectable'])
        self.assertTrue(result[1]['selectable'])

    def test_folder_not_selectable(self):
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']
        widget.nonselectable = ['Folder']
        view = ReferenceJsonEndpoint(widget, widget.request)

        resultstr = view()
        result = json.loads(resultstr)
        result = result['items']
        self.assertFalse(result[0]['selectable'])
        self.assertTrue(result[1]['selectable'])

    def test_additional_traversable_query_is_applied(self):
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']

        widget.traversal_query = {
            'object_provides': [IATFolder.__identifier__]}
        result = json.loads(ReferenceJsonEndpoint(
            widget, widget.request)())['items']

        self.assertEquals(1, len(result), 'Exepct only one item')
        self.assertEquals('/plone/folder', result[0]['path'])
