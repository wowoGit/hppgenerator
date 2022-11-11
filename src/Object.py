from utils import *
import xml.etree.ElementTree as ET


class XmlObject:
    def __init__(self,node: ET.Element):
        self.xmlnode = node
        self.name = node.findtext('name')
        self.formBrief(self.xmlnode)
        self.formDetailed(self.xmlnode)
        self.formTemplate(self.xmlnode)

    def formTemplate(self,node: ET.Element):
        self.template = None
        if self.containsField(node,'templateparamlist'):
            templatelist = node.find('templateparamlist')
            self.template = "template< "
            for field in templatelist.getchildren():
                self.template += field.findtext('type') + ' '
                if self.containsField(field,'declname'):
                    self.template += field.findtext('declname') + ' '
            self.template += '>\n'
    def formBrief(self,node : ET.Element) :
        self.brief = None
        if self.containsField(self.xmlnode,'briefdescription'):
            brief_node = node.find('briefdescription')
            for field in brief_node.getchildren():
                self.brief = "@brief "
                if len(field.getchildren()) == 0:
                    self.brief += field.text
                else:
                    ref = field.getchildren()[0]
                    self.brief += str(field.text or '') + ref.text + ref.tail
    
    def formDetailed(self,node: ET.Element):
        self.detailed = []
        self.params = []
        self.returnval = {}
        if self.containsField(self.xmlnode,'detaileddescription'):
            detailed_node = node.find('detaileddescription')
            for para in detailed_node.getchildren():
                if self.containsField(para, 'parameterlist'):
                    for field in para.find('parameterlist').getchildren():
                            #param_name_list = item.getchildren()[0]
                            param_name = field.find('parameternamelist/parametername')
                            param_dir = param_name.get('direction')
                            param_name_text = param_name.text
                            param_desc_text = field.find('parameterdescription/para').text
                            self.xmlnode.findall('param')
                            param = [param for param in self.xmlnode.findall('param') if param.findtext('declname') ==param_name_text][0]
                            param_type = param.find('type')
                            param_type_text = param_type.text
                            if self.containsField(param_type,'ref'):
                                ref = param_type.find('ref')
                                param_type_text += ref.text + ref.tail
                            #TODO: ADD RANGES
                            self.params.append({'name': param_name_text, 'type': param_type_text, 'description': param_desc_text})
                            self.detailed.append("@param[{0}] {1} {2}".format(param_dir, param_name_text, param_desc_text))
                if self.containsField(para, "simplesect"):
                    simplesect = para.find('simplesect')
                    kind = simplesect.get('kind')
                    simplesect_text = simplesect.find('para').text
                    self.returnval['type'] = self.xmlnode.findtext('type')
                    self.returnval['description'] = simplesect_text
                    self.detailed.append("@{0} {1}".format(kind,simplesect_text))
        if self.detailed == "":
            self.detailed = None

                    

    def containsField(self,node: ET.Element, fieldname:str):
        if node.find(fieldname) is not None:
            return True
        return False

    def print(self) -> str:
        return ""

    def generateHpp(self):
        raise NotImplementedError()
