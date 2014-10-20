import networkx as nx
import community

colors = [
	'1f77b4',
	'ff7f0e',
	'2ca02c',
	'd62728',
	'9467bd',
	'8c564b',
	'e377c2',
	'7f7f7f',
	'bcbd22',
	'17becf']

def hex_to_rgb():
	cList = []
	for hex_digits in colors:
		rgbDict = {}
		rgb = tuple([int(s, 16) for s in (hex_digits[0:2], hex_digits[2:4], hex_digits[4:6])])
		rgbDict['r'] = rgb[0]
		rgbDict['g'] = rgb[1]
		rgbDict['b'] = rgb[2]
		cList.append(rgbDict)
	return cList

rgbs = [
 {'b': 180, 'g': 119, 'r': 31},
 {'b': 14, 'g': 127, 'r': 255},
 {'b': 44, 'g': 160, 'r': 44},
 {'b': 40, 'g': 39, 'r': 214},
 {'b': 189, 'g': 103, 'r': 148},
 {'b': 75, 'g': 86, 'r': 140},
 {'b': 194, 'g': 119, 'r': 227},
 {'b': 127, 'g': 127, 'r': 127},
 {'b': 34, 'g': 189, 'r': 188},
 {'b': 207, 'g': 190, 'r': 23}]

if __name__ == '__main__':
	#Load .gml
	print('Loading data...')
	G = nx.read_gml('facebook.gml', relabel=True)

	#Run community detection algorithm
	print('Detecting communities...')
	myCNM = community.CNM(G)
	comms = myCNM[1]

	#Calculate node positions
	print('Laying out nodes...')
	pos = nx.spring_layout(G, scale = 1000)

	print('Saving attributes...')
	#Add the visual attrs to each node
	for i in range(len(comms)):
		for n in comms[i]:
			G.node[n]['viz']={'color': rgbs[i], 'position':{'x':pos[n][0], 'y':pos[n][1]}}

	#Export to 'facebook.gexf'
	nx.write_gexf(G, './network/data/facebook.gexf')