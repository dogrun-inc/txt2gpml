import networkx as nx


def create_psudo_edges(d:dict) -> dict:
    """_summary_
    Convert anchor of pathway to psudo-edges
    Args:
        d (dict): Pathway data
    Returns:
        dict: アンカーをインタラクション両端のノードに連結した擬似的グラフ
    """



def create_graph(d:dict) -> dict:
    """_summary_
    create graph from pathway data
    """
    G = nx.Graph()
    node_list = [n["id"] for n in d["nodes"]]
    G.add_nodes_from(node_list)
    edge_list = [(e["node1"], e["node2"]) for e in d["edges"]]
    G.add_edges_from(edge_list)


def main(d:dict) -> dict:
    """_summary_
    - The converted pathway data from the file is passed to networkx to obtain the coordinates of each node.
    - Since anchors cannot be converted to networks as they are, the nodes at both ends of the interaction are 
    connected to the nodes connected to the anchor and treated as a pseudo-network.
    Args:
        d: {nodes:[], edges:[], anchors:[]}
    Returns: 
        dict: x,y positions of nodes
    """
    # convert anchors to psudo-edges

    # create network

    # get x,y positions of nodes

    return d



