import xml.etree.ElementTree as ET
from Section import XmlSection
from Object import XmlObject

class XmlClass(XmlObject):
    def __init__(self,xmlnode):
        doc = ET.parse(xmlnode)
        root = doc.getroot()
        super().__init__(root.find('compounddef'))
        self.sections = [XmlSection(node) for node in self.xmlnode.findall('sectiondef')]
    
    
        
