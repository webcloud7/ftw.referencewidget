from zope import schema
from zope.interface import Interface


class IReferenceSettings(Interface):

    select_additional = schema.Tuple(title=u"Additional types to select.",
                                     default=())

    block_additional = schema.Tuple(title=u"Additional types to block.",
                                    default=())

    traverse_additional = schema.Tuple(title=u"Additional types to traverse.",
                                       default=())

    block_traversal_additional = schema.Tuple(
        title=u"Additional types to block traversel of.", default=())


class IReferenceWidget(Interface):
    pass
