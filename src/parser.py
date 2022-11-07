import xml.etree.ElementTree as ET








def main():
    tree = ET.parse('../testfiles/classActiveCallClient.xml')
    root = tree.getroot()
    for child in root:
        print(child.tag, child.attrib)
main()