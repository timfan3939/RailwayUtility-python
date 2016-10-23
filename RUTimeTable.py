from enum import Enum

class RUTTNodeType (Enum):
	RUTTArrival = 0x01
	RUTTDeparture = 0x02
	RUTTBypass = 0x03
	RUTTStopOnly = 0x04
	RUTTUnknown = 0x05
	
class RUTTNode:
	def __init__(self, this_station, this_train, time_stamp, node_type):
		self.this_station = this_station
		self.this_train = this_train
		self.time_stamp = time_stamp
		self.node_type = node_type
	
	def __str__(self):
		return str.format('RUTTNode\n|- {0}\n|- {1}\n|- {2}\n\\- {3}', self.this_station, self.this_train, self.time_stamp, self.node_Type)
	
class RUTTStationNode:
	def __init__ (self, name, id):
		self.name = name
		self.id = id
		self.schedules = []
		self.exist_lines = []
	
	def __str__(self):
		return str.format('RUTTStationNode\n|- {0}\n\\- {1}', self.name, self.id)

class RUTTTrainNode:
	def __init__ (self, id):
		self.id = id
		schedule = []
		operate_days = ''
		departure_station = None
		destination_station = None
		
	def __str__ (self):
		return str.format( 'RUTTTrainNode\n-\\{0}', self.id )
	
class RULineStationListNode:
	def __init__ (self):
		self.station = None
		self.distance = -1

class RULineListNode:
	def __init__ (self, name):
		self.name = name
		line = None

class RUTimeTable:
	def __init__ (self):
		self.line_list = []
		self.all_station_list = []
		self.all_train_list = []
	


def main():
	# Create Time Table instance
	timetable = RUTimeTable()

	# Create Lines and Stations
	line = RULineListNode('主線')
	timetable.line_list.append(line)
	
	print (timetable.line_list)
	

if __name__ == '__main__':
	main()