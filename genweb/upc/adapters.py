# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from zope.interface import implements
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations

from genweb.packets.interfaces import Ipacket, IpacketDefinition
from genweb.packets import PACKETS_KEY
from genweb.packets import packetsMessageFactory as _


class BasePacket(object):
    """ The default packet boilerplate """
    def get_packet_fields(self):
        annotations = IAnnotations(self.context)
        self._packet_fields = annotations.setdefault(PACKETS_KEY + '.fields', PersistentDict(self.default))
        return self._packet_fields

    def set_packet_fields(self, value):
        annotations = IAnnotations(self.context)
        annotations.setdefault(PACKETS_KEY + '.fields', PersistentDict(self.default))
        annotations[PACKETS_KEY + '.fields'] = value

    packet_fields = property(get_packet_fields, set_packet_fields)

    def get_packet_type(self):
        annotations = IAnnotations(self.context)
        self._type = annotations.setdefault(PACKETS_KEY + '.type', '')
        return self._type

    def set_packet_type(self, value):
        annotations = IAnnotations(self.context)
        annotations.setdefault(PACKETS_KEY + '.type', '')
        annotations[PACKETS_KEY + '.type'] = value

    packet_type = property(get_packet_type, set_packet_type)


class FitxaGrau(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    def __init__(self, context):
        self.context = context
        self.title = _(u"Fitxa de grau")
        self.description = _(u"Informació sobre un estudi d'un grau específic")
        self.URL_schema = 'http://www.upc.edu/grau/fitxa_grau.php?codi=%(codi_grau)s&lang=%(lang)s&sense_titol'
        self.fields = [_(u'codi_grau')]
        self.default = dict([(field, '') for field in self.fields])
        annotations = IAnnotations(context)
        self._packet_fields = annotations.setdefault(PACKETS_KEY + '.fields', PersistentDict(self.default))
        self._type = annotations.setdefault(PACKETS_KEY + '.type', '')


class PlaEstudisGrau(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    def __init__(self, context):
        self.context = context
        self.title = _(u"Pla d'estudi de grau")
        self.description = _(u"Informació sobre el pla d'estudis d'un grau específic")
        self.URL_schema = 'http://www.upc.edu/grau/fitxa_grau.php?codi=%(codi_grau)s&lang=%(lang)s&pla_estudis&sense_titol'
        self.fields = [_(u'codi_grau')]
        self.default = dict([(field, '') for field in self.fields])
        annotations = IAnnotations(context)
        self._packet_fields = annotations.setdefault(PACKETS_KEY + '.fields', PersistentDict(self.default))
        self._type = annotations.setdefault(PACKETS_KEY + '.type', '')


class FitxaMaster(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)
    # http://www.upc.edu/master/fitxa_master.php?id_estudi=19&lang=ca
    def __init__(self, context):
        self.context = context
        self.title = _(u"Fitxa de màster")
        self.description = _(u"Informació sobre un màster específic")
        self.URL_schema = 'http://www.upc.edu/master/fitxa_master.php?id_estudi=%(codi_master)s&lang=%(lang)s&sense_titol'
        self.fields = [_(u'codi_master')]
        self.default = dict([(field, '') for field in self.fields])
        annotations = IAnnotations(context)
        self._packet_fields = annotations.setdefault(PACKETS_KEY + '.fields', PersistentDict(self.default))
        self._type = annotations.setdefault(PACKETS_KEY + '.type', '')


class GrupsRecercaDepartament(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    def __init__(self, context):
        self.context = context
        self.title = _(u"Grups de recerca")
        self.description = _(u"Grups de recerca d'un departament específic")
        self.URL_schema = 'http://www.upc.edu/ws/drac/LlistatGrupsRecercav1.php?codiupc=%(codi_departament)s&lang=%(lang)s'
        self.fields = [_(u'codi_departament')]
        self.default = dict([(field, '') for field in self.fields])
        annotations = IAnnotations(context)
        self._packet_fields = annotations.setdefault(PACKETS_KEY + '.fields', PersistentDict(self.default))
        self._type = annotations.setdefault(PACKETS_KEY + '.type', '')


class InvestigadorsGrupRecercaDepartament(BasePacket):
    implements(IpacketDefinition)
    adapts(Ipacket)

    def __init__(self, context):
        self.context = context
        self.title = _(u"Investigadors d'un grup de recerca")
        self.description = _(u"Investigadors d'un grup de recerca d'un departament específic")
        self.URL_schema = 'http://www.upc.edu/ws/drac/LlistatInvestigadorsGRv1.php?acronim=%(acronim)s&lang=%(lang)s'
        self.fields = [_(u'acronim')]
        self.default = dict([(field, '') for field in self.fields])
        annotations = IAnnotations(context)
        self._packet_fields = annotations.setdefault(PACKETS_KEY + '.fields', PersistentDict(self.default))
        self._type = annotations.setdefault(PACKETS_KEY + '.type', '')
