# igpDraw

Quick and dirt script with the purpose of retrieving igp adjiaciencies parameters and draw it on an image for tshooting purpose

![alt tag](https://github.com/mft3000/igpDraw/blob/master/path.png)

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
				}
			}
		}
	}
}
```
## To Do List

1. ISIS as another IGP protocol
2. SNMP for retrieve IGP informations
3. API REST with flask
4. draw dotten line if the link is not primary (cost too high): draw a tree
