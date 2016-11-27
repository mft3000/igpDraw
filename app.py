
# ver 0.2
#
# changelog
#
# 0.1 start init
# 0.2 graph ok
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
	labels_edge = {}

	for local_remote_rid in sorted(json):
		logging.info( '%s ( %s )' % ( json[local_remote_rid]['hostname'], local_remote_rid ) )
		G.add_node(local_remote_rid)
		for intf in json[local_remote_rid]['path']:
			logging.info( '%s - %s' % ( intf, json[local_remote_rid]['path'][intf]) )
			labels[local_remote_rid] = json[local_remote_rid]['hostname']
			remote_remote_rid = json[local_remote_rid]['path'][intf]['rid']
			labels_edge[(local_remote_rid, remote_remote_rid)] = json[local_remote_rid]['path'][intf]['cost']
			G.add_edge(local_remote_rid, remote_remote_rid)

	pos = nx.spring_layout(G)

	nx.draw(G, pos)
	nx.draw_networkx(G, pos, labels=labels, font_size=10)

	nx.draw_networkx_edge_labels(G, pos, with_labels=True, edge_labels=labels_edge, label_pos=0.9, font_size=10)

	plt.savefig("path.png")

if __name__ == '__main__':
	main()