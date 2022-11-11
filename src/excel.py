import numpy as np
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Color, PatternFill, Font, Border
from openpyxl.styles import colors
from openpyxl.cell import Cell
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
    def __init__(self):
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
                ]
    
        }
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



file = load_workbook('testfiles/SW_Unit_example.xlsx')
empty = Workbook()
worksheet = file.active
ws = empty.active
redFill = PatternFill(start_color='FFECF0F1',
                        end_color='FFECF0F1',
                   fill_type='solid')
row = 1
column = 1
tab = Table()
tab.inteface = "dsads"
print(tab.inteface)
tab.inteface = 'YES'
tab.unitname = 'someFunc'
tab.prototype = 'void someFunc(int a, double b)'
tab.parameters = ['int','a', '0...255', 'IN', "Desc"]
tab.parameters = ['double','b', '0...255', 'IN']
for k, v in tab.table.items():
    ws.cell(row, 1).value = k
    ws.cell(row,1).fill = redFill
    if type(v) == list:
        ws.merge_cells(start_row=row, start_column=1, end_row=row + len(v) - 1,end_column=1)
        for inner in v:
            for val in inner:
                col = column + 1
                ws.cell(row, col).value = val
                column +=1
            column = 1
            row+=1
        break

    ws.cell(row, 2).value = v
    row +=1

ws.merge_cells('A2')
empty.save("testfiles/sample.xlsx")
