# txt2gpml
Tools to generate readable XML (GPML) for [WikiPathways (https://www.wikipathways.org/)](https://www.wikipathways.org/) from nodes and interactions data described in text format.

## Environment

- Python version must be 3.9 or higher
   - `networkx`, `matplotlib` should be installed using `pip`
- `graphviz` required for `pygraphviz`.

## Input data format

- comma-separated data of pathway, nodes, edges, and anchors for each block.
- If each block is preceded by a comment describing the type, for example, a line beginning with "# nodes", it is treated as a block describing a node up to the following empty line.
- The first line of each block describes the header. The headers are converted to dictionary keys after the file is read.
- IDs must be added for nodes, interactions and anchors. Each ID is a 5- or 8-digit string with the letters a-f as its initials.

```
# pathway
name,organism

# nodes
Label, BiologicalType,ID

# interactions
start_point,end_point,BiologicalType

# anchors
interaction,position,ID
```

### pathway
- name
- organism
- layout (optional)

In txt2gpml, Breadth-first search (BFS) layout is applied by default, so there is no need to specify the algorithm.
 If you want to use networkx layouts, you can specify circo, dot, etc. as the value of layout attribute.

### nodes
- Label
- BiologicalType
- Color (optional)
- ID

Nodes are drawn black by default, but you can also specify the Color attribute as a hexadecimal color code, such as 0000ff

### interactions
- start_point
- end_point
- BiologicalType
- LineStyle (optional)
- ID

Interactions describe the start node and target node, each with a node ID.
Interactions also describe the relationship between anchors and nodes.
Currently, when an interaction combines an anchor and a node, be sure to specify the anchor at the "end_point".

The line style of the interaction is solid by default, but the LindStyle attribute can be set separately, for example, "Broken".

### anchors
- interaction
- position
- ID

Anchors describe the interaction in which the anchor is placed, its relative position in the interaction, and the ID of the anchor.

## Way to use

```
$ python txt2gpm.py -i input_file -o output_file_name.gpml
```

## To be implemented...

- Layout optimization
- Group objects
- DB binding






