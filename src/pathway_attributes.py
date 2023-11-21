# encoding: utf-8
import read_pathway_from_text
import node_position as np
import interaction_position as ip
import bfs_positions

def main(file:str):
    source_dict = read_pathway_from_text.main(file)
    # interactionにhas_anchorフラグを追加
    for idx, inter in enumerate(source_dict['interactions']):
        anchors = [a['GraphId'] for a in source_dict['anchors']]
        source_dict['interactions'][idx]['has_anchor'] =\
            (inter['start_point'] in anchors) or (inter['end_point'] in anchors)
    
    # layout optionが入力された場合（circo, dotなど）
    pathway_info =source_dict['pathway']
    if pathway_info.get('layout', None):
        node_position = np.main(source_dict)
    else:
        # use bfs layout module by default
        node_position = bfs_positions.main(file)
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
                    {'TextLabel': n['Label'], 'GraphId': n['GraphId'], 'BiologicalType': n['BiologicalType'], 'Color': n.get('Color', None),
                    'CenterX': str(node_position[n['GraphId']][0]), 'CenterY': str(node_position[n['GraphId']][1]), 'xref_id': n.get('Xref_id'), 'xref_db': n.get('Xref_db')}
                    for n in source_dict['nodes'] 
                ],
                'Interactions': [
                    {'GraphId': i['GraphId'], 'BiologicalType': i['BiologicalType'], 'LineStyle': i.get('LineStyle', None),
                     'Points': [
                           {'X': str(interaction_position[i['GraphId']]['start_point']['x']),
                            'Y': str(interaction_position[i['GraphId']]['start_point']['y']),
                            'RelX': interaction_position[i['GraphId']]['start_point']['RelX'],
                            'RelY': interaction_position[i['GraphId']]['start_point']['RelY'],
                            'GraphRef': interaction_position[i['GraphId']]['start_point']['GraphRef']},
                           {'X': str(interaction_position[i['GraphId']]['end_point']['x']),
                            'Y': str(interaction_position[i['GraphId']]['end_point']['y']),
                            'RelX': interaction_position[i['GraphId']]['end_point']['RelX'],
                            'RelY': interaction_position[i['GraphId']]['end_point']['RelY'],
                            'GraphRef': interaction_position[i['GraphId']]['end_point']['GraphRef']},
                     ]}
                    for i in source_dict['interactions'] if i.get("BiologicalType")
                ],
                'Anchors': [
                    {'Position': str(a['position']), 'GraphId': a['GraphId'], 'Interaction': a['interaction']}
                    for a in source_dict['anchors']
                ]
            }
    # if not value is defined, remove the key
    pathway['Nodes'] = [{key:value for key, value in n.items() if value is not None } for n in pathway['Nodes']]
    return pathway