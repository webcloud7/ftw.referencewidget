from ftw.referencewidget.sources import ReferenceWidgetPathSourceBinder
from plone.app.dexterity import MessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel.model import fieldset
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface import alsoProvides
from zope.interface import Interface
from ftw.referencewidget.widget import ReferenceWidgetFactory


class IRelatedItems(Interface):
    """Behavior, which provides the same functionality as the
    plone.app.relationfield IRelatedItems behavior, BUT it uses a different
    widget.

    """

    fieldset('categorization',
             label=_(u'Categorization'),
             fields=['relatedItems'])

    directives.widget(relatedItems=ReferenceWidgetFactory)
    relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(title=u"Related",
                                  source=ReferenceWidgetPathSourceBinder()),
        required=False,
    )

alsoProvides(IRelatedItems, IFormFieldProvider)
