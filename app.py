
# ver 0.4
#
# changelog
#
# 0.1 start init
# 0.2 graph ok
# 0.3 move to obj, add draw options, add argparse, add demo, add read .list, add read .json
#>0.4 edit variables, add show ospf commands 
#

import argparse

from lib_app import NetDiscovery

def main():

	parser = argparse.ArgumentParser(description="")

	parser.add_argument("-c", "--clilist", nargs = '+', default = None )
	parser.add_argument("-j", "--json", default = None)
	parser.add_argument("-I", "--igp", default = "ospf")
	parser.add_argument("-n", "--nodelabel", choices=["hostname", "rid"], default = "hostname")
	parser.add_argument("-a", "--adjlabel", choices=["cost", "int", "area", "netype" ], default = "cost")
	parser.add_argument("-f", "--filename", default = "path.png")

	parser.add_argument("--community", default = "pubblic")

	args = parser.parse_args()
	
	##################################################

	adj_show_choose = args.adjlabel
	filename = args.filename
	igp = args.igp
	nodelabel = args.nodelabel
	jsonFile = args.json
	cli_input_list = args.clilist

	ilist = []

	if jsonFile:

		d = NetDiscovery( jsonFile = jsonFile )

	elif cli_input_list:

		if '.list' not in ''.join(cli_input_list):

			cli_input_list_variable = cli_input_list

		else:

			try:
				with open(''.join(cli_input_list)) as cli_input_list_as_file:
					cli_input_list_variable = cli_input_list_as_file.read().splitlines()
			except:
				print 'file does not exist'
				exit()

		d = NetDiscovery( input_list = cli_input_list_variable )

		for node in cli_input_list_variable:
			print( 'retrieve %s info under %s' % (igp, node) )
			d.igp( igp, node, save_as_file = False)
	else:
		print 'Nothing to do... exiting'
		exit()
	
	d.draw( filename = filename, host_labl = nodelabel, edge_labl = adj_show_choose )

if __name__ == "__main__":
	main()