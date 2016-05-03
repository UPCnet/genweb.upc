from zope.interface import implements
from plone.dexterity.content import Item

from genweb.upc.content.subhome import ISubhome


class Subhome(Item):
    implements(ISubhome)
