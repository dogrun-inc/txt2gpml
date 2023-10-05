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


def anchor_positions(d:dict, relative_postions) -> List[dict]:
    """
    Todo: アンカーの座標を求める。引数は要検討
    Args:
        d (dict): _description_
        relative_postions (_type_): _description_

    Returns:
        List[dict]: _description_
    """
    pass


def anchored_node_positions(d:dict, relative_postions) -> List[dict]:
    """
    Todo:
    ここまでの処理するとnode_position.pyのgraphvis_layout()と同等の情報がえられる
    """
    pass


def main():
    # pathwayの情報を{"pathway","nodes","interactions","anchors"}のdictで取得
    pathway = rpf.main("data/hsa04010.txt")
    G = nx.Graph()
    G.add_nodes_from([n["name"] for n in pathway["nodes"]])
    G.add_edges_from([(e["source"], e["target"]) for e in pathway["interactions"]])
