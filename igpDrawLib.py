#!/usr/bin/env python

# ver 0.6
#
# changelog
#
# 0.1 start init
# 0.2 graph ok
# 0.3 move to obj, add draw options, add argparse, add demo, add read .list, add read .json
# 0.4 edit variables, add show ospf commands 
# 0.5 device telnet, discovery and build json
# 0.6 randominze interface name for demo mode and reduce name in draw
#

import collections, json, re, os
from random import randint

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import networkx as nx
import matplotlib.pyplot as plt

from igp import OSPF, ISIS

tree = lambda: collections.defaultdict(tree)

def auth_cred(mode, debug = False):
	credentials = {}

	if mode == 'local':
	
		try:
			credentials = { \
				'username': str(os.environ["PYUSER"]), \
				'password': str(os.environ["PYPASS"]), \
				'enable': str(os.environ["PYEN"]), \
			}
		except:
			print("run \'source envs\' in order to load user/pass in env variables")
			
	if debug:
		print credentials
	
	return credentials

def reduce_netype(ntype):
	'''
	reduce igp network type title for problems in draw visualization
	'''
	if ntype == 'POINT_TO_POINT':
		return 'p2p'
	elif ntype == 'BROADCAST':
		return 'bcast'
	else:
		return ntype

def reduce_interface_name(interface_name):
	'''
	reduce interface name for problems in draw visualization
	'''
	if 'FastEthernet' in interface_name:
		return interface_name.replace('FastEthernet','Fa')
	elif 'TenGigabitEthernet' in interface_name:
		return interface_name.replace('TenGigabitEthernet','Te')
	elif 'GigabitEthernet' in interface_name:
		return interface_name.replace('GigabitEthernet','Gi')
	elif 'Ethernet' in interface_name:
		return interface_name.replace('Ethernet','Et')
	else:
		return interface_name

class NetDiscovery(object):

	jsonTree = tree()
	input_list = []

	igpNeighbors = tree()
	rid = ''
	pid = ''

	demo_code = [ 'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 
	'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 
	'MD', 'ME', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 
	'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 
	'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'VW', 'WY' ]

	interface_demo = [ 'Ethernet', 'FastEthernet', 'GigabitEthernet', 'TenGigabitEthernet' ]

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

	def demoRandom(self, list_to_random, avoid_duplicates = False):

		choose = list_to_random[randint(1,len(list_to_random) - 1)]
		if avoid_duplicates:
			list_to_random.remove( choose )

		return choose


	def igp(self, igp = 'ospf', node = None, demo = True, save_as_file = False , os = 'ios', community = 'pubblic' ):

		if igp == 'ospf':
			if demo:
				logging.info("generate json for node")

				self.jsonTree["201"].update( {
				 	node : {
				 		"hostname" : self.demoRandom( self.demo_code , avoid_duplicates= True ), 
				 		"os" : "ios",
				 		"path" : {
				 			self.demoRandom( self.interface_demo ) + "0/0" : {
				 				"rid" : self.demoRandom( self.input_list ), 
				 				"area" : "0",
				 				"cost" : randint(1, 100),
				 				"netype" : "POINT_TO_POINT",
				 				"state" : "Up"
				 			}
				 		}
				 	}
				} )

				print json.dumps(self.jsonTree, sort_keys=True, indent=4, separators=(',', ': '))

			else:

				o = OSPF(node)

				credentials = auth_cred('local', True)
				status = o.remote_connect(credentials)

				self.jsonTree = o.show_ospf_interface()

				o.remote_close()

		elif igp == 'isis':
			print 'Not Yet Developed... EXIT'
			exit(0)

		if save_as_file:
			self.save_topology_as_file()

	def save_topology_as_file(self, filename = "auto_save_file.json"):

			logging.info( 'save topology as %s for further draws' % (filename) )

			out_file_name_json = open( filename, "w")
			print >> out_file_name_json, json.dumps( self.jsonTree, sort_keys=True, indent=4, separators=(',', ': ') )
			out_file_name_json.close()

	# def preCheck(self, dests, community):

	# 	oids = {}
	# 	oids["sysName"] = ".1.3.6.1.2.1.1.5.0"
	# 	# oids["sysDescr"] = ".1.3.6.1.2.1.1.1.0"
	# 	oids["sysObjectID"] = ".1.3.6.1.2.1.1.2.0"

	# 	for destination in dests.split():
	# 		for oid_val in oids.values():
	# 			p = packet( destination, community, oid_val, False)

	# 	asyncore.loop()

	def draw(self, filename = 'path.png', host_labl = 'rid', edge_labl = 'cost'):

		G = nx.Graph()
		labels = {}
		labels_edge = {}

		print json.dumps( self.jsonTree, sort_keys=True, indent=4, separators=(',', ': ') )

		for pid in self.jsonTree:

			print pid

		for local_remote_rid in self.jsonTree[pid]:
			logging.info( '%s ( %s )' % ( self.jsonTree[pid][local_remote_rid]['hostname'], local_remote_rid ) )
			G.add_node(local_remote_rid)
			for intf in self.jsonTree[pid][local_remote_rid]['path']:
				logging.info( '%s - %s' % ( intf, self.jsonTree[pid][local_remote_rid]['path'][intf]) )

				if host_labl == 'hostname':
					labels[local_remote_rid] = self.jsonTree[pid][local_remote_rid]['hostname']
				elif host_labl == 'rid':
					labels[local_remote_rid] = local_remote_rid
				
				remote_remote_rid = self.jsonTree[pid][local_remote_rid]['path'][intf]['rid']

				if edge_labl == 'cost':
					choose_what_show = self.jsonTree[pid][local_remote_rid]['path'][intf]['cost']
				elif edge_labl == 'area':
					choose_what_show = self.jsonTree[pid][local_remote_rid]['path'][intf]['area']
				elif edge_labl == 'netype':
					choose_what_show = reduce_netype( self.jsonTree[pid][local_remote_rid]['path'][intf]['netype'] )
				elif edge_labl == 'int':
					choose_what_show = reduce_interface_name( intf )

				labels_edge[(local_remote_rid, remote_remote_rid)] = choose_what_show
				G.add_edge(local_remote_rid, remote_remote_rid)

		pos = nx.spring_layout(G)

		nx.draw(G, pos)
		nx.draw_networkx(G, pos, labels=labels, font_size=10)

		nx.draw_networkx_edge_labels(G, pos, with_labels=True, edge_labels=labels_edge, label_pos=0.75, font_size=10)

		plt.savefig(filename)
		logging.info( 'printing draw to %s' % (filename) )