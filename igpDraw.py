#!/usr/bin/env python

# ver 0.61
#
# changelog
#
# 0.1 start init
# 0.2 graph ok
# 0.3 move to obj, add draw options, add argparse, add demo, add read .list, add read .json
# 0.4 edit variables, add show ospf commands 
# 0.5 device telnet, discovery and build json
# 0.51 minor fix
# 0.55 add control in -c number of elements
# 0.61 add -r and --cmd to query device and show results (eg. show ip route 1.1.1.1)
#

import argparse, os

from igpDrawLib import NetDiscovery, auth_cred
from igp import Device

def lenCheck(obj):

	if len(obj) < 2:
		print 'WARNING: only one node to draw... exiting'
		exit(0)

def main():

	parser = argparse.ArgumentParser(description="")

	parser.add_argument("-c", "--clilist", nargs = '+', default = None )
	parser.add_argument("-j", "--json", default = None)
	parser.add_argument("-I", "--igp", default = "ospf")
	parser.add_argument("-n", "--nodelabel", choices=["hostname", "rid"], default = "hostname")
	parser.add_argument("-a", "--adjlabel", choices=["cost", "int", "area", "netype" ], default = "cost")
	parser.add_argument("-f", "--filename", default = "path.png")
	parser.add_argument("--demo", action='store_true', default = False)
	parser.add_argument("-s", "--save", action='store_true', default = False)

	parser.add_argument("--community", default = '' )

	parser.add_argument("-r","--router", default = '' )
	parser.add_argument("--cmd", nargs = '+', default = None )

	args = parser.parse_args()
	
	##################################################

	adj_show_choose = args.adjlabel
	filename = args.filename
	igp = args.igp
	nodelabel = args.nodelabel
	jsonFile = args.json
	cli_input_list = args.clilist
	demo = args.demo
	save = args.save

	cmd = args.cmd
	router = args.router

	if cmd:
		dev = Device(router)

		credentials = auth_cred('local', True)
		status = dev.remote_connect(credentials)

		print dev.remote_execute(' '.join(cmd))

	community = os.environ['PYCOMM'] if args.community == '' else args.community

	ilist = []

	if jsonFile:

		d = NetDiscovery( jsonFile = jsonFile )

	elif cli_input_list:

		if '.list' not in ''.join(cli_input_list):

			# lenCheck(cli_input_list)

			cli_input_list_variable = cli_input_list

		else:

			try:
				with open(''.join(cli_input_list)) as cli_input_list_as_file:
					# lenCheck(cli_input_list_as_file.read().splitlines())
					cli_input_list_variable = cli_input_list_as_file.read().splitlines()
			except:
				print 'file does not exist'
				exit()

		lenCheck(cli_input_list_variable)

		d = NetDiscovery( input_list = cli_input_list_variable )

		for node in cli_input_list_variable:
			print( 'retrieve %s info under %s' % (igp, node) )
			d.igp( igp, node, save_as_file = save, demo = demo, community = community )
	else:
		print 'Nothing to do... exiting'
		exit()
	
	d.draw( filename = filename, host_labl = nodelabel, edge_labl = adj_show_choose )

if __name__ == "__main__":
	main()