from z3c.form import converter
from z3c.relationfield.interfaces import IRelationList
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield import create_relation
from ftw.referencewidget.interfaces import IReferenceWidget
from zope.component import adapts


class ReferenceDataConverter(converter.BaseDataConverter):

    adapts(IRelationList, IReferenceWidget)

    def toFieldValue(self, value):
        if isinstance(value, unicode):
            return [create_relation(value.encode("utf8"))]
        else:
            result = []
            for item in value:
                result.append(create_relation(item.encode("utf-8")))
            return result

    def toWidgetValue(self, value):
        result = []
        for item in value:
            result.append(value.to_path().decode('utf8'))
        return result
