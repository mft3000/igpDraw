# igpDraw

Quick and dirty script with the purpose of retrieving igp adjiaciencies parameters and draw it on an image for tshooting purpose

![alt tag](https://github.com/mft3000/igpDraw/blob/master/ospf_doc.png)

a. from json '-j'

	```
	python igpDraw.py -c topology.list
	```

b. inline node list '-c'

	1. from file

		```
		python igpDraw.py -c topology.list
		```

	2. from cli

		```
		python igpDraw.py -c 1.1.1.1 2.2.2.2 3.3.3.3 4.4.4.4
		```

	3. simulate retrieve data from device '--demo'

		```
		python igpDraw.py --demo -c []
		```

	4. use '-s' to save the the discovery (even for demo) as 'auto_save_file.json'. 
	   in this way you can load configuration again with '-j' option

		```
		python igpDraw.py -c 1.1.1.1 2.2.2.2 3.3.3.3 4.4.4.4 -s
		```

c. by defaults the connections lines will carry igp cost informations. with '-a' you can specify what draw in the image {cost,int,area,netype}

	interface name
	```
	python igpDraw.py --demo -c [] -a int
	```
	area number
	```
	python igpDraw.py --demo -c [] -a area
	```

	area network type 
	```
	python igpDraw.py --demo -c [] -a netype
	```

d. draw 'rid' as node label '-n' (hostnames are defaults)

	```
	python igpDraw.py --demo -c [] -n rid
	```

e. specify output filename with '-f'

	```
	python igpDraw.py --demo -c [] -f topo.png
	```

f. choose IGP protocol (only OSPF for now)

	```
	python igpDraw.py --demo -c [] -I OSPF
	```

g. use '-r' and '--cmd' to query device and show results

	```
	python igpDraw.py -r 10.64.0.250 --cmd sh ip ro 1.1.1.1
	sh ip ro 1.1.1.1
	% Network not in table

	Nothing to do... exiting
	```

## json schema
```
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
                    "ANC": "#",
                    "NC": "#",
                    "pid": "#"
				}
			}
		}
	}
}
```
## To Do List

1. multiple fixing (for eg. data retrieve with multiple ios version and types)
2. more accurate images with labels, colors, multiarea igp data info ecc..
3. ISIS as another IGP protocol
4. SNMP for retrieve IGP informations
5. API REST with flask
6. draw dotten line if the link is not primary (cost too high): draw a tree