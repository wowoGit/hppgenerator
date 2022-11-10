import xml.etree.ElementTree as ET
from Field import *


class XmlSection(XmlObject):
    def __init__(self,xmlnode: ET.Element):
        super().__init__(xmlnode)
        self.kind = xmlnode.get('kind')
        self.fields = [FieldFactory.GetField(node.get('kind'),node) for node in self.xmlnode.findall('memberdef')]

    def print(self):
            for field in self.fields:
                print(field.detailed)

class XmlCompoundSection(XmlSection):
    def __init__(self, xmlnode: ET.Element):
         super().__init__(xmlnode)
         self.subsections = []
