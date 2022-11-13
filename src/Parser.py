#!/usr/bin/env python3
from Class import XmlClass
from Generator import Generator
from excel import *


def main():
    vehicledata = XmlClass("/home/vsildirian/etc/hppgenerator/testfiles/xml/classVehicleDataClient.xml")
    #gen = Generator(vehicledata)
    wb = Workbook()

    tbl = Table(wb,vehicledata)
    tbl.toExcel("testfiles/sample.xlsx")
    #gen.generateClass()
    #vehicledata.print()
    #activecall = XmlClass("/home/vsildirian/etc/hppgenerator/testfiles/xml/classActiveCallClient.xml")
    #gen = Generator(activecall)
    #gen.generateClass()
    #proxy = XmlClass("/home/vsildirian/etc/hppgenerator/testfiles/xml/classProxy.xml")
    #gen = Generator(proxy)
    #gen.generateClass()

main()