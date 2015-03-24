# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from zope.interface import implements
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations

from genweb.packets.interfaces import Ipacket, IpacketDefinition
from genweb.packets.base import BasePacket
from genweb.packets import PACKETS_KEY
from genweb.packets import packetsMessageFactory as _




class FitxaGrau(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    order = 1

    def __init__(self, context):
        self.context = context
        self.title = _(u"Fitxa de grau")
        self.description = _(u"Informació sobre un estudi d'un grau específic")
        #self.URL_schema = 'http://www.upc.edu/grau/fitxa_grau.php?codi=%(codi_grau)s&lang=%(lang)s&sense_titol'
        self.URL_schema = 'http://147.83.128.10/content/index.php/grau/fitxa/html?codi=%(codi_grau)s&lang=%(lang)s&sense_titol&contingut_upc=true'
        self.fields = [_(u'codi_grau')]
        self.default = dict([(field, '') for field in self.fields])
        self.mapui = dict(codi=u'codi_grau')

class PlaEstudisGrau(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    order = 2

    def __init__(self, context):
        self.context = context
        self.title = _(u"Pla d'estudi de grau")
        self.description = _(u"Informació sobre el pla d'estudis d'un grau específic")
        self.URL_schema = 'http://www.upc.edu/grau/fitxa_grau.php?codi=%(codi_grau)s&lang=%(lang)s&pla_estudis&sense_titol&contingut_upc=true'
        self.fields = [_(u'codi_grau')]
        self.default = dict([(field, '') for field in self.fields])
        self.mapui = dict(codi=u'codi_grau')


class FitxaMaster(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    order = 3

    # http://www.upc.edu/master/fitxa_master.php?id_estudi=19&lang=ca
    def __init__(self, context):
        self.context = context

        self.title = _(u"Fitxa de màster")
        self.description = _(u"Informació sobre un màster específic")
        self.URL_schema = 'http://www.upc.edu/master/fitxa_master.php?id_estudi=%(codi_master)s&lang=%(lang)s&sense_titol&contingut_upc=true'
        self.fields = [_(u'codi_master')]
        self.default = dict([(field, '') for field in self.fields])
        self.mapui = dict(codi=u'codi_master')


class PlaEstudisMaster(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    order = 4

    # http://www.upc.edu/master/fitxa_master.php?id_estudi=19&lang=ca
    def __init__(self, context):
        self.context = context

        self.title = _(u"Pla d'estudis de màster")
        self.description = _(u"Informació sobre un pla d'estudis de màster específic")
        self.URL_schema = 'http://www.upc.edu/master/fitxa_master.php?id_estudi=%(codi_pla_master)s&lang=%(lang)s&pla_estudis&sense_titol&contingut_upc=true'
        self.fields = [_(u'codi_pla_master')]
        self.default = dict([(field, '') for field in self.fields])
        self.mapui = dict(codi=u'codi_pla_master')


class GrupsRecercaDepartament(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    order = 5

    def __init__(self, context):
        self.context = context
        self.title = _(u"Grups de recerca")
        self.description = _(u"Grups de recerca d'un departament específic")
        self.URL_schema = 'http://www.upc.edu/ws/drac/LlistatGrupsRecercav1.php?codiupc=%(codi_departament)s&lang=%(lang)s&contingut_upc=true'
        self.fields = [_(u'codi_departament')]
        self.default = dict([(field, '') for field in self.fields])
        self.mapui = dict(codi=u'codi_departament')


class InvestigadorsGrupRecercaDepartament(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    order = 6

    def __init__(self, context):
        self.context = context
        self.title = _(u"Investigadors d'un grup de recerca")
        self.description = _(u"Investigadors d'un grup de recerca d'un departament específic")
        self.URL_schema = 'http://www.upc.edu/ws/drac/LlistatInvestigadorsGRv1.php?acronim=%(acronim)s&lang=%(lang)s&contingut_upc=true'
        self.fields = [_(u'acronim')]
        self.default = dict([(field, '') for field in self.fields])
        self.mapui = dict(codi=u'acronim')


class IndexPestanyes(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    order = 7

    def __init__(self, context):
        self.context = context
        self.title = _(u"Llista estudis")
        self.description = _(u"Llista estudis: es pot escollir 'grau' o 'master'")

        server = 'http://147.83.128.10/content/index.php/'
        self.URL_schema = server + '%(tipus_llistat)s/llistat/index/%(lang)s?genweb=true'
        self.URL_schema_estudi = server + '%(tipus_llistat)s/fitxa/html/?lang=%(lang)s&genweb=true'
        
        self.fields = [_(u'tipus_llistat')]
        self.default = dict([(field, '') for field in self.fields])
        self.mapui = dict(codi=u'tipus_llistat')


class ContingutGenweb(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    order = 8

    def __init__(self, context):
        self.context = context
        self.title = _(u"Contingut extern genweb")
        self.description = _(u"url del contingut ")
        self.URL_schema = '%(url_contingut)s'
        self.fields = [_(u'url_contingut')]
        self.default = dict([(field, '') for field in self.fields])
        self.mapui = dict(codi=u'url_contingut')

