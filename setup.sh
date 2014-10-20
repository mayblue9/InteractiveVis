#!/bin/bash
cd networkx
python setup.py install
cd ..

cd pyparsing
python setup.py install
cd ..

cd numpy
python setup.py install
cd ..

python -i make_gml_graph.py *.gdf
