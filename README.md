# txt2gpml
Tools to generate readable XML (GPML) for [WikiPathways (https://www.wikipathways.org/)](https://www.wikipathways.org/) from nodes and interactions data described in text format.

## 環境


## Input data format

- comma-separated data of pathway, nodes, edges, and anchors for each block.
- If each block is preceded by a comment describing the type, for example, a line beginning with "# node", it is treated as a block describing a node up to the following empty line.
- The first line of each block describes the header. The headers are converted to dictionary keys after the file is read.
- NODE records always specify an ID.
- The edge describes the start node and target node, each with a node ID.
- The anchor describes the node and interaction, and is described as edge ID and node ID, respectively.
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

### anchors
- interaction
- positin
- ID

## Way to use

```
$ python txt2gpm.py -i input_file -o output_file_name.gpml
```

## 実装予定
- Layout program option (dot,)
- GroupRef attribute
- Color attribute
- LineStyle attirbute
- DB binding
- Group 






