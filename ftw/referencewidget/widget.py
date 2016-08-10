from ftw.referencewidget.interfaces import IReferenceWidget
from z3c.form.browser import widget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from zope.component import adapter
from zope.interface import implementer
from zope.interface import implementsOnly


class ReferenceBrowserWidget(widget.HTMLTextInputWidget, Widget):
    """ Datepicker widget. """
    implementsOnly(IReferenceWidget)

    klass = u'reference-widget'
    block_traversal = None
    allow_traversal = None
    selectable = None
    nonselectable = None
    start = None
    override = None

    def __init__(self,
                 request,
                 block_traversal=[],
                 allow_traversal=[],
                 selectable=[],
                 nonselectable=[],
                 start='',
                 override=False):

        self.block_traversal = block_traversal
        self.allow_traversal = allow_traversal
        self.selectable = selectable
        self.nonselectable = nonselectable
        self.start = start
        self.override = override


@adapter(IReferenceWidget, IFormLayer)
@implementer(IFieldWidget)
def DateTimePickerWidgetFactory(field,
                                request,
                                block_traversal=[],
                                allow_traversal=[],
                                selectable=[],
                                nonselectable=[],
                                start='',
                                override=False):
    """IFieldWidget factory for DateTimePickerWidget."""
    return FieldWidget(field, ReferenceBrowserWidget(request,
                                                     block_traversal,
                                                     allow_traversal,
                                                     selectable,
                                                     nonselectable,
                                                     start,
                                                     override))
