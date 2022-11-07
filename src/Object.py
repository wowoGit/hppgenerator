
import xml.etree.ElementTree as ET


class XmlObject:
    def __init__(self,node: ET.Element):
        self.xmlnode = node
    

    def print(self):
        print(self.xmlnode.tag, self.xmlnode.attrib)

    def generateHpp(self):
        raise NotImplementedError()
