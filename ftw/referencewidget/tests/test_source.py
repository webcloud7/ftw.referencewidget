from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.sources import ReferenceObjSourceBinder
from ftw.referencewidget.tests import FunctionalTestCase


class TestReferenceObjSource(FunctionalTestCase):

    def setUp(self):
        super(TestReferenceObjSource, self).setUp()
        self.setup_fti()
        self.grant('Manager')

    def test_root_path_restriction(self):
        folder = create(Builder('folder'))
        subfolder = create(Builder('folder').within(folder))
        subsubfolder = create(Builder('folder').within(subfolder))
        sibling = create(Builder('folder'))

        source = ReferenceObjSourceBinder(
            root_path='/folder/folder')(subfolder)

        self.assertIn(subsubfolder, source)
        self.assertIn(subfolder, source)

        self.assertNotIn(folder, source)
        self.assertNotIn(sibling, source)
