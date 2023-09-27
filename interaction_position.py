# encoding: utf-8
from typing import Tuple
import get_rel_xy as grxy

def get_anchor_xy(interaction_position: dict, relative_position: float) -> Tuple[float]:
    """
    Interactionの始点、終点と、Anchorの相対位置から、Anchorの座標を返す
    
    Args:
        start_xy (Tuple[float]): Interactionの始点のxy座標
        end_xy (Tuple[float]): Interactionの終点のxy座標
        relative_position (float): AnchorのInteraction内の相対位置
    
    Returns:
        Tuple[float]: Anchorのxy座標
    """
    start_point = interaction_position['start_point']
    end_point = interaction_position['end_point']
    return tuple[float](start_point[i] + (end_point[i] - start_point[i]) * relative_position for i in ('x', 'y'))


def main(source: dict, nodes:dict):
    """
    - source_dictからinteractionを抽出し、さらにinteractionのstart_point, end_pointの各座標をノードの座標から生成する
    - 最終的にinteractionのstart_point, end_pointのX,Y座標,RelX,RelYを返す

    Args:
        nodes (dict): nodeのCenterX,CenterYを含むdict
    Returns:
        dict: interactionのstart_point, end_pointのX,Y座標
    """
    interactions = source["interactions"]
    iteraction_position = {}
    # pathway_attributesの最終出力にどちらの両端にもanchorを持たないinteractionの情報の追加
    for i in filter(lambda inter: inter.get('has_anchor') == False, interactions):
        # interactionのidは i["ID"]で取得できる
        # interactionのstart, endのnodeのidは i["start_point"], i["end_point"]で取得できる
        # start_position, end_positionの(CenterX,CenterY)座標を渡す< nodes[id]
        iteraction_position[i["ID"]] = grxy.main(nodes[i["start_point"]], nodes[i["end_point"]])
        iteraction_position[i["ID"]]['start_point']['GraphRef'] = i['start_point']
        iteraction_position[i["ID"]]['end_point']['GraphRef'] = i['end_point']

    print("iteraction position: ", iteraction_position)
    # pathway_attributesの最終出力にanchorを持つinteractionの情報の追加
    for i in filter(lambda inter: inter.get('has_anchor') == True, interactions):
        print("i: ", i)
        
        anchor = next(a for a in source['anchors'] if a['ID'] == i['end_point'])
        print("anchor: ", anchor)
        # anchorの座標を取得する。anchorの置かれたinteractionの両端の座標　と相対位置を引数にする
        # anchorはinteractionのend_pointに置くように運用的に固定する
        # start_point, end_pointそれぞれのx,y座標（{'start_point': {'x': 62.497, 'y': 162.0, 'RelX': 0, 'RelY': -1, 'GraphRef': 'n0001'}, 'end_point': {'x': 32.497, 'y': 90.0, 'RelX': 0, 'RelY': 1, 'GraphRef': 'n0002'}）を渡す
        # 第二引数としてanchorの相対位置（position）を渡す
        end_point = get_anchor_xy(iteraction_position[anchor['interaction']], float(anchor["position"]))

        iteraction_position[i["ID"]] = grxy.main(nodes[i["start_point"]], end_point, end_rel=False)
        iteraction_position[i["ID"]]['start_point']['GraphRef'] = i['start_point']
        iteraction_position[i["ID"]]['end_point']['GraphRef'] = i['end_point']

    return iteraction_position



