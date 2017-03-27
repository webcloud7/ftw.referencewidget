from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.tests import FunctionalTestCase
from ftw.testbrowser import browsing
import json
import transaction


class TestRelationChoice(FunctionalTestCase):

    def setUp(self):
        super(TestRelationChoice, self).setUp()
        self.setup_fti(additional_behaviors=[
            'ftw.referencewidget.behaviors.IRelationChoiceExample'])
        self.grant('Manager')

    @browsing
    def test_relation_choice(self, browser):
        folder = create(Builder('folder').titled(u'Some folder'))

        content = create(Builder('sample content').titled(u'Sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Choice': folder})
        browser.find_button_by_label('Save').click()

        self.assertEquals(folder, content.realtionchoice.to_object)

        browser.login().visit(content, view='@@edit')
        selected = json.loads(browser.css(
            '.selected_items').first.attrib['data-select'])
        self.assertEquals('/'.join(folder.getPhysicalPath()),
                          selected[0]['path'])

    @browsing
    def test_relateditems_with_removed_relation(self, browser):
        folder1 = create(Builder('folder').titled(u'Some folder'))

        content = create(Builder('sample content')
                         .titled(u'Sample content')
                         .having(realtionchoice=folder1))

        self.portal.manage_delObjects([folder1.getId()])
        transaction.commit()

        self.assertIsNone(content.realtionchoice.to_object)

        browser.login().visit(content, view='@@edit')
        self.assertNotIn('data-select',
                         browser.css('.selected_items').first.attrib)
