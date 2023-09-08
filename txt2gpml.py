import xmlschema
import json
from xml.etree.ElementTree import ElementTree as ET


xsd_path = './sample/GPML2021.xsd'
gpml2021schema = xmlschema.XMLSchema(xsd_path)
# dictをjsonに変換する
jsondata = {
    "Comment": "test Comment"
}


def simle_schema_test():
    schema_file = open("/Users/oec/Dropbox/workspace/bio/txt2gpml/sample/test_test2.xsd").read()
    schema = xmlschema.XMLSchema(schema_file)
    #jdata = xmlschema.to_json(xml_document = """<note>this is a Note text</note>""", schema = schema)
    #jsonData = json.dumps(jdata)
    jsn_txt = json.dumps({'note': 'this is a Note text','comment': 'this is a Comment text'})
    #xmldata = xmlschema.from_json(jsn_txt, schema=schema, preserve_root=True, namespaces={"": "urn:oasis:names:tc:emergency:cap:1.2"})
    xmldata = xmlschema.from_json(jsn_txt, schema=schema, preserve_root=True)
    ET(xmldata).write('./sample/test_test2.xml')


def most_simple_schema_test():
    """_summary_
    最もシンプルなスキーマでのテスト
    このテストは成功する
    """
    my_xsd = '<?xml version="1.0"?> <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"> <xs:element name="note" type="xs:string"/> </xs:schema>'
    # schemaはファイルでもよい
    schema_file = open("/Users/oec/Dropbox/workspace/bio/txt2gpml/sample/test_test_simple.xsd").read()
    schema = xmlschema.XMLSchema(schema_file)
    #schema = xmlschema.XMLSchema(my_xsd)
    data = json.dumps({'note': 'this is a Note text'})
    xml = xmlschema.from_json(data, schema=schema, preserve_root=True)
    ET(xml).write('./sample/simple_test.xml')

def main(jsondata):
    """
    gpmlをファイルとして書き出す
    """
    jsn = json.dumps(jsondata, indent=4)
    xml = xmlschema.from_json(jsn, xmlschema=gpml2021schema)
    ET(xml).write('test.xml', encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    #main(jsondata)
    simle_schema_test()
    #most_simple_schema_test()