import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import read_pathway_from_text as rft
from matplotlib import pyplot as plt

def create_psudo_network(d:dict) -> dict:
    """_summary_
    Convert anchor of pathway to psudo-nodes and psudo-edges
    Args:
        d (dict): Pathway data
    Returns:
        dict: network data (node list, edgelist) with psudo-nodes and psudo-edges
    """
    # Todo: anchorにedgeが接続するケースを考慮する（CBDの例ではnode ID 13のケース）
    # Todo: anchorを擬似的なnodeとして追加する方向で考える
    # i) 一つのanchorに対して一つのnodeを追加する
    # ii) i)で追加したノードとanchorのノードを連結した仮想的なedgeを追加する
    # iii) anchorとinteractionのstart,
    ps_nodes = []
    ps_edges = []
    for a in d["anchors"]:
        ps_node_id = "a" + a["interaction"]
        ps_nodes.append({"ID": ps_node_id})
        interaction = next((item for item in d["edges"] if item['ID'] == a["interaction"]), None)
        if interaction is None:
            # Todo: nodeがedgeでは無くanchorにinteractionする場合、
            # 再起的にedgeの両端のノードをたたどって、そのノードとの仮想的なedgeを追加する
            interaction_to_anchor = next((item for item in d["anchors"] if item['interaction'] == a["interaction"]), None)
            if interaction_to_anchor is None:
                pass
            else:
                ps_edges.append({"node1": interaction_to_anchor["node"], "node2": ps_node_id})
                ps_edges.append({"node1": ps_node_id, "node2": a["node"]})
        else:
            ps_edges.append({"node1": interaction["node1"],"node2":ps_node_id})
            ps_edges.append({"node1": ps_node_id, "node2": interaction["node2"]})
            ps_edges.append({"node1": ps_node_id, "node2": a["node"]})

    d["nodes"].extend(ps_nodes)
    d["edges"].extend(ps_edges)
    return d
    
    # 以下一回そうのanchorに対してしか対応できないため、一旦保留
    # anchorsのinteractionをキーにedgesからnode1,node2の二つのノードを取得し
    # anchor１レコードから二つの擬似的なedgeを作成する
    ps_edges = []
    for a in d["anchors"]:
        edge_id = a["interaction"]
        # fetch elements with matching edge_id
        interaction = next((item for item in d["edges"] if item['ID'] == edge_id), None)
        # Todo:anchorsのノード要素にinteractionのノード要素を連結する二つのedgeを作成を追加する
        ps_edges.extend([{"node1": interaction["node1"],
                          "node2": a["node"]},{"node1":a["node"], "node2": interaction["node2"]}])

    # 既存のedgesにps_edgesを追加する（仮のedgeであり、IDはつけない）
    d["edges"].extend(ps_edges)
    return d


def create_graph(d:dict) -> dict:
    """_summary_
    create graph from pathway data
    """
    G = nx.Graph()
    node_list = [n["ID"] for n in d["nodes"]]
    G.add_nodes_from(node_list)
    edge_list = [(e["node1"], e["node2"]) for e in d["edges"]]
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
        dict: x,y positions of nodes ex. {'001': array([-0.32849682,  0.86052563]),,}
    """
    # convert anchors to psudo-edges
    psudo_graph = create_psudo_network(d)
    # create network
    G = create_graph(psudo_graph)
    # get x,y positions of nodes
    # 階層的レイアウト(dot)がPatywayのイメージに最もマッチするとおもわれる。その他circo,fdpなども良いかもしれない
    pos = graphviz_layout(G, prog='dot')
    # 基本だがPathwayを表している感じがあまりしない
    # pos = nx.spring_layout(G, k=1, seed=10)
    nx.draw(G, pos, with_labels=True)
    plt.show()
    return pos

if __name__ == '__main__':
    main(rft.main("docs/input_sample_CBD.txt"))
