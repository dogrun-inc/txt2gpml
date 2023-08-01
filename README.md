# txt2gpml
A tools to generate readable XML (GPML) for [WikiPathways (https://www.wikipathways.org/)](https://www.wikipathways.org/) from node and interaction data described in text files.

## Input file format

- Tab-delimited description of nodes, edges, and anchors for each block.
- If each block is preceded by a comment describing the type, for example, a line beginning with "# node", it is treated as a block describing a node up to the following empty line.
- The first line of each block describes the header. The headers are converted to dictionary keys after the file is read.
- NODE records always specify an ID.
- The edge describes the start node and target node, each with a node ID.
- The anchor describes the node and interaction, and is described as edge ID and node ID, respectively.

## Reading files and converting to dict

- Read files in the read_pathway_from_text module and convert them to dict format.

