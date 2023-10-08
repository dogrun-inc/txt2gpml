# encoding: utf-8
import read_pathway_from_text as rpf
import node_position as nop
import interaction_position as ip
import bfs_positions as bfsp

def main(file:str):
    source_dict = rpf.main(file)
    
    # has_anchorフラグを追加
    for idx, inter in enumerate(source_dict['interactions']):
        anchors = [a['ID'] for a in source_dict['anchors']]
        source_dict['interactions'][idx]['has_anchor'] =\
            (inter['start_point'] in anchors) or (inter['end_point'] in anchors)
    
    # 擬似グラフを作成し、レイアウトしたノードの座標を取得する
    # if use bfs layout comment out this line
    # node_position = nop.main(source_dict)
    
    # bfsを利用する場合
    node_position = bfsp.main(file)
    print(node_position)
    # interactionのstart_point, end_pointの座標とRelXYを生成する
    interaction_position = ip.main(source_dict, node_position)
    print(interaction_position)

    max_x = max(p[0] for p in node_position.values())
    max_y = max(p[1] for p in node_position.values())
    pathway = { 'Pathway': {
                   'Name': source_dict['pathway']['name'],
                   'Organism': source_dict['pathway']['organism'],
                   'BoardWidth': str(max_x + 100),
                   'BoardHeight': str(max_y + 30),
                },
                'Nodes': [
                    {'TextLabel': n['Label'], 'GraphId': n['ID'], 'BiologicalType': n['BiologicalType'],
                    'CenterX': str(node_position[n['ID']][0]), 'CenterY': str(node_position[n['ID']][1])}
                    for n in source_dict['nodes'] if n.get("Label")
                ],
                'Interactions': [
                    {'GraphId': i['ID'], 'BiologicalType': i['BiologicalType'],
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