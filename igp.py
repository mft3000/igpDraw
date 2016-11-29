#!/usr/bin/env python

# ver 0.2
#
# changelog
#
# 0.1 start init
# 0.11 minor fix
# 0.2 adjust in retrive ospf data functions
# 

# import argparse, os, logging
# from scapy.all import SNMP
# from socket import socket, AF_INET, SOCK_DGRAM

# import asyncore

# class packet(asyncore.file_dispatcher):

#     dst = str()
#     comm = str()
#     oid = str()

#     def __init__(self, dst, comm, oid, debug = False):
#         asyncore.dispatcher.__init__(self)

#         self.dst = dst
#         self.comm = comm
#         self.oid = oid
#         self.debug = debug

#         self.create_socket(AF_INET, SOCK_DGRAM)
#         self.connect((self.dst, 161))

#     def handle_read(self):

#         r = SNMP( self.recv(4096) )

#         if self.debug:
#             logging.debug( r.show() )                                                                                                                 
#             logging.debug( hexdump(r) )         

#         print self.dst, '[', self.comm, ']',
#         print r[SNMPvarbind].oid.val, '-', r[SNMPvarbind].value.val

#         self.handle_close()

#     def writable(self):
#         return False

#     def handle_connect(self):
#         snmp = SNMP(community=self.comm,PDU=SNMPget(varbindlist=[SNMPvarbind(oid=self.oid)]))

#         buf = str( snmp )
#         while buf:
#             bytes = self.send( buf )
#             buf = buf[bytes:]

#     def handle_close(self):
#         self.close()

#     def handle_expt(self):
#         self.close()












# def stripAfterDot(var):
# 	try:
# 		ix = var.index('.')
# 		return var[:ix]
# 	except:
# 		return var

# def resolve_sysObjectIDNG_v02(host, comm=str(os.environ['PYCOMM'])):
# 	#
# 	# translation hostname/ip -> oid -> name, platform, os, version     by snmp
# 	#
	
# 	if not PreChecks(host, comm):
# 		return "unkn", "unkn enterprise.9.1.x", "ios", "unkn"
		
# 	load("RFC1213-MIB")					# sysName, ecc..
	
# 	m = M(host, comm, version=2, none=True, timeout=0.1)
		
# 	oid = str(m.sysObjectID)
	
# 	x = oid.split(".")[-1]
# 	with open(str(os.environ['DEV']) + '/libs/mib.list', 'r') as mibs:
# 		for mib in mibs:
# 			if mib.split()[1].split(".")[-1] == x:
# 				return str(m.sysName), mib.split()[0] + " (ent.9.1." + x + ")", mib.split()[2], showVer(str(m.sysDescr))

# 		return "unkn", "unkn enterprise.9.1." + x, "ios", "unkn"

import collections, os, re, json

from Exscript.protocols import Telnet
#from Exscript.protocols import SSH2
from Exscript import Account

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

tree = lambda: collections.defaultdict(tree)
	
class Device(object):
	
	_hostname = None
	_community = None
	_opsys = 'ios'
	_platform = None
	_version = None
	
	ospfDevice = tree()
	
	_remote_connection = None
	_remote_credentials = None
	
	def __init__(self, ip, comm = str(os.environ['PYCOMM']) ):

		self._community = comm
		
		# n, p, o, v = resolve_sysObjectIDNG_v02(ip)
		
		self._ip = ip
		self._hostname = ip
		# self._hostname = mftCustom.stripAfterDot(n)
		# self._platform = p
		# self._opsys = o
		# self._version = v
		
		# self.ospfDevice[self._hostname]['platform'] = self._platform
		# self.ospfDevice[self._hostname]['opsys'] = self._opsys
		# self.ospfDevice[self._hostname]['version'] = self._version
		
	def __str__(self):
	
		logging.info("print __str__()...")
		
		return json.dumps(self.ospfDevice, sort_keys=True, indent=4, separators=(',', ': '))
		
	@property
	def remote_connection(self):

		return self._remote_connection

	@remote_connection.setter
	def remote_connection(self, connection):

		self._remote_connection = connection

	@property
	def remote_credentials(self):

		return self._remote_credentials

	@remote_credentials.setter
	def remote_credentials(self, credentials):

		self._remote_credentials = credentials

	def remote_connect(self, credentials, host=None, resolve = True):

		connection = Telnet()

		host = host or self._hostname
		ip = self._ip
		
		logging.debug("host %s..." % (host))
		logging.debug("ip %s..." % (ip))
		logging.debug(self._opsys)
		
		if resolve:
			target = host
		else:
			target = ip
		logging.debug("enter target %s..." % (target))

		try:
			connection.connect(target)
			connection.set_driver(self._opsys)
			logging.debug("DONE")
		except Exception, err:
			logging.debug("1. FAILED CONNECTION")
			return False
		logging.debug("enter credentials host %s..." % (target))
		try:
			logging.debug(credentials['username'])
			logging.debug(credentials['password'])
			logging.debug(credentials['enable'])
			account = Account(credentials['username'],
							  credentials['password'],
							  credentials['enable'])
			connection.login(account)
			logging.debug("DONE")
		except Exception, err:
			logging.debug("2. FAILED AUTH")
			return False

		self.remote_connection = connection
		self.remote_credentials = credentials
		return True

	def remote_execute(self, command):

		connection = self.remote_connection
		host = self._hostname
		try:
			connection.execute(command)
			logging.debug("remote command execute '%s'" % (command))
		except Exception, err:
			return False

		return str(connection.response)

	def remote_close(self, connection=None):

		host = self._hostname
		connection = connection or self.remote_connection
		try:
			connection.send('exit\r')
			logging.debug("exit host")
			connection.close(True)
		except Exception, err:
			return False

		return True

