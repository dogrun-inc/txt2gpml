import xmlschema
import json
from xml.etree.ElementTree import ElementTree as ET


xsd_path = './data/GPML2021.xsd'
gpml2021schema = xmlschema.XMLSchema(xsd_path)

# dictをjsonに変換する
jsondata = ""
xml = xmlschema.from_json(jsondata, xmlschema=gpml2021schema)

ET(xml).write('test.xml', encoding='utf-8', xml_declaration=True)