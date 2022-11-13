import xml.etree.ElementTree as ET
from Section import XmlSection, XmlCompoundSection
from Object import XmlObject

class XmlClass(XmlObject):
    def __init__(self,xmlnode):
        doc = ET.parse(xmlnode)
        root = doc.getroot()
        super().__init__(root.find('compounddef'))
        self.inherits = None
        self.inheritance_type = None
        self.name = self.xmlnode.findtext('compoundname')
        if self.containsField(self.xmlnode,'basecompoundref'):
            self.inherits = self.xmlnode.findtext('basecompoundref')
            self.inheritance_type = self.xmlnode.find('basecompoundref').get('prot')
        self.sections = [XmlSection(node) for node in self.xmlnode.findall('sectiondef')]
        self.print()
    
    def print(self):
        super().print()
        print("Object name: {0}\n Inherits: {1}".format(self.name,self.inherits))
        for section in self.sections:
            print("Section: {}".format(section.kind))
            for field in section.fields:
                print(field.print())
    
    
        
