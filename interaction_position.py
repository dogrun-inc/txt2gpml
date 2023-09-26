# encoding: utf-8
from typing import Tuple
import get_rel_xy as grxy

def get_anchor_xy(start_xy: Tuple[float], end_xy: Tuple[float], relative_position: float) -> Tuple[float]:
    """
    Interactionの始点、終点と、Anchorの相対位置から、Anchorの座標を返す
    
    Args:
        start_xy (Tuple[float]): Interactionの始点のxy座標
        end_xy (Tuple[float]): Interactionの終点のxy座標
        relative_position (float): AnchorのInteraction内の相対位置
    
    Returns:
        Tuple[float]: Anchorのxy座標
    """
    return tuple[float](start_xy[i] + (end_xy[i] - start_xy[i]) * relative_position for i in (0, 1))



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
    print("indertaction", interactions)
    for i in filter(lambda inter: inter.get('anchor') == 'false', interactions):
        # interactionのidは i["ID"]で取得できる
        # interactionのstart, endのnodeのidは i["start_point"], i["end_point"]で取得できる
        # start_position, end_positionの(CenterX,CenterY)座標を渡す< nodes[id]
        iteraction_position[i["ID"]] = grxy.main(nodes[i["start_point"]], nodes[i["end_point"]])
        iteraction_position[i["ID"]]['start_point']['GraphRef'] = i['start_point']
        iteraction_position[i["ID"]]['end_point']['GraphRef'] = i['end_point']

    for i in filter(lambda inter: inter.get('anchor') == 'true', interactions):

        end_point = get_anchor_xy(nodes[i["start_point"]], iteraction_position[i["interaction"]]['end_point'], float(i["position"]))

    return iteraction_position



