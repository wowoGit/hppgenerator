#!/usr/bin/env python3
from Class import XmlClass
from Generator import Generator


def main():
    vehicledata = XmlClass("/home/vsildirian/etc/hppgenerator/testfiles/xml/classVehicleDataClient.xml")
    gen = Generator(vehicledata)
    gen.generateClass()
    activecall = XmlClass("/home/vsildirian/etc/hppgenerator/testfiles/xml/classActiveCallClient.xml")
    gen = Generator(activecall)
    gen.generateClass()
    proxy = XmlClass("/home/vsildirian/etc/hppgenerator/testfiles/xml/classProxy.xml")
    gen = Generator(proxy)
    gen.generateClass()

main()