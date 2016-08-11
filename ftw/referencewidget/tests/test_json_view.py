from ftw.referencewidget.browser.jsongenerator import ReferenceJsonEndpoint
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from unittest2 import TestCase
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
import json
from ftw.referencewidget.tests.views.form import TestView

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
        self.assertEquals(2, len(result))
        self.assertEquals(1, len(result['folder']['children']))
        self.assertEquals(0, len(result['file']['children']))

    def test_all_selectable(self):
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']
        view = ReferenceJsonEndpoint(widget, widget.request)
        resultstr = view()
        result = json.loads(resultstr)
        self.assertTrue(result['folder']['selectable'])
        self.assertTrue(result['folder']['children']['file']['selectable'])
        self.assertTrue(result['file']['selectable'])

    def test_folder_not_selectable(self):
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']
        widget.nonselectable = ['Folder']
        view = ReferenceJsonEndpoint(widget, widget.request)

        resultstr = view()
        result = json.loads(resultstr)
        self.assertFalse(result['folder']['selectable'])
        self.assertTrue(result['folder']['children']['file']['selectable'])
        self.assertTrue(result['file']['selectable'])
