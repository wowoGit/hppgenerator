import numpy as np
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.cell import Cell
from openpyxl.styles import Border, Color, Font, PatternFill, colors

from Class import XmlClass
from Field import *

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
class Table:
    def __init__(self,workbook: Workbook, xmlclass: XmlClass):
        self.workbook = workbook
        self.xmlclass = xmlclass
        self._interface = None
        self._unitname = None
        self._prototype = None
        self._parameters = None
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
                'Description': None

    
        }
    def toExcel(self,path):
        row = 1
        column = 2
        ws = self.workbook.active
        for section in self.xmlclass.sections:
            if section.kind.startswith('public'):
                for field in section.fields:
                    row += 3
                    self.inteface = 'YES'
                    self.unitname = field.name
                    self.prototype = field.definition
                    if len(field.returnval) > 0:
                        self.table['Return Type'].append([field.returnval['type'], 'Range 1-10'] )
                        self.table['Description'] = field.returnval['description']
                    for param in field.params:
                        self.parameters = [param['type'], param['name'], 'Range 1-10', 'IN', param['description']]
                    
                    for k, v in self.table.items():
                        ws.cell(row, 1).value = k
                        if type(v) == list:
                            ws.merge_cells(start_row=row, start_column=1, end_row=row + len(v) - 1,end_column=1)
                            for inner in v:
                                for val in inner:
                                    ws.cell(row, column).value = val
                                    column += 1
                                column = 2
                                row+=1
                            continue
                        ws.cell(row, column).value = v
                        row +=1
        self.workbook.save(path)

    def _get_interface(self):
        return self.table.get('Interface')

    def _set_interface(self, value):
        self.table['Interface'] = value

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


    inteface = property(
        fget=_get_interface,
        fset=_set_interface,
        doc="The interface property."
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