class ISIS(Device):
	
	pid = ''
	net = ''
	hostname = ''

	igpNeighbors = tree()

	def set_hostname(self, os = 'ios'):

		raws = self.remote_execute("term len 0")
		raws = self.remote_execute("sh run | i hostname")

		for line in raws.splitlines():
				if 'hostname' in line:
					self.hostname = line.split()[1]

class OSPF(Device):
	
	pid = ''
	rid = ''
	hostname = ''

	igpNeighbors = tree()

	intfLists = []

	def set_hostname(self, os = 'ios'):

		raws = self.remote_execute("term len 0")
		raws = self.remote_execute("sh run | i hostname")

		for line in raws.splitlines():
				if 'hostname' in line:
					self.hostname = line.split()[1]

	def show_ospf(self, os = 'ios'):

		self.set_hostname()

		raws = self.remote_execute("show ip ospf")
		
		# raws = '''
		 # Routing Process "ospf 123" with ID 2.2.2.2
		 # Start time: 6w2d, Time elapsed: 00:11:01.952
		 # Supports only single TOS(TOS0) routes
		 # Supports opaque LSA
		 # Supports Link-local Signaling (LLS)
		 # Supports area transit capability
		 # Event-log enabled, Maximum number of events: 1000, Mode: cyclic
		 # Router is not originating router-LSAs with maximum metric
		 # Initial SPF schedule delay 5000 msecs
		 # Minimum hold time between two consecutive SPFs 10000 msecs
		 # Maximum wait time between two consecutive SPFs 10000 msecs
		 # Incremental-SPF disabled
		 # Minimum LSA interval 5 secs
		 # Minimum LSA arrival 1000 msecs
		 # LSA group pacing timer 240 secs
		 # Interface flood pacing timer 33 msecs
		 # Retransmission pacing timer 66 msecs
		 # Number of external LSA 0. Checksum Sum 0x000000
		 # Number of opaque AS LSA 0. Checksum Sum 0x000000
		 # Number of DCbitless external and opaque AS LSA 0
		 # Number of DoNotAge external and opaque AS LSA 0
		 # Number of areas in this router is 1. 1 normal 0 stub 0 nssa
		 # Number of areas transit capable is 0
		 # External flood list length 0
		 # IETF NSF helper support enabled
		 # Cisco NSF helper support enabled
		 # Reference bandwidth unit is 100 mbps
		 #    Area BACKBONE(0) (Inactive)
		 #        Number of interfaces in this area is 3
			# Area has no authentication
			# SPF algorithm last executed 00:10:42.800 ago
			# SPF algorithm executed 1 times
			# Area ranges are
			# Number of LSA 1. Checksum Sum 0x005F46
			# Number of opaque link LSA 0. Checksum Sum 0x000000
			# Number of DCbitless LSA 0
			# Number of indication LSA 0
			# Number of DoNotAge LSA 0
			# Flood list length 0
		# '''

		# print raws

		for line in raws.splitlines():
			if 'Routing Process' in line:
				self.rid = line.split('with ID')[1].split()[0]
				self.pid = line.split('with ID')[0].split()[-1].replace('\"','')
				break

		print self.pid, self.rid

	def show_ospf_neighbor(self, os = 'ios'):

		raws = self.remote_execute("show ip ospf neighbor")

