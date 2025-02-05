from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.tests import FunctionalTestCase
from ftw.testbrowser import browsing
import transaction


class TestRelatedItemsReplacement(FunctionalTestCase):

    def setUp(self):
        super(TestRelatedItemsReplacement, self).setUp()
        self.setup_fti()
        self.grant('Manager')

    @browsing
    def test_relateditems_behavior_with_one_item(self, browser):
        folder = create(Builder('folder').titled('Some folder'))

        content = create(Builder('refwidget sample content').titled(
            'refwidget sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Items': folder})
        browser.find_button_by_label('Save').click()

        self.assertEqual(
            [folder],
            [relation.to_object for relation in content.relatedItems])

    @browsing
    def test_relateditems_behavior_with_multiple_items(self, browser):
        folder1 = create(Builder('folder').titled('Some folder'))
        folder2 = create(Builder('folder').titled('Some folder'))

        content = create(Builder('refwidget sample content').titled(
            'refwidget sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Items': [folder1, folder2]})
        browser.find_button_by_label('Save').click()

        self.assertEqual(
            [folder1, folder2],
            [relation.to_object for relation in content.relatedItems])

    @browsing
    def test_relateditems_with_removed_relation(self, browser):
        folder1 = create(Builder('folder').titled('Some folder'))
        folder2 = create(Builder('folder').titled('Some folder'))

        content = create(Builder('refwidget sample content')
                         .titled('refwidget sample content')
                         .having(relatedItems=[folder1, folder2]))

        self.portal.manage_delObjects([folder2.getId()])
        transaction.commit()

        browser.login().visit(content, view='@@edit')

        self.assertEqual(
            [folder1, None],
            [relation.to_object for relation in content.relatedItems])

        selected = browser.css('.selected_items [type="hidden"]')
        self.assertEqual(1, len(selected), 'Expect only one item')
        self.assertEqual(['/'.join(folder1.getPhysicalPath())],
                         [item.attrib['value'] for item in selected])

    @browsing
    def test_render_stored_related_items(self, browser):
        folder1 = create(Builder('folder').titled('Some folder'))
        folder2 = create(Builder('folder').titled('Some folder'))

        content = create(Builder('refwidget sample content')
                         .titled('refwidget sample content')
                         .having(relatedItems=[folder1, folder2]))

        browser.login().visit(content, view='@@edit')
        selected_items = browser.css('.selected_items input')

        self.assertEqual(2, len(selected_items))

        self.assertEqual(folder1.Title(),
                         selected_items[0].attrib['data-title'])
        self.assertEqual('/'.join(folder1.getPhysicalPath()),
                         selected_items[0].attrib['value'])

        self.assertEqual(folder2.Title(),
                         selected_items[1].attrib['data-title'])
        self.assertEqual('/'.join(folder2.getPhysicalPath()),
                         selected_items[1].attrib['value'])

    @browsing
    def test_multi_value_display_mode(self, browser):
        folder1 = create(Builder('folder').titled('Folder 1'))
        folder2 = create(Builder('folder').titled('Folder 2'))

        content = create(Builder('refwidget sample content')
                         .titled('sample content')
                         .having(relatedItems=[folder1, folder2]))

        browser.login().visit(content)

        links = browser.css('.reference-widget.relationlist-field a')
        self.assertEqual(2, len(links), 'Expect two links')

        link1, link2 = links
        self.assertEqual(folder1.Title(), link1.text)
        self.assertEqual(folder1.absolute_url(), link1.attrib['href'].replace(':80', ''))
        self.assertEqual(folder2.Title(), link2.text)
        self.assertEqual(folder2.absolute_url(), link2.attrib['href'].replace(':80', ''))
