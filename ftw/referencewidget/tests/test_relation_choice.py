from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import statusmessages
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
    def test_relation_choice_with_removed_relation(self, browser):
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


class TestRelationChoiceRestricted(FunctionalTestCase):

    def setUp(self):
        super(TestRelationChoiceRestricted, self).setUp()
        self.setup_fti(additional_behaviors=[
            'ftw.referencewidget.behaviors.IRelationChoiceRestricted'])
        self.grant('Manager')

    @browsing
    def test_relation_choice_folder_is_not_allowed(self, browser):
        folder = create(Builder('folder').titled(u'Some folder'))

        content = create(Builder('sample content').titled(u'Sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Choice Restricted': folder})
        browser.find_button_by_label('Save').click()

        self.assertEquals('Constraint not satisfied',
                          browser.css('.fieldErrorBox .error').first.text)
        self.assertEquals(['There were some errors.'],
                          statusmessages.error_messages())

    @browsing
    def test_other_types_are_allowed(self, browser):
        content1 = create(Builder('sample content').titled(u'Some content'))

        content2 = create(Builder('sample content').titled(u'Sample content'))

        browser.login().visit(content1, view='@@edit')
        browser.fill({'Related Choice Restricted': content2})
        browser.find_button_by_label('Save').click()

        self.assertEquals(content2,
                          content1.realtionchoice_restricted.to_object)

    @browsing
    def test_custom_filter_method_for_source_binder(self, browser):

        folder = create(Builder('folder').titled(u'Some folder'))

        content = create(Builder('sample content').titled(u'Sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Choice Restricted Title': folder})
        browser.find_button_by_label('Save').click()

        self.assertEquals(['There were some errors.'],
                          statusmessages.error_messages())

        folder.title = u'Immutable title'
        transaction.commit()

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Choice Restricted Title': folder})
        browser.find_button_by_label('Save').click()

        self.assertEquals(folder,
                          content.realtionchoice_restricted_title.to_object)
