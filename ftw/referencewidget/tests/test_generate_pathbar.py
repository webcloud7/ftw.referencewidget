from ftw.referencewidget.browser.generate_pathbar import GeneratePathbar
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from unittest2 import TestCase
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
import json


class TestGeneratePathbar(TestCase):
    layer = FTW_REFERENCE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.folder = create(Builder('folder'))
        self.lower_file = create(Builder('file').within(self.folder))
        self.file = create(Builder('file'))

    def test_generate_pathbar(self):
        self.portal.REQUEST['POST'] = {'origin': '/plone'}
        view = GeneratePathbar(self.portal, self.portal.REQUEST)
        resultstr = view()
        result = json.loads(resultstr)
        self.assertEquals(1, len(result))
        self.assertEquals("http://nohost/plone", result[0]['url'])
        self.assertEquals("Plone site", result[0]['title'])

