
# ver 0.1
#
# changelog
#
# 0.1 start init
#

from lib_app import Discovery

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import networkx as nx
import matplotlib.pyplot as plt

def main():

	d = Discovery()
	json = d.showJson()

	G = nx.Graph()
	labels = {}

	for node in sorted(json):
		print node,
		G.add_node(node)
		print json[node]['rid']
		for path in json[node]['path']:
			print '-', path,
			labels[(node, path)] = json[node]['path'][path]['cost']
			print json[node]['path'][path]
			G.add_edge(node, path)

	pos = nx.spring_layout(G)

	nx.draw(G, pos)
	nx.draw_networkx(G, pos, with_labels=True, font_size=10)
	nx.draw_networkx_edge_labels(G, pos, with_labels=True, edge_labels=labels, font_size=10)

	plt.savefig("path.png")

if __name__ == '__main__':
	main()