#!/usr/bin/env python3
import types
import xml.etree.ElementTree as ET
import openpyxl
import glob
import os
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, PatternFill, Side
import argparse

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
def str_if_none(val):
    return val or ''
def unpack_ref(node: ET.Element):
    ref = node[0]
    return str_if_none(node.text) + ref.text + str_if_none(ref.tail)
def removescope(name :str):
    namespace_end = name.find('::')
    return name[namespace_end+2:] if namespace_end != -1 else name
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
                if self.containsField(field,'ref'):
                    ref = field.getchildren()[0]
                    self.brief += str(field.text or '') + ref.text + ref.tail
                else:
                    self.brief = field.text
    
    def formDetailed(self):
        def getRange(string: str):
            if param_desc_text.__contains__('Range'):
                range_keyword_start = param_desc_text.find('Range')
                range_end = param_desc_text[range_keyword_start:].find('.') + range_keyword_start
                range_text = param_desc_text[range_keyword_start + len('Range '):range_end]
                stripped_string = string[:range_keyword_start] + string[range_end+1:]
                return stripped_string,range_text


        self.params_desc = {}
        self.returnval = {}
        if self.containsField(self.xmlnode,'detaileddescription'):
            detailed_node = self.xmlnode.find('detaileddescription')
            for para in detailed_node.getchildren():
                if self.containsField(para, 'parameterlist'):
                    for field in para.find('parameterlist').getchildren():
                            param_name = field.find('parameternamelist/parametername')
                            param_name_text = param_name.text
                            param_dir = param_name.get('direction')
                            param_desc_text = field.find('parameterdescription/para').text
                            range_text = None
                            if param_desc_text.__contains__('Range'):
                                param_desc_text,range_text = getRange(param_desc_text)
                            self.xmlnode.findall('param')
                            param = [param for param in self.xmlnode.findall('param') if param.findtext('declname') ==param_name_text][0]
                            param_type = param.find('type')
                            param_type_text = param_type.text or ''
                            if self.containsField(param_type,'ref'):
                                param_type_text += unpack_ref(param_type)
                            self.params_desc[param_name_text] = { 'value/range':range_text, "direction":'IN', 'description': param_desc_text}
                if self.containsField(para, "simplesect"):
                    simplesect = para.find('simplesect')
                    simplesect_text = simplesect.find('para').text
                    if self.containsField(simplesect.find('para'),'ref'):
                        simplesect_text += unpack_ref(param_type)
                    range_text = None
                    if simplesect_text.__contains__('Range'):
                        simplesect,range_text = getRange(simplesect)
                    if self.containsField(self.xmlnode.find('type'),'ref'):
                        self.returnval['type'] = unpack_ref(self.xmlnode.find('type'))
                    else:
                        self.returnval['type'] = self.xmlnode.findtext('type')
                    self.returnval['description'] = simplesect_text
                    self.returnval['range/value'] = range_text

                    

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
        self.formParams()

    def formParams(self):
        self.params = []
        for param in self.xmlnode.findall('param'):
            param_name = param.findtext('declname')
            param_type = param.findtext('type')
            self.params.append({
             'name':param_name,
             'type':param_type,
             'description': self.params_desc.get(param_name,dict()).get('description'),
             'value/range':self.params_desc.get(param_name,dict()).get('value/range'),
             'direction':self.params_desc.get(param_name,dict()).get('direction'),
             })

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
        self.name = removescope(self.xmlnode.findtext('compoundname'))
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
        self.header = 'Software Unit Information'
        self.table = {
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

    def fillForm(self,field:XmlFieldFunc):
        form = TableForm()
        form.inteface = 'YES' if field.protection == 'public' else 'NO'
        form.unitname = field.name
        form.prototype = field.definition
        form.return_description = field.brief
        if len(field.returnval) > 0:
            form.returntype = [field.returnval['type'], field.returnval['range/value']]
        else:
                form.returntype = ['-','-']
        if len(field.params) > 0:
            for param in field.params:
                form.parameters = [param['type'], param['name'], param['value/range'], param['direction'], param['description']]
        else:
                form.parameters = ['-','-','-','-','-',]
        return form

    def toExcel(self):
        row = 1
        column = 2
        ws = self.workbook.create_sheet(self.xmlclass.name)
        for section in self.xmlclass.sections:
            if section.kind in export_to_excel:
                for field in section.fields:
                    form = self.fillForm(field) 
                    table_start_row = row
                    ws.cell(row,1).value = form.header
                    ws.cell(row=row, column=1).border = self.border
                    ws.cell(row=row, column=1).fill = self.cellFill
                    ws.merge_cells(start_row=row, start_column=1, end_row=row,end_column=6)
                    ws.cell(row=row,column=1).alignment = Alignment(horizontal='center')
                    row += 1
                    for k, v in form.table.items():
                        ws.cell(row, 1).value = k
                        ws.cell(row,1).fill = self.cellFill
                        ws.cell(row,1).border = self.border
                        ws.cell(row,1).alignment = Alignment(horizontal='center')
                        if type(v) == list:
                            ws.merge_cells(start_row=row, start_column=1, end_row=row + len(v) - 1,end_column=1)
                            row_old = row
                            for inner in v:
                                for val in inner:
                                    if val in v[0]:
                                        ws.cell(row, column).fill = self.cellFill
                                    ws.cell(row, column).border = self.border
                                    ws.cell(row, column).value = val
                                    column += 1
                                    if k == 'Return Type' or k == 'Global Variables':
                                        column +=1
                                column = 2
                                row+=1
                            if k == 'Return Type' or k == 'Global Variables':
                                merge_row = row_old
                                while merge_row < row:
                                    ws.merge_cells(start_row=merge_row, start_column=2, end_row=merge_row,end_column = 3)
                                    ws.merge_cells(start_row=merge_row, start_column=4, end_row=merge_row,end_column = 6)
                                    merge_row += 1
                        else:
                            ws.cell(row, column).value = v
                            ws.cell(row,column).border = self.border
                            ws.merge_cells(start_row=row, start_column=2, end_row=row,end_column = 6)
                            row +=1

                    self.setBorder(row_start = table_start_row, row_end=row-1,col_start=1,col_end=6,border=self.border)
                    row += 3

    def setBorder(self, row_start, row_end, col_start, col_end,border : Border):
        ws = self.workbook.active
        for row in ws.iter_rows(min_row=row_start, min_col=col_start, max_row=row_end, max_col=col_end):
            for cell in row:
                cell.border = border


def main():
    parser = argparse.ArgumentParser(
                    prog = 'ProgramName',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
    parser.add_argument("-d", "--Directory",dest="directory", help = "Starting directory",required=True)
    args = parser.parse_args()
    files = [file for file in glob.glob(args.directory + '/*.xml') if os.path.basename(file).startswith('class') == True]
    #gen = Generator(vehicledata)
    wb = Workbook()
    for file in files:
        xmlclass = XmlClass(file)
        tbl = Table(wb,xmlclass)
        tbl.toExcel()
    wb.save('../testfiles/sample.xlsx')
if __name__ == '__main__':
    main()


