import xmlschema
import json
import xml.etree.ElementTree as ET
import datetime
import pathway_attributes

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
    ET.ElementTree(xmldata).write('./sample/test_test2.xml')


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
    ET.ElementTree(xml).write('./sample/simple_test.xml')


def dict2etree(pathway):
    """
    Pathway の情報を持った Dict から、GPML のもととなる ElementTree を返す

    Args:
        pathway (Dict[Dict[str, Any]): Pathway の情報を持った Dict

    Returns:
        ElementTree: GPML のもととなる ElementTree
    """
    print(pathway)
    root = ET.Element('Pathway')
    root.set('xmlns', 'http://pathvisio.org/GPML/2013a')
    root.set('Name', pathway['Pathway']['Name'])
    root.set('Version', datetime.datetime.now().strftime('%Y%m%d'))
    root.set('Organism', pathway['Pathway']['Organism'])

    graphics = ET.SubElement(root, 'Graphics')
    graphics.set('BoardWidth', pathway['Pathway']['BoardWidth'])
    graphics.set('BoardHeight', pathway['Pathway']['BoardHeight'])

    for node in pathway['Nodes']:
        data_node = ET.SubElement(root, 'DataNode')
        data_node.set('TextLabel', node['TextLabel'])
        data_node.set('GraphId', node['GraphId'])
        data_node.set('Type', node['BiologicalType'])

        data_graphics = ET.SubElement(data_node, 'Graphics')
        data_graphics.set('CenterX', str(node['CenterX']))
        data_graphics.set('CenterY', str(node['CenterY']))
        data_graphics.set('Width', '150.0')  # TODO: 暫定で固定、必要に応じて座標系から取得
        data_graphics.set('Height', '25.0')
        data_graphics.set('ZOrder', '32768')
        data_graphics.set('FontSize', '12')
        data_graphics.set('Valign', 'Middle')
        # data_graphics.set('Color', '0000ff')

        data_xref = ET.SubElement(data_node, 'Xref')
        data_xref.set('Database', '')
        data_xref.set('ID', '')

    for interaction in pathway['Interactions']:
        int_root = ET.SubElement(root, 'Interaction')
        int_root.set('GraphId', interaction['GraphId'])

        int_graphics = ET.SubElement(int_root, 'Graphics')
        int_graphics.set('ZOrder', '12288')
        int_graphics.set('LineThickness', '1.0')

        for index, point in enumerate(interaction['Points']):
            int_point = ET.SubElement(int_graphics, 'Point')
            int_point.set('X', str(point['X']))
            int_point.set('Y', str(point['Y']))
            int_point.set('GraphRef', point['GraphRef'])
            int_point.set('RelX', str(point['RelX']))
            int_point.set('RelY', str(point['RelY']))
            if index == 1:
                int_point.set('ArrowHead', interaction['BiologicalType'])

        data_xref = ET.SubElement(int_root, 'Xref')
        data_xref.set('Database', '')
        data_xref.set('ID', '')

        anchors = list(filter(lambda a: a['interaction'] == interaction['ID'], pathway['Anchors']))
        if len(anchors) == 0:
            continue

        for anchor in anchors:
            int_anchor = ET.SubElement(int_graphics, 'Anchor')
            int_anchor.set('Position', str(anchor['Position']))
            int_anchor.set('GraphId', anchor['GraphId'])
            int_anchor.set('Shape', 'None')

    return root


def main(jsondata):
    """
    gpmlをファイルとして書き出す
    """
    jsn = json.dumps(jsondata, indent=4)
    xml = xmlschema.from_json(jsn, xmlschema=gpml2021schema)
    ET.ElementTree(xml).write('test.xml', encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    root = dict2etree(pathway_attributes.main("sample/simple_metabolite_text.txt"))
    print(root)
    #main(jsondata)
    #simle_schema_test()
    #most_simple_schema_test()