# encoding: utf-8
import os
import sys
import csv

def read_text(f:str):
    with open(f, 'r') as f:
        lines = f.readlines()
    return lines
    

def main(f:str):
    """_summary_
    0. The source is a tab-delimited file in which nodes, edges, 
    and anchors are described block by block, and the comment line 
    on the first line of each block begins with nodes, edges, and anchors.
    1. Read tab-delimited file describing nodes, edges, and anchors.
    2. Parses rows for each block and converts to a list or dict.
    3. Returns a list of dicts for each block.
    """
    rows = [r.rstrip() for r in read_text(f)]
    # append blank line to the end of the list
    rows.append("")
    print(get_blcoks(rows))


def get_blcoks(rows:list):
    """_summray_
    Finding the position of a block in a list from converted nodes, edges, and anchors
    1. find the position (index) of nodes, edges, anchors
    2. find the position of the nearest blank line
    3. find the position of the block from the position of 1 and 2
    return: parts of list
    """
    # 1. find the position (index) of nodes, edges, anchors
    start_nodes = [i for i, r in enumerate(rows) if r.startswith("# nodes")]
    start_edges = [i for i, r in enumerate(rows) if r.startswith("# edges")]
    start_anchors = [i for i, r in enumerate(rows) if r.startswith("# anchors")]
    blank_rows = [i for i, r in enumerate(rows) if r == ""]
    # 2. find the position of the nearest blank line
    position_end_nodes = min(blank_rows, key=lambda x:x-start_nodes[0]if x > start_nodes[0] else float('inf'))
    position_end_edges = min(blank_rows, key=lambda x:x-start_edges[0]if x > start_edges[0] else float('inf'))    
    position_end_anchors = min(blank_rows, key=lambda x:x-start_anchors[0]if x > start_anchors[0] else float('inf'))
    # 3. find the position of the block from the position of 1 and 2
    nodes = rows[start_nodes[0]+1:position_end_nodes]
    edges = rows[start_edges[0]+1:position_end_edges]
    anchors = rows[start_anchors[0]+1:position_end_anchors]
    return nodes, edges, anchors


def convert2nodelist():
    pass

def convert2edgelist():
    pass

def convert2anchorlist():
    pass

if __name__ == '__main__':
    main("docs/input_sample_CBD.txt")
    