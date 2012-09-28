import pprint
import xml.dom.minidom
from xml.dom.minidom import Node
import sys
from optparse import OptionParser
import json
import random

usage="Run as python gexf2json.py input.gexf output.json [pretty]"

"""parser = OptionParser()
parser.add_option("-i", "--input", dest="input",
                  help="gexf file to read as input", metavar="INPUT")
parser.add_option("-o", "--output", dest="output",
                  help="json file to write to as output", metavar="OUTPUT")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()
"""

if (len(sys.argv)<3):
	print usage
	exit()


HEX = '0123456789abcdef'
def rgb2hex(r,g,b):
    return format((r<<16)|(g<<8)|b, '06x')


gexf = xml.dom.minidom.parse(sys.argv[1])

#Parse Attributes
nodesAttributes = []#The list of attributes of the nodes of the graph that we build in json
edgesAttributes = []#The list of attributes of the edges of the graph that we build in json
#In the gexf (that is an xml), the list of xml nodes 'attributes' (note the plural 's')
attributesNodes = gexf.getElementsByTagName("attributes")
for attr in attributesNodes:
	if (attr.getAttribute("class") == "node"):
		attributeNodes = attr.getElementsByTagName("attribute")#The list of xml nodes 'attribute' (no 's')
		for attributeNodes in attributeNodes:
			id = attributeNodes.getAttribute('id')
			title = attributeNodes.getAttribute('title')
			type = attributeNodes.getAttribute('type')
			attribute = {"id":id, "title":title, "type":type}
        	nodesAttributes.append(attribute);
	elif (attr.getAttribute("class")=="edge"):
		attributeNodes = attr.getElementsByTagName('attribute')#The list of xml nodes 'attribute' (no 's')
		for attributeNode in attributeNodes:
			#Each xml node 'attribute'
			id = attributeNode.getAttribute('id')
		  	title = attributeNode.getAttribute('title')
		  	type = attributeNode.getAttribute('type')
		  	
		  	attribute = {"id":id, "title":title, "type":type}
		  	edgesAttributes.append(attribute)
	 
jsonNodes = []#The nodes of the graph
nodesNodes = gexf.getElementsByTagName("nodes")#The list of xml nodes 'nodes' (plural)

for nodes in nodesNodes:
	listNodes = nodes.getElementsByTagName("node")#The list of xml nodes 'node' (no 's')
	for nodeEl in listNodes:
		#Each xml node 'node' (no 's')
		id = nodeEl.getAttribute('id')
		title = nodeEl.getAttribute('title')
		label = nodeEl.getAttribute('label') if nodeEl.hasAttribute("label") else id
	  
		#viz
		size = 1
		x = 100 - 200*random.random()
		y = 100 - 200*random.random()
		color=""

		#SAH: Original JS code tested for size.length in ternary; is len(...)!=0 appropriate replacement?
		sizeNodes = nodeEl.getElementsByTagName('size')
		sizeNodes = sizeNodes if len(sizeNodes)!=0 else nodeEl.getElementsByTagNameNS('*','size')
		if(len(sizeNodes)>0):
			sizeNode = sizeNodes[0];
			size = float(sizeNode.getAttribute('value'))
		
		#SAH save as sizeNodes
		positionNodes = nodeEl.getElementsByTagName('position')
		positionNodes = positionNodes if len(positionNodes)!=0 else nodeEl.getElementsByTagNameNS('*','position')
		if(len(positionNodes)>0):
			positionNode = positionNodes[0]
			x = float(positionNode.getAttribute('x'))
			y = float(positionNode.getAttribute('y'))
		
		
		#SAH: really couldn't this be a function by now; same as above
		colorNodes = nodeEl.getElementsByTagName('color')
		colorNodes = colorNodes if len(colorNodes)!=0 else nodeEl.getElementsByTagNameNS('*','color')
		if(len(colorNodes)>0):
			colorNode = colorNodes[0]
			color = '#'+rgb2hex(int(colorNode.getAttribute('r')),
						int(colorNode.getAttribute('g')),
						int(colorNode.getAttribute('b')))
		
		#Create Node
		node = {"id":id,"label":label, "size":size, "x":x, "y":y, "attributes":[], "color":color};  #The graph node
	  
		#Attribute values
		attvalueNodes = nodeEl.getElementsByTagName("attvalue")
		for attvalueNode in attvalueNodes:
			attr = attvalueNode.getAttribute('for');
			val = attvalueNode.getAttribute('value');
			node["attributes"].append({"attr":attr, "val":val})

		jsonNodes.append(node)

jsonEdges = []
edgeId = 0
edgesNodes = gexf.getElementsByTagName('edges')
for edgesNode in edgesNodes:
	edgeNodes = edgesNode.getElementsByTagName('edge')
	for edgeNode in edgeNodes:
		source = edgeNode.getAttribute("source")
		target = edgeNode.getAttribute("target")
		label = edgeNode.getAttribute("label")
		id = edgeNode.getAttribute("id") if edgeNode.hasAttribute("id") else edgeId
		edgeId=edgeId+1
		
		edge = {
		    "id":         id,
		    "sourceID":   source,
		    "targetID":   target,
		    "label":      label,
		    "attributes": []
		}

		if(edgeNode.hasAttribute("weight")):
			edge["weight"] = edgeNode.getAttribute('weight')

		attvalueNodes = edgeNode.getElementsByTagName('attvalue')
		for attvalueNode in attvalueNodes:
			attr = attvalueNode.getAttribute('for')
			val = attvalueNode.getAttribute('value')
			edge["attributes"].append({"attr":attr, "val":val})

		jsonEdges.append(edge)

fhOutput = open(sys.argv[2],"w")
j={"nodes":jsonNodes,"edges":jsonEdges}
if len(sys.argv)>=4 and "pretty"==lower(sys.argv[3]):
	json.dump(j,fhOutput,indent=4)
else:
	json.dump(j,fhOutput)