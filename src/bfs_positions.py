import networkx as nx
import math
from typing import Tuple, List

import read_pathway_from_text as rpf


# Todo:stage_width, stage_heightはレイアウト情報から算出する
min_stage_width = 400
min_stage_height = 400
stage_margin = 150
interaction_length = 200

def layer_index(g, nodes, root_node) -> dict:
    """
    ノード同士のインタラクションがある各ノードの相対的な位置情報
    （layerの番号、layer中のインデックス）をBFSで算出し返す
    
    Returns:
        List[dict]:[{name(str), layer(int), indx(int)},,]
    """
    layers = dict(enumerate(nx.bfs_layers(g, [root_node])))
    relative_position = []
    for node in nodes:
        # 各ノードのlayerとindexを取得
        layer = next(filter(lambda item:  node in item[1], layers.items()), None)
        # index取得
        if layer:
            i = layer[1].index(node)
            total = len(layer[1])
            relative_position.append({"name": node, "layer":layer[0], "indx": i, "total": total}) # node, layer, layer内のnodeのindex

    max_index_size = max(relative_position, key=lambda x: x["indx"]).get("indx")
    # max_layer_size = max(relative_position, key=lambda x: x["layer"]).get("layer")
    return relative_position, max_index_size


def node_positions(relative_postions, max_index) -> List[dict]:
    """_summary_
    pathwayの内連結したノード（anchorの連結は含まない）の中心点の座標を算出し返す
    Args:
        relative_postions (_type_): layer_index()で算出した各ノードのlayerとlayer内のindex情報
    Returns:
        List[dict]: List[{"name": n["name"], "x": posx, "y": posy,  "layer":n["layer"],"indx": n["indx"]}]
    """
    stage_width = min_stage_width + max_index * 150
    #stage_height = min_stage_height + max_layer * 150
    positions = []
    for n in relative_postions:
        posx = (n["indx"] + 1) * stage_width / (n["total"] + 1) + stage_margin
        # y軸はlayerごとにinteraction_lengthが追加される
        posy = interaction_length * n["layer"] + stage_margin
        positions.append({"ID": n["name"], "x": posx, "y": posy,  "layer":n["layer"],"indx": n["indx"]})
    return positions


def anchored_node_positions(pathway:dict, positions) -> List[dict]:
    """
    Todo:
    anchorに接続するノードのx,y座標を算出し返す.
    1. anchorの置かれるinteractionを取得
    2. interactionからanchorに接続するノードを取得
    3. interactionの両端のノードの座標を取得し、anchorに接続するノードの座標を算出する（ex.正三角形の位置。もしくはanchorのpositionを反映した位置）
    ここまでの処理するとnode_position.pyのgraphvis_layout()と同等の情報がえられる   
    Args:
        pathway(dict): テキストファイルから読み込んだpathway情報
    Returns:
        positions (dict): {node_id (str): Tuple[x(flot), y(float)]) }
    """
    # anchorの置かれるinteractionを取得（interactionのend_pointがpathway["anchors"]のIDと一致するものを抽出）
    anchor_ids = [x["interaction"] for x in pathway["anchors"]]
    #interaction_ids = [x["ID"] for x in pathway["interactions"]]
    interaction_has_anchor = [x for x in pathway["interactions"] if x["ID"] in anchor_ids]
    # interactionのstart_point, end_pointの座標を取得
    anchor_nodes = {}
    for i in interaction_has_anchor:
        # 上記のinteractionの持つanchorを取得
        anchors = [x for x in pathway["anchors"] if x["interaction"] == i["ID"]]
        # anchorをend_pointに持つinteractionとそのstart_point（anchorに接続するノード）を取得
        for a in anchors:
            # anchorの置かれたinteractionを取得
            interaction = next(filter(lambda item:  item["ID"] == a["interaction"], interaction_has_anchor), None)
            # interactionの両端の座標をpositionsから取得
            start = next(filter(lambda item: item["ID"] == interaction["start_point"], positions), None)
            end = next(filter(lambda item: item["ID"] == interaction["end_point"], positions), None)
            # anchorに接続するノードのIDを取得
            anchor_node_interaction = next(filter(lambda item: item["end_point"] == a["ID"], pathway["interactions"]), None)
            node = anchor_node_interaction["start_point"]
            # interactionの両端のノードの座標とanchorのposition(相対値)からanchorに接続するノードの座標を算出する
            anchor_nodes_pos = calculate_trianble_vertices(start["x"], start["y"], end["x"], end["y"], float(a["position"]))
            anchor_nodes.update({node: anchor_nodes_pos})
    return anchor_nodes


def calculate_trianble_vertices(xA, yA, xB, yB, r, angle_C= math.radians(45)):
    """
    anchorの相対位置とinteractionのstart,end両端の座標からanchorの接続するノードの座標を算出する
    Calculate the coordinates of point C, which is the midpoint of AB and AM:BM = r:1.
    Args:
        xA (float): interactionの始点のx座標
        yA (float): interactionの始点のy座標
        xB (float): interactionの終点のx座標
        yB (float): interactionの終点のy座標
        r (float): interactionの始点からanchorまでの相対位置（0～1）

    Returns:
        Tuple[float]: ノードの座標 (Cx, Cy)
    """
    # Calculate ABベクトル
    AB_x = xB - xA
    AB_y = yB - yA
    # Calculate AMベクトル
    AM_x = r * AB_x
    AM_y = r * AB_y

    # Calculate CMベクトル, 11/10 CMの長さを調整
    CM_x = -AB_y * 0.75
    CM_y = AB_x * 0.75

    # Calculate 点Mの座標
    M_x = xA + AM_x
    M_y = yA + AM_y
    # Calculate 点Cの座標
    C_x = M_x + CM_x
    C_y = M_y + CM_y
    # Return 頂点A, B, Cの座標
    return C_x, C_y


def main(f:str):
    """
    bfsを利用したレイアウトでの連結したノードおよびanchorに接続するノードの座標を算出する
    Returns:
        pos (dict): {node_id (str): Tuple[x(flot), y(float)]) }
    """
    # pathwayの情報を{"pathway","nodes","interactions","anchors"}のdictで取得
    pathway = rpf.main(f)
    # 連結するノードのみで構成されるグラフを作成
    G = nx.Graph()
    G.add_nodes_from([n["ID"] for n in pathway["nodes"]])
    G.add_edges_from([(e["start_point"], e["end_point"]) for e in pathway["interactions"]])
    # ノードの座標をbfsの情報から算出
    nodes = [n["ID"] for n in pathway["nodes"]]
    pos = node_positions(*layer_index(G, nodes, nodes[0]))
    # anchorと連結するノードの座標anchorの配置されたinteractionを利用して算出
    apos = anchored_node_positions(pathway, pos)
    lpos = {p["ID"]: (p["x"],p["y"]) for p in pos}
    # Todo: Listではなくdictにする
    return {**lpos, **apos}


if __name__ == "__main__":
    print(main("../sample/simple_pathway.txt"))