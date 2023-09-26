# encoding: utf-8
import os
import sys
import csv
import node_position

def read_text(f:str):
    with open(f, 'r') as f:
        lines = f.readlines()
    return lines
    

def get_blcoks(rows:list):
    """_summray_
    Finding the position of a block in a list from converted nodes, edges, and anchors
    1. find the position (index) of nodes, edges, anchors
    2. find the position of the nearest blank line
    3. find the position of the block from the position of 1 and 2
    return: parts of list
    """
    # Todo: root データの取得を追加する
    start_pathway = [i for i, r in enumerate(rows) if r.startswith("# pathway")]
    # 1. find the position (index) of nodes, edges, anchors
    start_nodes = [i for i, r in enumerate(rows) if r.startswith("# nodes")]
    start_edges = [i for i, r in enumerate(rows) if r.startswith("# interaction")]
    start_anchors = [i for i, r in enumerate(rows) if r.startswith("# anchors")]
    blank_rows = [i for i, r in enumerate(rows) if r == ""]
    # 2. find the position of the nearest blank line

    position_end_pathway = min(blank_rows, key=lambda x:x-start_pathway[0]if x > start_pathway[0] else float('inf'))
    position_end_nodes = min(blank_rows, key=lambda x:x-start_nodes[0]if x > start_nodes[0] else float('inf'))
    position_end_edges = min(blank_rows, key=lambda x:x-start_edges[0]if x > start_edges[0] else float('inf'))    
    position_end_anchors = min(blank_rows, key=lambda x:x-start_anchors[0]if x > start_anchors[0] else float('inf'))
    # 3. find the position of the block from the position of 1 and 2
    pathway = rows[start_pathway[0]+1:position_end_pathway]
    nodes = rows[start_nodes[0]+1:position_end_nodes]
    edges = rows[start_edges[0]+1:position_end_edges]
    anchors = rows[start_anchors[0]+1:position_end_anchors]
    return pathway, nodes, edges, anchors


def list2dict(lst:list):
    """_summary_
    split strings
    """
    lst_splt = [x.split(',') for x in lst]
    return [dict(zip(lst_splt[0], v)) for v in lst_splt[1:]]


def main(f:str):
    """_summary_
    0. The source is a tab-delimited file in which nodes, edges, 
    and anchors are described block by block, and the comment line 
    on the first line of each block begins with nodes, edges, and anchors.
    1. Read tab-delimited file describing nodes, edges, and anchors.
    2. Parses rows for each block and converts to a list or dict.
    3. Returns a list of dicts for each block.
    4. convert to node list, edge list, anchor list to each dict.

    Args:
        string: data file path
    Returns:
        dict: pathway data
    """
    rows = [r.rstrip() for r in read_text(f)]
    # append blank line to the end of the list
    rows.append("")
    # Todo: root属性の取得スクリプトをget_blocksに追加する


    #root_props, node_list, edge_list, anchor_list = get_blcoks(rows)
    pathway_attr, node_list, edge_list, anchor_list = get_blcoks(rows)
    pathway = list2dict(pathway_attr)[0]
    nodes = list2dict(node_list)
    edges = list2dict(edge_list)
    anchors = list2dict(anchor_list)
    # Todo: 座標要素（node, anchor）を追加する
    # Todo: interactionの座標はnodeの座標と微妙に異なるので、それを踏まえinteractionのpositionを計算する
    # Interactionのstart-endの座標セットとして計算する
    pathway_dict = {"pathway": pathway, "nodes":nodes, "interactions":edges, "anchors":anchors}
    return pathway_dict


if __name__ == '__main__':
    main("sample/simple_metabolite_text.txt")
