import networkx as nx
from typing import Tuple, List

import read_pathway_from_text as rpf


# レイアウトの初期値設定
stage_width = 500
stage_height = 500
stage_margin = 30
interaction_length = 50

def layer_index(g, nodes, root_node) -> dict:
    """
    ノード同士のインタラクションがある各ノードの相対的な位置情報
    （layerの番号、layer中のインデックス）をBFSで算出し返す
    
    Returns:
        dict:{name(str), layer(int), indx(int)}
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
    return relative_position


def node_positions(relative_postions) -> List[dict]:
    """_summary_
    pathwayの内連結したノード（anchorの連結は含まない）の中心点の座標を算出し返す
    Args:
        relative_postions (_type_): _description_

    Returns:
        List[dict]: List[{"name": n["name"], "x": posx, "y": posy,  "layer":n["layer"],"indx": n["indx"]}]
    """
    positions = []
    for n in relative_postions:
        posx = (n["indx"] + 1) * stage_width / (n["total"] + 1) + stage_margin
        # y軸はlayerごとにinteraction_lengthが追加される
        posy = interaction_length * n["layer"] + stage_margin
        positions.append({"name": n["name"], "x": posx, "y": posy,  "layer":n["layer"],"indx": n["indx"]})
    return positions


def anchored_node_positions(d:dict, relative_postions) -> List[dict]:
    """
    Todo:
    anchorに接続するノードのx,y座標を算出し返す.
    1. anchorの置かれるinteractionを取得
    2. interactionからanchorに接続するノードを取得
    3. interactionの両端のノードの座標を取得し、anchorに接続するノードの座標を算出する（ex.正三角形の位置。もしくはanchorのpositionを反映した位置）
    ここまでの処理するとnode_position.pyのgraphvis_layout()と同等の情報がえられる
    """
    pass



def calculate_trianble_vertices(xA, yA, xB, yB, r):
    """
    anchorの相対位置とinteractionのstart,end両端の座標からanchorの接続するノードの座標を算出する
    Calculate the coordinates of point C, which is the midpoint of AB and AM:BM = r:1.
    Args:
        xA (_type_): _description_
        yA (_type_): _description_
        xB (_type_): _description_
        yB (_type_): _description_
        r (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Calculate ABベクトル
    AB_x = xB - xA
    AB_y = yB - yA
    # Calculate AMベクトル
    AM_x = r * AB_x
    AM_y = r * AB_y
    # Calculate CMベクトル
    CM_x = -AB_y
    CM_y = AB_x
    # Calculate 点Mの座標
    M_x = xA + AM_x
    M_y = yA + AM_y
    # Calculate 点Cの座標
    C_x = M_x + CM_x
    C_y = M_y + CM_y

    # Return 頂点A, B, Cの座標
    return (xA, yA), (xB, yB), (C_x, C_y)



def main():
    # pathwayの情報を{"pathway","nodes","interactions","anchors"}のdictで取得
    pathway = rpf.main("data/hsa04010.txt")
    G = nx.Graph()
    G.add_nodes_from([n["name"] for n in pathway["nodes"]])
    G.add_edges_from([(e["source"], e["target"]) for e in pathway["interactions"]])
    # 仮想エッジ、仮想ノードを追加

    # pathway_attribute.main()に渡すdictを作成


if __name__ == "__main__":
    # anchorの相対日
    # Given coordinates and ratio
    xA = 0
    yA = 0
    xB = 4
    yB = 0
    ratio_AM_to_BM = 0.5  # Example ratio
    # Calculate point C coordinates
    A, B, C = calculate_trianble_vertices(xA, yA, xB, yB, ratio_AM_to_BM)

    # Print the coordinates of point C
    print("頂点A:", A)
    print("頂点B:", B)
    print("頂点C:", C)