import xml.etree.ElementTree as ET
from Object import XmlObject
import enum




"""
FieldType: method, attribute, property, typedef, enum
"""

class XmlField(XmlObject):
    def __init__(self, node : ET.Element):
        super().__init__(node)
    def removescope(self,node:ET.Element,full_def:str):
            class_name = node.get('id')[5:node.get('id').find('_')]
            namespace_end_pos = full_def.rfind('::')+2
            namespace_start_pos = full_def[:namespace_end_pos].rfind(class_name)
            stripped_def = full_def[:namespace_start_pos]
            return stripped_def



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


class XmlFieldFunc(XmlField):
    def __init__(self, node: ET.Element):
        super().__init__(node)
        
        self.definition = self.formDefinition(node)

    def formDefinition(self, node: ET.Element):
        func_def = ""
        full_def = node.find('definition').text
        func_name = node.find('name').text
        template = ""



        if self.containsField(node,'templateparamlist'):
            templatelist = node.find('templateparamlist')
            template = "template< "
            for field in templatelist.getchildren():
                template += field.findtext('type') + ' '
                if self.containsField(field,'declname'):
                    template += field.findtext('declname') + ' '
            template += '>\n'

        if full_def.startswith(func_name) or func_name.startswith('~'):
            func_def += ' ' + func_name
        else:
            stripped_def = self.removescope(node,full_def)
            func_def += stripped_def + func_name
        if self.containsField(node,'argsstring'):
            func_def += node.findtext('argsstring')
        func_def = template + func_def
        return func_def
            
    def print(self):
        print("-----------------------")
        print(self.brief)
        print(self.detailed)
        print(self.definition)

class XmlFieldVariable(XmlFieldFunc):
    def __init__(self, node: ET.Element):
        super().__init__(node)
        self.initializer = None
        if self.containsField(node,'initializer'):
            self.initializer = node.findtext('initializer')
            self.definition += ' ' + self.initializer
    
    def print(self):
        print("-----------------------")
        print(self.brief)
        print(self.detailed)
        print(self.definition)

FieldMapper  = {
    "signal": globals()["XmlFieldFunc"],
    "function": globals()['XmlFieldFunc'],
    "property": globals()['XmlFieldProperty'],
    "variable": globals()['XmlFieldVariable'],
    "typedef": globals()['XmlFieldVariable']
}
class FieldFactory():
    def GetField(fieldtype : str, node): 
        return FieldMapper[fieldtype](node)



class XMlElement(XmlObject):
    def __init__(self, node: ET.Element):
        super().__init__(node)
    def print(self):
        print(self.xmlnode.tag, self.xmlnode.text)

    def __str__(self) -> str:
        if self.xmlnode is not None and self.xmlnode.text != "":
            return self.xmlnode.tag.upper() + " " + self.xmlnode.text 
        return ""
