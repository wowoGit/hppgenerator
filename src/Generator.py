from Class import *




class Generator:
    def __init__(self,xmlClass: XmlClass):
        self.xmlClass = xmlClass
        self.file = open(self.xmlClass.name + '.hpp','w') 
    
    def generateSection(self,file, section_protection:str, sections:XmlSection):
            self.file.write('{}:\n'.format(section_protection))
            for section in sections:
                for field in section.fields:
                    field_body = field.print()
                    self.file.write(field_body + ';\n')
    def generateLine(self,line : str):
        self.file.write(line + '\n')

    def generateClass(self):
        self.generateLine('#pragma once')
        if self.xmlClass.template is not None:
            self.generateLine(self.xmlClass.template)
        definition = 'class ' + self.xmlClass.name 
        if self.xmlClass.inherits is not None:
            definition += ': ' + self.xmlClass.inheritance_type + ' ' + self.xmlClass.inherits
        definition += ' {'

        if self.xmlClass.inherits == 'QObject': 
            self.generateLine('Q_OBJECT')

        self.generateLine(definition)
        public_sections = [section for section in self.xmlClass.sections if section.kind.startswith('public')]
        private_sections = [section for section in self.xmlClass.sections if section.kind.startswith('private')]
        protected_sections = [section for section in self.xmlClass.sections if section.kind.startswith('protected')]
        if len(public_sections) > 0:
            self.generateSection(self.file,'public',public_sections)
        if len(private_sections) > 0:
            self.generateSection(self.file,'private',private_sections)
        if len(protected_sections) > 0:
            self.generateSection(self.file,'protected',protected_sections)
        self.generateLine('};')
