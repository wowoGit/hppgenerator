import xml.etree.ElementTree as ET
from Field import *


class XmlSection(XmlObject):
    def __init__(self,xmlnode: ET.Element):
        super().__init__(xmlnode)
        self.kind = xmlnode.get('kind')
        self.fields = [FieldFactory.GetField(self.kind,node) for node in self.xmlnode.findall('memberdef')]
        print("Kind" + self.kind)
        print(self.fields)
        for field in self.fields:
            field.print()