import xml.etree.ElementTree as ET
from Object import XmlObject
import enum
from Mapper import properties


class FieldType(enum.Enum):
    PubFunction = 'public-func'
    PrivFunction = 'private-func'
    Variable = 'variable'
    PrivVariable = 'private-attrib'
    Signal   = 'signal'
    Property = 'property'



"""
FieldType: method, attribute, property, typedef, enum
"""

class XmlField(XmlObject):
    def __init__(self, node : ET.Element):
        super().__init__(node)


class XmlFieldProperty(XmlField):
    def __init__(self, node: ET.Element):
        super().__init__(node)
        self.type_ = self.xmlnode.find('type').text
        self.name = self.xmlnode.find('name').text
        self.read = self.xmlnode.find('read').text
        self.write = self.xmlnode.find('write').text if self.containsField(self.xmlnode, 'write') else None
        self.signal = self.name+"Changed"
    def print(self):
        res = "QPROPERTY({0} {1} READ {2} ".format(self.type_,self.name,self.read)
        if self.write is not None:
            res += "WRITE {0} ".format(self.write)
        res += "NOTIFY {0}Changed)".format(self.name)
        print(res)
        #print("QPROPERTY({0} {1} {2} {3} {4}".format())

class XmlFieldVariable(XmlField):
    def _init__(self, node: ET.Element):
        super().__init__(node)
    def generateHpp(self):
        return str()

class XmlFieldFunc(XmlField):
    def __init__(self, node: ET.Element):
        super().__init__(node)
        self.definition = self.formDefinition(node)

    def formDefinition(self, node: ET.Element):
        func_def = ""
        func_name = node.find('name').text[1:] if node.find('name').text.startswith('~') else node.find('name').text
        for attr in node.attrib.keys():
            if node.attrib[attr] == 'yes' and attr != "const":
                func_def += attr + " "
        if node.find('definition').text.startswith(func_name):
            func_def += ' ' + func_name
        else:
            func_def += node.find('definition').text
        func_def += node.find('argsstring').text
        return func_def
            
    def print(self):
        print("-----------------------")
        print(self.brief)
        print(self.detailed)
        print(self.definition)


class FieldFactory():
    def GetField(fieldtype : str, node): 
        if (fieldtype == FieldType.PubFunction.value   or 
            fieldtype == FieldType.PrivFunction.value  or
            fieldtype == FieldType.Signal.value):
            return XmlFieldFunc(node)

        elif fieldtype == FieldType.Variable.value or fieldtype == FieldType.PrivVariable.value:
            return XmlFieldVariable(node)

        elif fieldtype == FieldType.Property.value:
            return XmlFieldProperty(node)



class XMlElement(XmlObject):
    def __init__(self, node: ET.Element):
        super().__init__(node)
    def print(self):
        print(self.xmlnode.tag, self.xmlnode.text)

    def __str__(self) -> str:
        if self.xmlnode is not None and self.xmlnode.text != "":
            return self.xmlnode.tag.upper() + " " + self.xmlnode.text 
        return ""
