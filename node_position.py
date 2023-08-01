import networkx as nx
import read_pathway_from_text as rft
from matplotlib import pyplot as plt

def create_psudo_edges(d:dict) -> dict:
    """_summary_
    Convert anchor of pathway to psudo-edges
    Args:
        d (dict): Pathway data
    Returns:
        dict: アンカーをインタラクション両端のノードに連結した擬似的グラフ
    """
    # anchorsのinteractionをキーにedgesからnode1,node2の二つのノードを取得し
    # anchor１レコードから二つの擬似的なedgeを作成する
    ps_edges = []
    for a in d["anchors"]:
        edge_id = a["interaction"]
        # fetch dcit with matching edge_id
        interaction = next((item for item in d["edges"] if item['ID'] == edge_id), None)
        ps_edges.append({"node1": interaction["node1"], "node2": interaction["node2"]})
    # Todo: 既存のedgesにps_edgesを追加する（仮のedgeであり、IDはつけない）
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
    psudo_graph = create_psudo_edges(d)
    # create network
    G = create_graph(psudo_graph)
    # get x,y positions of nodes
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()
    return pos

if __name__ == '__main__':
    main(rft.main("docs/input_sample_CBD.txt"))
