from ftw.referencewidget.selectable import DefaultSelectable
from ftw.referencewidget.sources import ReferenceObjSourceBinder
from ftw.referencewidget.widget import ReferenceWidgetFactory
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.model import fieldset
from plone.base import PloneMessageFactory as pmf
from ftw.referencewidget import _
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface import provider


@provider(IFormFieldProvider)
class IRelatedItems(model.Schema):
    """Behavior, which provides the same functionality as the
    plone.app.relationfield IRelatedItems behavior, BUT it uses a different
    widget.

    """

    fieldset('categorization',
             label=pmf('Categorization'),
             fields=['relatedItems'])

    directives.widget(relatedItems=ReferenceWidgetFactory)
    relatedItems = RelationList(
        title=_('label_related_items', default='Related Items'),
        default=[],
        value_type=RelationChoice(title=u"Related",
                                  source=ReferenceObjSourceBinder()),
        required=False,
    )


@provider(IFormFieldProvider)
class IRelationChoiceExample(model.Schema):
    """Demo behavior containing a RelationChoice (single value).

    """
    directives.widget(realtionchoice=ReferenceWidgetFactory)
    realtionchoice = RelationChoice(
        title=_('Related Choice'),
        source=ReferenceObjSourceBinder(),
        default=None,
        required=False,
    )


class CustomSelectableClass(DefaultSelectable):

    def is_selectable(self):
        return self.content.Title() == 'Immutable title'


@provider(IFormFieldProvider)
class IRelationChoiceRestricted(model.Schema):
    """Demo behavior containing a RelationChoice (single value).
    But it's not allowd to reference a folder.

    """
    directives.widget(realtionchoice_restricted=ReferenceWidgetFactory)
    realtionchoice_restricted = RelationChoice(
        title=_('Related Choice Restricted'),
        source=ReferenceObjSourceBinder(
            nonselectable=['Folder']),
        default=None,
        required=False,
    )

    directives.widget(realtionchoice_restricted_title=ReferenceWidgetFactory)
    realtionchoice_restricted_title = RelationChoice(
        title=_('Related Choice Restricted Title'),
        source=ReferenceObjSourceBinder(
            selectable_class=CustomSelectableClass),
        default=None,
        required=False,
    )

    directives.widget(realtionchoice_restricted_path=ReferenceWidgetFactory)
    realtionchoice_restricted_path = RelationChoice(
        title=_('Related Choice Restricted Title'),
        source=ReferenceObjSourceBinder(
            root_path='/testfolder'),
        default=None,
        required=False,
    )
