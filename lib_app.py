
# ver 0.3
#
# changelog
#
# 0.1 start init
# 0.2 graph ok
# 0.3 move to obj, add draw options, add argparse, add demo, add read .list, add read .json
#

import collections, json
from random import randint

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import networkx as nx
import matplotlib.pyplot as plt

tree = lambda: collections.defaultdict(tree)

class NetDiscovery(object):

	jsonTree = tree()
	input_list = []

	demo_code = [ 'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 
	'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 
	'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 
	'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 
	'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'VW', 'WY' ]

	def __init__(self, input_list = None, jsonFile = None):

		if input_list:
			logging.info( 'reading input list %s' % (input_list) )
			self.input_list = input_list

		if jsonFile:
			logging.info( 'reading json file %s' % (jsonFile) )
			with open(jsonFile) as data_file:    
				self.jsonTree = json.load(data_file)

	def showJson(self):
		return json.dumps( self.jsonTree, sort_keys=True, indent=4, separators=(',', ': ') )

	def demoRandom(self, list_to_random, purge = False):

		choose = list_to_random[randint(1,len(list_to_random) - 1)]
		if purge:
			list_to_random.remove( choose )

		return choose

	def igp(self, igp = 'ospf', node = None, demo = True ):

		if demo:

			self.jsonTree.update( {
			 	node : {
			 		'hostname' : self.demoRandom( self.demo_code , purge= True ), 
			 		'os' : 'ios',
			 		'path' : {
			 			'e0.12': {
			 				'rid' : self.demoRandom( self.input_list ), 
			 				'area' : '0',
			 				'cost' : randint(1, 100),
			 				'netype' : 'p2p',
			 				'state' : 'Up'
			 			}
			 		}
			 	}
			} )

	def draw(self, filename = 'path.png', host_labl = 'rid', edge_labl = 'cost'):

		G = nx.Graph()
		labels = {}
		labels_edge = {}

		for local_remote_rid in sorted(self.jsonTree):
			logging.info( '%s ( %s )' % ( self.jsonTree[local_remote_rid]['hostname'], local_remote_rid ) )
			G.add_node(local_remote_rid)
			for intf in self.jsonTree[local_remote_rid]['path']:
				logging.info( '%s - %s' % ( intf, self.jsonTree[local_remote_rid]['path'][intf]) )

				if host_labl == 'hostname':
					labels[local_remote_rid] = self.jsonTree[local_remote_rid]['hostname']
				elif host_labl == 'rid':
					labels[local_remote_rid] = local_remote_rid
				
				remote_remote_rid = self.jsonTree[local_remote_rid]['path'][intf]['rid']

				if edge_labl == 'cost':
					choose_what_show = self.jsonTree[local_remote_rid]['path'][intf]['cost']
				elif edge_labl == 'area':
					choose_what_show = self.jsonTree[local_remote_rid]['path'][intf]['area']
				elif edge_labl == 'netype':
					choose_what_show = self.jsonTree[local_remote_rid]['path'][intf]['netype']
				elif edge_labl == 'int':
					choose_what_show = intf

				labels_edge[(local_remote_rid, remote_remote_rid)] = choose_what_show
				G.add_edge(local_remote_rid, remote_remote_rid)

		pos = nx.spring_layout(G)

		nx.draw(G, pos)
		nx.draw_networkx(G, pos, labels=labels, font_size=10)

		nx.draw_networkx_edge_labels(G, pos, with_labels=True, edge_labels=labels_edge, label_pos=0.75, font_size=10)

		plt.savefig(filename)
		logging.info( 'printing draw to %s' % (filename) )