# 		raws = '''10.199.199.137  1    FULL/DR       0:00:31    192.168.80.37      Ethernet0
# 172.16.48.1     1    FULL/DROTHER  0:00:33    172.16.48.1        Ethernet1
# 172.16.48.200   1    FULL/DROTHER  0:00:33    172.16.48.200      Ethernet2
# 10.199.199.137  5    FULL/DR       0:00:33    172.16.48.189      Ethernet3
# '''

		for line in raws.splitlines():
			if re.search('^\d+.', line):
				logging.debug( line ) 
				intf = line.split()[-1]
				self.intfLists.append( intf )
				self.igpNeighbors[self.pid][self.rid]['path'][intf]['state'] = line.split()[2]
				self.igpNeighbors[self.pid][self.rid]['path'][intf]['rid'] = line.split()[0]

		# print json.dumps(self.igpNeighbors, sort_keys=True, indent=4, separators=(',', ': '))

	def show_ospf_interface(self, os = 'ios'):

		self.show_ospf()

		raws = self.remote_execute("show ip ospf interface")
		
		# raws = '''
		# Ethernet 0 is up, line protocol is up 
		#  Internet Address 10.32.0.251/11, Area 0 
		#  Process ID 123, Router ID 1.1.1.1, Network Type BROADCAST, Cost: 1
		#  Transmit Delay is 1 sec, State DR, Priority 1
		#  Designated Router (ID) 1.1.1.1, Interface address 10.32.0.251
		#  No backup designated router on this network
		#  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
		#  oob-resync timeout 40
		#  Hello due in 00:00:02
		#  Supports Link-local Signaling (LLS)
		#  Cisco NSF helper support enabled
		#  IETF NSF helper support enabled
		#  Index 1/1, flood queue length 0
		#  Next 0x0(0)/0x0(0)
		#  Last flood scan length is 0, maximum is 0
		#  Last flood scan time is 0 msec, maximum is 0 msec
		#  Neighbor Count is 0, Adjacent neighbor count is 0 
		#  Suppress hello for 0 neighbor(s)
		# Vlan1 is up, line protocol is up 
		#  Internet Address 10.64.0.250/11, Area 0 
		#  Process ID 123, Router ID 1.1.1.1, Network Type BROADCAST, Cost: 1
		#  Transmit Delay is 1 sec, State DR, Priority 1
		#  Designated Router (ID) 1.1.1.1, Interface address 10.64.0.250
		#  No backup designated router on this network
		#  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
		#  oob-resync timeout 40
		#  Hello due in 00:00:02
		#  Supports Link-local Signaling (LLS)
		#  Cisco NSF helper support enabled
		#  IETF NSF helper support enabled
		#  Index 1/1, flood queue length 0
		#  Next 0x0(0)/0x0(0)
		#  Last flood scan length is 0, maximum is 0
		#  Last flood scan time is 0 msec, maximum is 0 msec
		#  Neighbor Count is 0, Adjacent neighbor count is 0 
		#  Suppress hello for 0 neighbor(s)
		# '''

		self.igpNeighbors[self.pid][self.rid]["hostname"] = self.hostname
		self.igpNeighbors[self.pid][self.rid]["os"] = "ios"

		#print self.intfLists

		intf = ''

		for line in raws.splitlines():

			if 'is up' in line:
				# intf = "".join((line.split()[0], line.split()[1]))
				intf = line.split()[0]

				# if intf not in self.intfLists:
				# 	break
				continue

			if 'Loopback' not in intf:
				if 'Process ID' in line:
					self.igpNeighbors[self.pid][self.rid]['path'][intf]['pid'] = line.split(',')[0].split()[-1]
				if 'Router ID' in line:
					self.igpNeighbors[self.pid][self.rid]['path'][intf]['rid'] = ''
				if 'Area' in line:
					self.igpNeighbors[self.pid][self.rid]['path'][intf]['area'] = line.split(',')[-1].split()[1]
				if 'Cost:' in line:
					self.igpNeighbors[self.pid][self.rid]['path'][intf]['cost'] = line.split(',')[-1].split()[1]
				if 'Network Type' in line:
					self.igpNeighbors[self.pid][self.rid]['path'][intf]['netype'] = line.split(',')[-2].split()[2]
				if 'Neighbor Count is' in line:
					self.igpNeighbors[self.pid][self.rid]['path'][intf]['NC'] = line.split(',')[0].split()[-1]
				if 'Adjacent neighbor count is' in line:
					self.igpNeighbors[self.pid][self.rid]['path'][intf]['ANC'] = line.split(',')[1].split()[-1]

		self.show_ospf_neighbor()

		return self.igpNeighbors