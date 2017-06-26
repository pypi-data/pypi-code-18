
class Device(object):
	__slots__ = ['status', 'hash', 'db_id', 
				 'address', 'device_id',
				 'connection',
				 ]


class Status(object):
    __slots__ = ['alert', 'position', 'voltages',
    			 'inputs', 'device'
    			 ]

    
