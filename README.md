# txt2gpml
Tools to generate readable XML (GPML) for [WikiPathways (https://www.wikipathways.org/)](https://www.wikipathways.org/) from nodes and interactions data described in text format.

## 環境


## Input data format

- comma-separated data of pathway, nodes, edges, and anchors for each block.
- If each block is preceded by a comment describing the type, for example, a line beginning with "# nodes", it is treated as a block describing a node up to the following empty line.
- The first line of each block describes the header. The headers are converted to dictionary keys after the file is read.
- ノード、インタラクション, アンカーにはIDをつける。各IDはa-fのアルファベットを頭文字にした5桁もしくは8桁の文字列。

```
# pathway
name,organism, 

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

### nodes
- Label
- BiologicalType
- ID

### interactions
- start_point
- end_point
- BiologicalType
- ID

The interactions describes the start node and target node, each with a node ID.
interactions block. The interactions also describe the relationship between anchors and nodes.

### anchors
- interaction
- positin
- ID

Anchors describes the interaction in which the anchor is placed, its relative position in the interaction, and the ID of the anchor.

## Way to use

```
$ python txt2gpm.py -i input_file -o output_file_name.gpml
```

## 実装予定
- Layout optimization
- Option to allow select ayout program option (dot,crco etc)
- GroupRef attribute
- Color attribute
- LineStyle attirbute
- DB binding
- Group 






