
# ver 0.3
#
# changelog
#
# 0.1 start init
# 0.2 graph ok
# 0.3 move to obj, add draw options, add argparse, add demo, add read .list, add read .json
#

import argparse

from lib_app import NetDiscovery

def main():

	parser = argparse.ArgumentParser(description="")

	parser.add_argument("-i", "--ilist", nargs = '+', default = None )
	parser.add_argument("-j", "--json", default = None)
	parser.add_argument("-I", "--igp", default = "ospf")
	parser.add_argument("-l", "--hostlabel", choices=["hostname", "rid"], default = "hostname")
	parser.add_argument("-o", "--adjlabel", choices=["cost", "int", "area", "netype"], default = "cost")
	parser.add_argument("-f", "--filename", default = "path.png")

	args = parser.parse_args()
	
	##################################################

	choose = args.adjlabel
	filename = args.filename
	igp = args.igp
	hl = args.hostlabel
	jsonFile = args.json
	input_list = args.ilist

	ilist = []

	if jsonFile:

		d = NetDiscovery( jsonFile = jsonFile )

	elif input_list:

		if '.list' not in ''.join(input_list):

			ilist_var = input_list

		else:

			try:
				with open(''.join(input_list)) as f:
					ilist_var = f.read().splitlines()
			except:
				print 'file does not exist'

		d = NetDiscovery( input_list = ilist_var )

		for node in ilist_var:
			print "retrieve %s info under %s" % (igp, node)
			d.igp( igp, node )
	else:
		print 'Nothing to do... exiting'
		exit()
	
	d.draw( filename = filename, host_labl = hl, edge_labl = choose )

if __name__ == "__main__":
	main()