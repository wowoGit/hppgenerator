import xml.etree.ElementTree as ET
from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.styles import Border,Side, PatternFill, Alignment

export_to_excel = [
    'public-func',
    'public-slot',
    'signal',
    'event',
    'public-static-func',
    'protected-func',
    'protected-static-func',
    'protected-slot',
    'private-func',
    'private-static-func',
    'friend',
    'prototype'
]
class XmlObject:
    def __init__(self,node: ET.Element):
        self.xmlnode = node
        self.name = node.findtext('name')
        self.formBrief()
        self.formDetailed()
        self.formTemplate()

    def formTemplate(self):
        self.template = None
        if self.containsField(self.xmlnode,'templateparamlist'):
            templatelist = self.xmlnode.find('templateparamlist')
            self.template = "<"
            for field in templatelist.getchildren():
                self.template += field.findtext('type') + ' '
                if self.containsField(field,'declname'):
                    self.template += ' ' + field.findtext('declname')
            self.template += '>'
    def formBrief(self) :
        self.brief = None
        if self.containsField(self.xmlnode,'briefdescription'):
            brief_node = self.xmlnode.find('briefdescription')
            for field in brief_node.getchildren():
                self.brief = ''
                if len(field.getchildren()) == 0:
                    self.brief = field.text
                else:
                    ref = field.getchildren()[0]
                    self.brief += str(field.text or '') + ref.text + ref.tail
    
    def formDetailed(self):
        self.detailed = []
        self.params = []
        self.returnval = {}
        if self.containsField(self.xmlnode,'detaileddescription'):
            detailed_node = self.xmlnode.find('detaileddescription')
            for para in detailed_node.getchildren():
                if self.containsField(para, 'parameterlist'):
                    for field in para.find('parameterlist').getchildren():
                            #param_name_list = item.getchildren()[0]
                            param_name = field.find('parameternamelist/parametername')
                            param_dir = param_name.get('direction')
                            param_name_text = param_name.text
                            param_desc_text = field.find('parameterdescription/para').text
                            range_text = None
                            if param_desc_text.__contains__('Range'):
                                range_keyword_start = param_desc_text.find('Range')
                                range_end = param_desc_text[range_keyword_start:].find('.') + range_keyword_start
                                range_text = param_desc_text[range_keyword_start + len('Range '):range_end]
                                param_desc_text = param_desc_text[:range_keyword_start] + param_desc_text[range_end+1:]

                            self.xmlnode.findall('param')
                            param = [param for param in self.xmlnode.findall('param') if param.findtext('declname') ==param_name_text][0]
                            param_type = param.find('type')
                            param_type_text = param_type.text
                            if self.containsField(param_type,'ref'):
                                ref = param_type.find('ref')
                                param_type_text += ref.text + ref.tail
                            self.params.append({'name': param_name_text, 'type': param_type_text, 'value/range':range_text,"direction":'IN', 'description': param_desc_text})
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


class XmlField(XmlObject):
    def __init__(self, node : ET.Element):
        super().__init__(node)
        self.protection = node.get('prot')
    def removescope(self,full_def:str):
            class_name = self.xmlnode.get('id')[5:self.xmlnode.get('id').find('_')]
            namespace_start_pos = full_def.find(class_name)
            first = full_def[:namespace_start_pos]
            second = full_def[full_def.rfind('::')+2:]
            stripped_def = first + second
            return stripped_def

class XmlFieldFunc(XmlField):
    def __init__(self, node: ET.Element):
        super().__init__(node)
        self.formDefinition()

    def formDefinition(self):
        func_def = ""
        full_def = self.xmlnode.find('definition').text
        func_name = self.xmlnode.find('name').text
        self.name = func_name

        if full_def.startswith(func_name) or func_name.startswith('~'):
            if self.xmlnode.get('explicit') == 'yes':
                func_def += 'explicit '
            func_def += func_name
        else:
            stripped_def = self.removescope(full_def)
            func_def += stripped_def 
        if self.containsField(self.xmlnode,'argsstring'):
            func_def += self.xmlnode.findtext('argsstring')
        if self.template is not None:
            arg_pos = func_def.find('(')
            func_def = func_def[:arg_pos] + self.template + func_def[arg_pos:]
            self.name +=self.template
        self.definition = func_def
class XmlSection(XmlObject):
    def __init__(self,xmlnode: ET.Element):
        super().__init__(xmlnode)
        self.kind = xmlnode.get('kind')
        self.fields = [XmlFieldFunc(node) for node in self.xmlnode.findall('memberdef')]


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
        self.sections = [XmlSection(node) for node in self.xmlnode.findall('sectiondef') if node.get('kind') in export_to_excel]
    


           
