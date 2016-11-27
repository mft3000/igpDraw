
# ver 0.2
#
# changelog
#
# 0.1 start init
# 0.2 graph ok
#

class Discovery(object):

	json = {
		'172.31.1.1': {
			'hostname' : 'LA',
			'os' : 'ios',
			'path' : {
				'e0.12': {
					'rid' : '172.31.2.2', 
					'area' : '0',
					'cost' : '1',
					'net' : 'point-to-point'
				},
				'e0.13': {
					'rid' : '172.31.3.3', 
					'area' : '0',
					'cost' : '1',
					'net' : 'point-to-point'
				}
			}
		},
		'172.31.2.2': {
			'hostname' : 'SA',
			'os' : 'ios',
			'path' : {
				'e0.12': {
					'rid' : '172.31.1.1', 
					'area' : '0',
					'cost' : '2',
					'net' : 'point-to-point'
				},
				'e0.24': {
					'rid' : '172.31.4.4', 
					'area' : '0',
					'cost' : '2',
					'net' : 'point-to-point'
				},
				'e0.23': {
					'rid' : '172.31.3.3', 
					'area' : '0',
					'cost' : '2',
					'net' : 'point-to-point'
				}
			}
		},
		'172.31.3.3': {
			'hostname' : 'SF',
			'os' : 'xr',
			'path' : {
				'e0.13': {
					'rid' : '172.31.1.1', 
					'area' : '0',
					'cost' : '2',
					'net' : 'point-to-point'
				},
				'e0.23': {
					'rid' : '172.31.2.2', 
					'area' : '0',
					'cost' : '2',
					'net' : 'point-to-point'
				}
			}
		},
		'172.31.4.4': {
			'hostname' : 'NY',
			'os' : 'ios',
			'path' : {
				'e0.12': {
					'rid' : '172.31.2.2', 
					'area' : '0',
					'cost' : '1',
					'net' : 'point-to-point'
				},
				'e0.18': {
					'rid' : '172.31.5.5', 
					'area' : '0',
					'cost' : '1',
					'net' : 'point-to-point'
				}
			}
		},
		'172.31.5.5': {
			'hostname' : 'CHI',
			'os' : 'xr',
			'path' : {
				'e0.12': {
					'rid' : '172.31.4.4', 
					'area' : '0',
					'cost' : '100',
					'net' : 'point-to-point'
				},
				'e0.15': {
					'rid' : '172.31.3.3', 
					'area' : '0',
					'cost' : '100',
					'net' : 'point-to-point'
				}
			}
		}
	}

	def showJson(self):
		return self.json