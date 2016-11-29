
a. from json '-j'

	'''
	python app.py -c topology.list
	'''

b. inline node list '-c'

	1. from file

		'''
		python app.py -c topology.list
		'''

	2. from cli

		'''
		python app.py -c 1.1.1.1 2.2.2.2 3.3.3.3 4.4.4.4
		'''

	3. simulate retrieve data from device '--demo'

		'''
		python app.py --demo -c []
		'''

c. by defaults the connections lines will carry igp cost informations. with '-a' you can specify what draw in the image {cost,int,area,netype}

	interface name
	'''
	python app.py --demo -c [] -a int
	'''
	area number
	'''
	python app.py --demo -c [] -a area
	'''

	area network type 
	'''
	python app.py --demo -c [] -a netype
	'''

d. draw 'rid' as node label '-n' (hostnames are defaults)

	'''
	python app.py --demo -c [] -n rid
	'''

e. specify output filename with '-f'

	'''
	python app.py --demo -c [] -f topo.png
	'''

f. choose IGP protocol (only OSPF for now)

	'''
	python app.py --demo -c [] -I OSPF
	'''

==== json schema

{
	"pid" : {
		"rid or node" : {
			"hostname" : "xxxxx", 
			"os" : "ios",
			"path" : {
				"e0.12": {
					"rid" : "x.x.x.x", 
					"area" : "0|0.0.0.0|...",
					"cost" : "10|...",
					"netype" : "BROADCAST|POINT_TO_POINT|...",
					"state" : "Up|DOWN|..."
				}
			}
		}
	}
}

==== To Do List

1. ISIS as another IGP protocol
2. SNMP for retrieve IGP informations
3. API REST
4. draw dotten line if the link is not primary (cost too high): draw a tree