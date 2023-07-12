# input text案

## node list
label   biologicalType id
cannabigerolic acid (CBGA)  Metabolite  001
Cannabidiolic acid (CBDA)   Metabolite 002
Cannabidiolic acid synthase (CBDAS) Protein 003

## edge list (node listのidでnodesを指定する)
node1   node2   biologicaltype
001 002 mim-conversion

## anchor list　（node listのidのセットでnode-anchorを指定する）
node    interaction biologicaltype
003 [001,002]   mim-catalysis