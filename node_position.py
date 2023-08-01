import networkx as nx

def main():
    """_summary_
    - The converted pathway data from the file is passed to networkx to obtain the coordinates of each node.
    - Since anchors cannot be converted to networks as they are, the nodes at both ends of the interaction are 
    connected to the nodes connected to the anchor and treated as a pseudo-network.
    """


