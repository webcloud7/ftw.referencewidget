from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.tests import FunctionalTestCase
from ftw.testbrowser import browsing
import transaction


class TestRelationChoice(FunctionalTestCase):

    def setUp(self):
        super(TestRelationChoice, self).setUp()
        self.setup_fti(additional_behaviors=[
            'ftw.referencewidget.behaviors.IRelationChoiceExample'])
        self.grant('Manager')

    @browsing
    def test_relation_choice(self, browser):
        # It's important to use an umlaut in the title of the folder
        # in order to test that there is no UnicodeDecodeError when
        # rendering the widget. Please do not remove the umlaut.
        folder = create(Builder('folder').titled('Some f\xf6lder'))

        content = create(Builder('refwidget sample content')
                         .titled('sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Choice': folder})
        browser.find_button_by_label('Save').click()

        self.assertEqual(folder, content.realtionchoice.to_object)

        browser.login().visit(content, view='@@edit')
        selected = browser.css('.selected_items [type="hidden"]')
        self.assertEqual('/'.join(folder.getPhysicalPath()),
                         selected[0].attrib['value'])

    @browsing
    def test_relation_choice_with_removed_relation(self, browser):
        folder1 = create(Builder('folder').titled('Some folder'))

        content = create(Builder('refwidget sample content')
                         .titled('refwidget sample content')
                         .having(realtionchoice=folder1))

        self.portal.manage_delObjects([folder1.getId()])
        transaction.commit()

        self.assertIsNone(content.realtionchoice.to_object)

        browser.login().visit(content, view='@@edit')
        self.assertNotIn('data-select',
                         browser.css('.selected_items').first.attrib)

    @browsing
    def test_single_value_display_mode(self, browser):
        folder = create(Builder('folder').titled('Some folder'))

        content = create(Builder('refwidget sample content')
                         .titled('sample content')
                         .having(realtionchoice=folder))

        browser.login().visit(content)

        link = browser.css('.reference-widget.relationchoice-field a').first
        self.assertEqual(folder.Title(), link.text)
        self.assertEqual(folder.absolute_url(), link.attrib['href'].replace(':80', ''))


class TestRelationChoiceRestricted(FunctionalTestCase):

    def setUp(self):
        super(TestRelationChoiceRestricted, self).setUp()
        self.setup_fti(additional_behaviors=[
            'ftw.referencewidget.behaviors.IRelationChoiceRestricted'])
        self.grant('Manager')

    @browsing
    def test_relation_choice_folder_is_not_allowed(self, browser):
        folder = create(Builder('folder').titled('Some folder'))

        content = create(Builder('refwidget sample content').titled('refwidget sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Choice Restricted': folder})
        browser.find_button_by_label('Save').click()

        self.assertEqual('Constraint not satisfied',
                         browser.css('.error .invalid-feedback').first.text)
        self.assertIn('There were some errors',
                      browser.css('.statusmessage-error').first.text)

    @browsing
    def test_other_types_are_allowed(self, browser):
        content1 = create(Builder('refwidget sample content').titled('Some content'))

        content2 = create(Builder('refwidget sample content').titled('refwidget sample content'))

        browser.login().visit(content1, view='@@edit')
        browser.fill({'Related Choice Restricted': content2})
        browser.find_button_by_label('Save').click()

        self.assertEqual(content2,
                         content1.realtionchoice_restricted.to_object)

    @browsing
    def test_custom_selectable_class_for_source_binder(self, browser):

        folder = create(Builder('folder').titled('Some folder'))

        content = create(Builder('refwidget sample content').titled('refwidget sample content'))

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Choice Restricted Title': folder})
        browser.find_button_by_label('Save').click()

        self.assertIn('There were some errors',
                      browser.css('.statusmessage-error').first.text)

        folder.title = 'Immutable title'
        transaction.commit()

        browser.login().visit(content, view='@@edit')
        browser.fill({'Related Choice Restricted Title': folder})
        browser.find_button_by_label('Save').click()

        self.assertEqual(folder,
                         content.realtionchoice_restricted_title.to_object)
