
import xml.etree.ElementTree as ET


class XmlObject:
    def __init__(self,node: ET.Element):
        self.xmlnode = node
        self.formBrief(self.xmlnode)
        self.formDetailed(self.xmlnode)

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
        self.detailed = ""
        if self.containsField(self.xmlnode,'detaileddescription'):
            detailed_node = node.find('detaileddescription')
            for para in detailed_node.getchildren():
                if self.containsField(para, 'parameterlist'):
                    for field in para.getchildren():
                        for item in field.getchildren():
                            param_name_list = item.getchildren()[0]
                            param_name = param_name_list[0]
                            param_dir = param_name.get('direction')
                            param_name_text = param_name.text
                            param_desc = item.find('parameterdescription/para').text
                            self.detailed += "@param[{0}] {1} {2}\n".format(param_dir, param_name_text, param_desc)
                if self.containsField(para, "simplesect"):
                    simplesect = para.getchildren()[0]
                    kind = simplesect.get('kind')
                    simplesect_text = simplesect.find('para').text
                    self.detailed +="@{0} {1}".format(kind,simplesect_text)
        if self.detailed == "":
            self.detailed = None

                    

    def containsField(self,node: ET.Element, fieldname:str):
        if node.find(fieldname) is not None:
            return True
        return False

    def print(self):
        print(self.brief,self.detailed)

    def generateHpp(self):
        raise NotImplementedError()
