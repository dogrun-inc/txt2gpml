# encoding: utf-8

def anchor_relative_position(startpoint:set, endpoint:set, anchorpoint:set) -> int:
    """
    インテラクション（start,end）のポジションとanchorのポジションからanchorの相対値をもとめる
    Args:
        startpoint: interactionのstart座標(x,y)
        endpoint: interactionのend座標(x,y)
        anchorpoint: anchorの座標(x,y)
    Returns:
        Int: anchorの相対位置
    """
    node1_node2_pos = (startpoint, endpoint)
    anchor_pos = anchorpoint
    node1_node2_dist = sum((p2 - p1) ** 2 for p1, p2 in zip(*node1_node2_pos)) ** 0.5
    node1_anchor_dist = sum((p2 - p1) ** 2 for p1, p2 in zip(node1_node2_pos[0], anchor_pos)) ** 0.5
    return node1_anchor_dist / node1_node2_dist