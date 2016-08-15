from z3c.objpath.interfaces import IObjectPath
from zope.interface import implements
from z3c.objpath import path, resolve
from zope.component.hooks import getSite


class ObjectPath(object):

    implements(IObjectPath)

    def path(self, obj):
        return path(getSite(), obj)

    def resolve(self, path):
        return resolve(getSite(), path)
