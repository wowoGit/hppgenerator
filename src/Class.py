import xml.etree.ElementTree as ET
from Section import XmlSection
from Object import XmlObject

class XmlClass(XmlObject):
    def __init__(self,xmlnode):
        doc = ET.parse(xmlnode)
        self.root = doc.getroot()
        self.xmlnode = self.root.find('compounddef')
        self.sections = [XmlSection(node) for node in self.xmlnode.findall('sectiondef')]
    
    
        
