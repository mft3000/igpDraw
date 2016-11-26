
# ver 0.1
#
# changelog
#
# 0.1 start init
#

import networkx as nx
import matplotlib.pyplot as plt

class Discovery(object):

	json = {
		'R1': {
			'rid' : '172.31.1.1',
			'path' : {
				'R2': {
					'int' : 'e0.12', 
					'cost' : '1',
					'net' : 'p2p'
				},
				'R3': {
					'int' : 'e0.13', 
					'cost' : '1',
					'net' : 'p2p'
				}
			}
		},
		'R2': {
			'rid' : '172.31.2.2',
			'path' : {
				'R1': {
					'int' : 'e0.12', 
					'cost' : '1',
					'net' : 'p2p'
				},
				'R4': {
					'int' : 'e0.24', 
					'cost' : '10',
					'net' : 'p2p'
				},
				'R5': {
					'int' : 'e0.25', 
					'cost' : '1',
					'net' : 'p2p'
				}
			}
		},
		'R3': {
			'rid' : '172.31.3.3',
			'path' : {
				'R1': {
					'int' : 'e0.13', 
					'cost' : '1',
					'net' : 'p2p'
				}
			}
		},
		'R4': {
			'rid' : '172.31.4.4',
			'path' : {
				'R2': {
					'int' : 'e0.24', 
					'cost' : '10',
					'net' : 'p2p'
				},
				'R5': {
					'int' : 'e0.45', 
					'cost' : '1',
					'net' : 'p2p'
				}
			}
		},
		'R5': {
			'rid' : '172.31.5.5',
			'path' : {
				'R2': {
					'int' : 'e0.25', 
					'cost' : '1',
					'net' : 'p2p'
				},
				'R4': {
					'int' : 'e0.45', 
					'cost' : '1',
					'net' : 'p2p'
				}
			}
		}
	}

	def showJson(self):
		return self.json