class TableForm:
    def __init__(self) -> None:
        self._interface = None
        self._unitname = None
        self._prototype = None
        self._parameters = None
        self._returnval = None
        self._return_description = None
        self.table = {
    
                "Software Unit Information" : None,
                "Interface" : None,
                "Unit Name": None,
                "Prototype" : None,
                "Parameters": [
                    [
                        "Type", "Name", "Value/Range", "IN/OUT", "Description",
                    ],
                ],
                'Return Type': [
                    [
                    'Type', 'Value/Range'
                    ]
                ],
                'Description': None,
                'Global Variables': [
                    ['Name', 'Read/Write'],
                    ['-', '-']
                ],
                'Called Function': '-',
                'Calling Function': '-',
                'Execution Time': '-'

    
        }
    

    def _get_interface(self):
        return self.table.get('Interface')

    def _set_interface(self, value):
        self.table['Interface'] = value

    def _get_returntype(self):
        return self.table.get('Return Type')

    def _set_returntype(self, value):
        if len(self.table['Return Type']) > 1:
            self.table['Return Type'][1] = value
            return
        
        self.table['Return Type'].append(value)


    def _get_unitname(self):
        return self.table.get('Unit Name')

    def _set_unitname(self, value):
        self.table['Unit Name'] = value

    def _get_prototype(self):
        return self.table.get('Prototype')

    def _set_prototype(self, value):
        self.table['Prototype'] = value

    def _get_parameters(self):
        return self.table.get('Parameters')

    def _set_parameters(self, value):
        self.table['Parameters'].append(value)

    def _get_description(self):
        return self.table.get('Description')

    def _set_description(self, value):
        self.table['Description'] = value

    inteface = property(
        fget=_get_interface,
        fset=_set_interface,
        doc="The interface property."
    )
    return_description = property(
        fget=_get_description,
        fset=_set_description,
        doc="The return description property."
    )
    returntype = property(
        fget=_get_returntype,
        fset=_set_returntype,
        doc="The return type property."
    )
    unitname = property(
        fget=_get_unitname,
        fset=_set_unitname,
        doc="The Unit Name property."
    )
    prototype = property(
        fget=_get_prototype,
        fset=_set_prototype,
        doc="The prototype property."
    )
    parameters = property(
        fget=_get_parameters,
        fset=_set_parameters,
        doc="The parameters property."
    )
class Table:
    def __init__(self,workbook: Workbook, xmlclass: XmlClass):
            self.workbook = workbook
            self.xmlclass = xmlclass
            self.border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))
            self.cellFill = PatternFill(start_color='FFB2B2B2',
                                    end_color='FFB2B2B2',
                                    fill_type='solid')

    def toExcel(self,path):
        row = 1
        column = 2
        ws = self.workbook.create_sheet(self.xmlclass.name)
        for section in self.xmlclass.sections:
            if section.kind in export_to_excel:
                for field in section.fields:
                    table_start_row = row
                    rowform = TableForm()
                    rowform.inteface = 'YES' if field.protection == 'public' else 'NO'
                    rowform.unitname = field.name
                    rowform.prototype = field.definition
                    rowform.return_description = field.brief
                    if len(field.returnval) > 0:
                        rowform.returntype = [field.returnval['type'], 'Range 1-10']
                    else:
                            rowform.returntype = ['-','-']
                    if len(field.params) > 0:
                        for param in field.params:
                            rowform.parameters = [param['type'], param['name'], param['value/range'], param['direction'], param['description']]
                    else:
                            rowform.parameters = ['-','-','-','-','-',]
                    for k, v in rowform.table.items():
                        ws.cell(row, 1).value = k
                        ws.cell(row,1).fill = self.cellFill
                        ws.cell(row,1).border = self.border
                        ws.cell(row,1).alignment = Alignment(horizontal='center')
                        if type(v) == list:
                            ws.merge_cells(start_row=row, start_column=1, end_row=row + len(v) - 1,end_column=1)
                            row_old = row
                            for inner in v:
                                for val in inner:
                                    ws.cell(row, column).value = val
                                    column += 1
                                column = 2
                                row+=1
                            if k == 'Return Type' or k == 'Global Variables':
                                merge_row = row_old
                                while merge_row < row:
                                    ws.merge_cells(start_row=merge_row, start_column=2, end_row=merge_row,end_column = 3)
                                    ws.merge_cells(start_row=merge_row, start_column=4, end_row=merge_row,end_column = 6)
                                    merge_row += 1
                            continue
                        ws.cell(row, column).value = v
                        ws.cell(row,column).border = self.border
                        ws.merge_cells(start_row=row, start_column=2, end_row=row,end_column = 6)
                        row +=1
                    self.setBorder(row_start = table_start_row, row_end=row-1,col_start=1,col_end=6,border=self.border)
                    row += 3

        self.workbook.save(path)
    def setBorder(self, row_start, row_end, col_start, col_end,border : Border):
        ws = self.workbook.active
        for row in ws.iter_rows(min_row=row_start, min_col=col_start, max_row=row_end, max_col=col_end):
            for cell in row:
                cell.border = border


def main():
    vehicledata = XmlClass("/home/vsildirian/etc/hppgenerator/testfiles/xml/classVehicleDataClient.xml")
    #gen = Generator(vehicledata)
    wb = Workbook()

    tbl = Table(wb,vehicledata)
    tbl.toExcel("testfiles/sample.xlsx")

if __name__ == '__main__':
    main()


