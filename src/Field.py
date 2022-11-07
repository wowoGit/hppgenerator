import xml.etree.ElementTree as ET
from Object import XmlObject
import enum


class FieldType(enum.Enum):
    PubFunction = 'public-func'
    PrivFunction = 'private-func'
    Variable = 'variable'
    PrivVariable = 'private-attrib'
    Signal   = 'signal'
    Property = 'property'



class XmlField(XmlObject):
    def __init__(self, node : ET.Element):
        super().__init__(node)


class XmlFieldProperty(XmlField):
    def _init__(self, node: ET.Element):
        super().__init__(node)

class XmlFieldVariable(XmlField):
    def _init__(self, node: ET.Element):
        super().__init__(node)

class XmlFieldFunc(XmlField):
    def _init__(self, node: ET.Element):
        super().__init__(node)

class XmlFieldSignal(XmlField):
    def _init__(self, node: ET.Element):
        super().__init__(node)


class FieldFactory():
    def GetField(fieldtype : str, node): 
        print()
        if fieldtype == FieldType.PubFunction.value  or fieldtype == FieldType.PrivFunction.value:
            return XmlFieldFunc(node)

        elif fieldtype == FieldType.Variable.value:
            return XmlFieldVariable(node)

        elif fieldtype == FieldType.Property.value:
            return XmlFieldProperty(node)

        elif fieldtype == FieldType.Signal.value:
            return XmlFieldProperty(node)
        elif fieldtype == FieldType.PrivVariable.value:
            return XmlFieldProperty(node)


         
