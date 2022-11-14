import numpy as np
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.cell import Cell
from openpyxl.styles import Border, Color, Font, PatternFill, colors

from Class import XmlClass
from Field import *
from utils import export_to_excel

table = {
    
        "Software Unit Information" : None,
        "Interface" : "YES",
        "Unit Name": "someMethod",
        "Prototype" : "void someMethod(int a, double b)",
        "Parameters": [
            [
                "Type", "Name", "Value/Range", "IN/OUT", "Description",
            ],
            [
                "int", "a", "0-255", "IN", "First parameter",
            ],
            [
                "double", "b", "0-255", "IN", "Second parameter",
            ],
        ]
    
}
class TableForm:
    def __init__(self) -> None:
        self._interface = None
        self._unitname = None
        self._prototype = None
        self._parameters = None
        self._returnval = None
        self._returndescription = None
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
        self.merge_rules = {
            'Software Unit Unformation':{'row':0,'col':6},
            'Interface':{'row':0,'col':6},
            'Software Unit Unformation':{'row':0,'col':6},
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
    returndescription = property(
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
    def toExcel(self,path):
        row = 1
        column = 2
        ws = self.workbook.active
        for section in self.xmlclass.sections:
            if section.kind in export_to_excel:
                for field in section.fields:
                    row += 3
                    rowform = TableForm()
                    rowform.inteface = 'YES' if field.protection == 'public' else 'NO'
                    rowform.unitname = field.name
                    rowform.prototype = field.definition
                    if len(field.returnval) > 0:
                        rowform.returntype = [field.returnval['type'], 'Range 1-10']
                        rowform.returndescription = field.returnval['description']
                    if len(field.params) > 0:
                        for param in field.params:
                            rowform.parameters = [param['type'], param['name'], param['value/range'], param['direction'], param['description']]
                    else:
                            rowform.parameters = ['-','-','-','-','-',]
                    
                    ws.merge_cells(start_row=row, start_column=1, end_row=row,end_column=6)
                    for k, v in rowform.table.items():
                        ws.cell(row, 1).value = k
                        if type(v) == list:
                            ws.merge_cells(start_row=row, start_column=1, end_row=row + len(v) - 1,end_column=1)
                            row_old = row
                            col_old = column
                            for inner in v:
                                for val in inner:
                                    ws.cell(row, column).value = val
                                    column += 1
                                column = 2
                                row+=1
                            if k == 'Return Type' or k == 'Global Variables':
                                merge_row = row_old
                                while merge_row < row:
                                    ws.merge_cells(start_row=row_old, start_column=2, end_row=row_old,end_column = 3)
                                    ws.merge_cells(start_row=row_old, start_column=4, end_row=row_old,end_column = 6)
                                    merge_row += 1
                            continue
                        ws.cell(row, column).value = v
                        ws.merge_cells(start_row=row, start_column=2, end_row=row,end_column = 6)
                        row +=1
        self.workbook.save(path)





