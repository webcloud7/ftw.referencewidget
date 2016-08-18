from ftw.referencewidget.interfaces import IReferenceWidget
from z3c.form import converter
from z3c.relationfield.interfaces import IRelationList
from zope.component import adapts


class ReferenceDataConverter(converter.BaseDataConverter):

    adapts(IRelationList, IReferenceWidget)

    def toFieldValue(self, value):
        if isinstance(value, unicode):
            return [self.widget.context.unrestrictedTraverse(
                value.encode("utf8"))]
        else:
            result = []
            for item in value:
                result.append(self.widget.context.unrestrictedTraverse(
                    item.encode("utf-8")))
            return result

    def toWidgetValue(self, value):
        result = []
        for item in value:
            result.append('/'.join(item.getPhysicalPath()))
        return result
