# encoding: utf-8
import read_pathway_from_text as rpft
import node_position as nop
import interaction_position as ip
import bfs_positions as bfsp

def main(file:str):
    source_dict = rpft.main(file)
    
    # interactionにhas_anchorフラグを追加
    for idx, inter in enumerate(source_dict['interactions']):
        anchors = [a['ID'] for a in source_dict['anchors']]
        source_dict['interactions'][idx]['has_anchor'] =\
            (inter['start_point'] in anchors) or (inter['end_point'] in anchors)
    
    # layout optionが入力された場合（circo, dotなど）
    pathway_info =source_dict['pathway']
    if pathway_info.get('layout', None):
        node_position = nop.main(source_dict)
    else:
        # use bfs layout module by default
        node_position = bfsp.main(file)
    # interactionのstart_point, end_pointの座標とRelXYを生成する
    interaction_position = ip.main(source_dict, node_position)

    max_x = max(p[0] for p in node_position.values())
    max_y = max(p[1] for p in node_position.values())
    pathway = { 'Pathway': {
                   'Name': pathway_info['name'],
                   'Organism': pathway_info['organism'],
                   'Layout': pathway_info.get('layout', None),
                   'BoardWidth': str(max_x + 200),
                   'BoardHeight': str(max_y + 100),
                },
                'Nodes': [
                    {'TextLabel': n['Label'], 'GraphId': n['ID'], 'BiologicalType': n['BiologicalType'], 'Color': n['Color'],
                    'CenterX': str(node_position[n['ID']][0]), 'CenterY': str(node_position[n['ID']][1])}
                    if n.get("Label") and n.get("Color")
                    else 
                    {'TextLabel': n['Label'], 'GraphId': n['ID'], 'BiologicalType': n['BiologicalType'],
                    'CenterX': str(node_position[n['ID']][0]), 'CenterY': str(node_position[n['ID']][1])}
                    for n in source_dict['nodes'] 
                ],
                'Interactions': [
                    {'GraphId': i['ID'], 'BiologicalType': i['BiologicalType'], 'LineStyle': i.get('LineStyle', None),
                     'Points': [
                           {'X': str(interaction_position[i['ID']]['start_point']['x']),
                            'Y': str(interaction_position[i['ID']]['start_point']['y']),
                            'RelX': interaction_position[i['ID']]['start_point']['RelX'],
                            'RelY': interaction_position[i['ID']]['start_point']['RelY'],
                            'GraphRef': interaction_position[i['ID']]['start_point']['GraphRef']},
                           {'X': str(interaction_position[i['ID']]['end_point']['x']),
                            'Y': str(interaction_position[i['ID']]['end_point']['y']),
                            'RelX': interaction_position[i['ID']]['end_point']['RelX'],
                            'RelY': interaction_position[i['ID']]['end_point']['RelY'],
                            'GraphRef': interaction_position[i['ID']]['end_point']['GraphRef']},
                     ]}
                    for i in source_dict['interactions'] if i.get("BiologicalType")
                ],
                'Anchors': [
                    {'Position': str(a['position']), 'GraphId': a['ID'], 'Interaction': a['interaction']}
                    for a in source_dict['anchors']
                ]
            }

    return pathway

if __name__ == "__main__":
    main("sample/simple_metabolite_text.txt")