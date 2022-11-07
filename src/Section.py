import xml.etree.ElementTree as ET
from Object import XmlObject


class XmlSection(XmlObject):
    def __init__(self,xmlnode: ET.Element):
        self.xmlnode = xmlnode
        self.kind = xmlnode.get('kind')
