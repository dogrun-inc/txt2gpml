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
    for i in filter(lambda inter: inter.get('has_anchor') == False, interactions):
        # interactionのidは i["ID"]で取得できる
        # interactionのstart, endのnodeのidは i["start_point"], i["end_point"]で取得できる
        # start_position, end_positionの(CenterX,CenterY)座標を渡す< nodes[id]
        iteraction_position[i["ID"]] = grxy.main(nodes[i["start_point"]], nodes[i["end_point"]])
        iteraction_position[i["ID"]]['start_point']['GraphRef'] = i['start_point']
        iteraction_position[i["ID"]]['end_point']['GraphRef'] = i['end_point']

    for i in filter(lambda inter: inter.get('has_anchor') == True, interactions):
        print("i", i)
        # endpointがanchorのid, anchorのendpointのstar,とend_pointの座標を渡す
        anchor = next(a for a in source['anchors'] if a['ID'] == i['end_point'])
        end_point = get_anchor_xy(iteraction_position[anchor['interaction']], float(i["position"]))
        iteraction_position[i["ID"]] = grxy.main(nodes[i["start_point"]], end_point, end_rel=False)
        iteraction_position[i["ID"]]['start_point']['GraphRef'] = i['start_point']
        iteraction_position[i["ID"]]['end_point']['GraphRef'] = i['end_point']

    return iteraction_position



