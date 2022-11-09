import xml.etree.ElementTree as ET
from Section import XmlSection, XmlCompoundSection
from Object import XmlObject

class XmlClass(XmlObject):
    def __init__(self,xmlnode):
        doc = ET.parse(xmlnode)
        root = doc.getroot()
        super().__init__(root.find('compounddef'))
        include = self.xmlnode.findall('includes')
        self.sections = [XmlSection(node) for node in self.xmlnode.findall('sectiondef')]
        self.print()
    
    def print(self):
        super().print()
        for section in self.sections:
            print("Section: {}".format(section.kind))
            for field in section.fields:
                field.print()
    
    
        
