
# ver 0.3
#
# changelog
#
# 0.1 start init
# 0.2 graph ok
# 0.3 move to obj, add draw options, add argparse, add demo, add read .list, add read .json
#

import collections, json, re
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

	igpNeighbors = tree()
	rid = ''
	pid = ''

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

	def demoRandom(self, list_to_random, avoid_duplicates = False):

		choose = list_to_random[randint(1,len(list_to_random) - 1)]
		if avoid_duplicates:
			list_to_random.remove( choose )

		return choose

	def show_ospf(self, os = 'ios'):

		raws = '''
		Routing Process "ospf 201" with ID 10.0.0.1 and Domain ID 10.20.0.1 
		  Supports only single TOS(TOS0) routes 
		  Supports opaque LSA 
		  SPF schedule delay 5 secs, Hold time between two SPFs 10 secs 
		  Minimum LSA interval 5 secs. Minimum LSA arrival 1 secs 
		  LSA group pacing timer 100 secs 
		  Interface flood pacing timer 55 msecs 
		  Retransmission pacing timer 100 msecs 
		  Number of external LSA 0. Checksum Sum 0x0      
		  Number of opaque AS LSA 0. Checksum Sum 0x0      
		  Number of DCbitless external and opaque AS LSA 0 
		  Number of DoNotAge external and opaque AS LSA 0 
		  Number of areas in this router is 2. 2 normal 0 stub 0 nssa 
		  External flood list length 0 
		     Area BACKBONE(0) 
		         Number of interfaces in this area is 2 
		         Area has message digest authentication 
		         SPF algorithm executed 4 times 
		         Area ranges are 
		         Number of LSA 4. Checksum Sum 0x29BEB  
		         Number of opaque link LSA 0. Checksum Sum 0x0      
		         Number of DCbitless LSA 3 
		         Number of indication LSA 0 
		         Number of DoNotAge LSA 0 
		         Flood list length 0 
		     Area 172.16.26.0 
		         Number of interfaces in this area is 0 
		         Area has no authentication 
		         SPF algorithm executed 1 times 
		         Area ranges are 
		            192.168.0.0/16 Passive Advertise  
		         Number of LSA 1. Checksum Sum 0x44FD   
		         Number of opaque link LSA 0. Checksum Sum 0x0      
		         Number of DCbitless LSA 1 
		         Number of indication LSA 1 
		         Number of DoNotAge LSA 0 
		         Flood list length 0
		'''


		for line in raws.splitlines():
			if 'Routing Process' in line:
				self.rid = line.split('with ID')[1].split()[0]
				self.pid = line.split('with ID')[0].split()[-1].replace('\"','')
				break


	def show_ospf_neighbor(self, os = 'ios'):

		self.show_ospf()

		raws = '''10.199.199.137  1    FULL/DR       0:00:31    192.168.80.37      Ethernet0
172.16.48.1     1    FULL/DROTHER  0:00:33    172.16.48.1        Ethernet1
172.16.48.200   1    FULL/DROTHER  0:00:33    172.16.48.200      Ethernet2
10.199.199.137  5    FULL/DR       0:00:33    172.16.48.189      Ethernet3
'''

		for line in raws.splitlines():
			if re.match('^\d+.', line):
				intf = line.split()[-1]
				self.igpNeighbors[self.pid][self.rid][intf]['rrid'] = line.split()[0]
				self.igpNeighbors[self.pid][self.rid][intf]['state'] = line.split()[2]

		return json.dumps(self.igpNeighbors, sort_keys=True, indent=4, separators=(',', ': '))

	def show_ospf_interface(self, os = 'ios'):	

		self.show_ospf_neighbor()
		
		raws = '''
		Ethernet 0 is up, line protocol is up
		 Internet Address 192.168.254.202, Mask 255.255.255.0, Area 0.0.0.0
		 AS 201, Router ID 192.77.99.1, Network Type BROADCAST, Cost: 10
		 Transmit Delay is 1 sec, State Up, Priority 1
		 Designated Router id 192.168.254.10, Interface address 192.168.254.10
		 Backup Designated router id 192.168.254.28, Interface addr 192.168.254.28
		 Timer intervals configured, Hello 10, Dead 60, Wait 40, Retransmit 5
		 Hello due in 0:00:05
		 Neighbor Count is 8, Adjacent neighbor count is 2
		  Adjacent with neighbor 192.168.254.28  (Backup Designated Router)
		'''

		for line in raws.splitlines():
			if 'is up' in line:
				intf = "".join((line.split()[0], line.split()[1]))
				continue
			if 'Area' in line:
				self.igpNeighbors[self.pid][self.rid][intf]['area'] = line.split(',')[-1].split()[1]
			if 'Cost' in line:
				self.igpNeighbors[self.pid][self.rid][intf]['cost'] = line.split(',')[-1].split()[1]
			if 'Network Type' in line:
				self.igpNeighbors[self.pid][self.rid][intf]['netype'] = line.split(',')[-2].split()[2]

		return json.dumps(self.igpNeighbors, sort_keys=True, indent=4, separators=(',', ': '))

	def igp(self, igp = 'ospf', node = None, demo = True, save_as_file = False , os = 'ios' ):

		if demo:
			logging.info("generate json for node")

			self.jsonTree["201"].update( {
			 	node : {
			 		"hostname" : self.demoRandom( self.demo_code , avoid_duplicates= True ), 
			 		"os" : "ios",
			 		"path" : {
			 			"e0.12": {
			 				"rid" : self.demoRandom( self.input_list ), 
			 				"area" : "0",
			 				"cost" : randint(1, 100),
			 				"netype" : "p2p",
			 				"state" : "Up"
			 			}
			 		}
			 	}
			} )

			#print json.dumps(self.jsonTree, sort_keys=True, indent=4, separators=(',', ': ')) 

		if save_as_file:
			self.save_topology_as_file()

	def save_topology_as_file(self, filename = "auto_save_file.json"):

			logging.info( 'save topology as %s for further draws' % (filename) )

			out_file_name_json = open( filename, "w")
			print >> out_file_name_json, json.dumps( self.jsonTree, sort_keys=True, indent=4, separators=(',', ': ') )
			out_file_name_json.close()

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
					choose_what_show = self.jsonTree[pid][local_remote_rid]['path'][intf]['netype']
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