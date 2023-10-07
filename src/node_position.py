import re
import networkx as nx
from typing import Tuple
from networkx.drawing.nx_agraph import graphviz_layout
from matplotlib import pyplot as plt
import read_pathway_from_text as rpft


def create_psudo_network(d:dict) -> dict:
    """_summary_
    Convert anchor of pathway to psudo-nodes and psudo-edges
    Args:
        d (dict): Pathway data
    Returns:
        dict: network data (node list, edgelist) with psudo-nodes and psudo-edges
    """
    # 2023/9/27 データ構造変更に伴い仮想グラフ(=psudo_graph)の作成方法を変更
    # i. anchor仮想ノードとしてps_nodesに追加する  ok
    # ii. 仮想エッジを生成する。anchorと両端の（interaction両端）のノードを結ぶ
    # iii. ファイルより読み込んだnodesとinteractionsにps_nodeをps_edgeを追加する

    ps_nodes = []
    ps_edges = []
    for a in d["anchors"]:
        # anchorを仮想ノードとしてps_nodesに追加
        ps_node_id = a["ID"]
        ps_nodes.append({"ID": ps_node_id})

        # 仮想エッジを追加
        # a. anchorを抽出し、anchorが乗るinteractionを取得
        ps_interaction = next((item for item in d["interactions"] if item['ID'] == a["interaction"]), None)
        # b. anchorが乗るinteractionのstart_point, end_pointのノードを取得
        ps_start_point = ps_interaction["start_point"] 
        ps_end_point = ps_interaction["end_point"]
        # c. anchorとinteractionのstart_point, end_pointのノードとanchorを結ぶ仮想エッジを生成し、ps_edges:listに追加する
        # interactionの両端ノードとanchorを結ぶ二つの仮想エッジを生成する
        ps_edges.extend([{"start_point": ps_start_point, "end_point": ps_node_id, "ID": ps_node_id},
                          {"start_point": ps_node_id, "end_point": ps_end_point, "ID": ps_node_id}])

    d["nodes"].extend(ps_nodes)
    d["interactions"].extend(ps_edges)
    return d


def create_graph(d:dict) -> dict:
    """_summary_
    create graph from pathway data
    """
    G = nx.Graph()
    node_list = [n["ID"] for n in d["nodes"]]
    G.add_nodes_from(node_list)
    ###
    # Todo: interactionsの要素がリストとしてeが取得されるケースがある
    ###
    edge_list = [(e["start_point"], e["end_point"]) for e in d["interactions"]]
    G.add_edges_from(edge_list)

    return G


def main(d:dict) -> dict:
    """_summary_
    - The converted pathway data from the file is passed to networkx to obtain the coordinates of each node.
    - Since anchors cannot be converted to networks as they are, the nodes at both ends of the interaction are 
    connected to the nodes connected to the anchor and treated as a pseudo-network.
    - If you want to visualize a hypothetical graph, you need to install matplotlib, but it is not essential 
    to install matplotlib because visualization is not required for the original functionality.
    Args:
        d: {nodes:[], edges:[], anchors:[]}
    Returns: 
        positions (dict): {node_id (str): Tuple[x(flot), y(float)]) }
        ex. {'n001': (103.6, 162.0), 'n002': (178.6, 162.0), 'n003': (28.597, 162.0),'noo2': (73.597, 18.0)}
    """
    prg_option = d["pathway"].get("layout")
    if prg_option is None:
        prg = 'circo'
    else:
        prg = re.sub(r'[\W_]+', '', prg_option)

    # convert anchors to psudo-edges
    psudo_graph = create_psudo_network(d)
    # create network
    G = create_graph(psudo_graph)
    # get x,y positions of nodes
    # 階層的レイアウト(dot)がPatywayのイメージに最もマッチするとおもわれる。その他circo,fdpなども良いかもしれない
    #pos = graphviz_layout(G, prog='dot', root=0)
    pos = graphviz_layout(G, prog=prg, root=0)

    # 基本だがPathwayを表している感じがあまりしない
    #pos = nx.spring_layout(G, k=1, seed=10)
    #nx.draw(G, pos, with_labels=True)
    #nx.draw_networkx_nodes(G, pos, node_shape='s', node_size=300)
    #nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True)
    #nx.draw_networkx_labels(G, pos, font_size=10, font_color="white")
    #plt.show()
    return pos


if __name__ == '__main__':
    main(rpft.main("docs/input_sample_CBD.txt"))
