from enum import Enum
from operator import attrgetter

class RUTTNodeType (Enum):
	RUTTArrival = 0x01
	RUTTDeparture = 0x02
	RUTTBypass = 0x03
	RUTTStopOnly = 0x04
	RUTTUnknown = 0x05
	
class RUTTNode:
	def __init__(self, station, train, time_stamp, node_type):
		self.station = station
		self.train = train
		self.time_stamp = time_stamp
		self.node_type = node_type
	
	def __str__(self):
		return str.format('RUTTNode\n|- {0}\n|- {1}\n|- {2}\n\\- {3}', self.station, self.train, self.time_stamp, self.node_Type)
		
	def __lt__(self, other):
		if self.train.id != other.train.id:
			return self.time_stamp < other.time_stamp
		return self.train.id < other.train.id
	
	def __le__(self, other):
		if self.train.id != other.train.id:
			return self.time_stamp <= other.time_stamp
		return self.train.id <= other.train.id
	
	def __eq__(self, other):
		return (self <= other and self >= other)
	
	def __ne__(self, other):
		return not self == other
	
	def __gt__(self, other):
		if self.train.id != other.train.id:
			return self.time_stamp > other.time_stamp
		return self.train.id > other.train.id
	
	def __ge__(self, other):
		if self.train.id != other.train.id:
			return self.time_stamp >= other.time_stamp
		return self.train.id >= other.train.id
		
	
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
	def __init__ (self, station, milestone):
		self.station = station
		self.milestone = milestone

class RULineListNode:
	def __init__ (self, name):
		self.name = name
		self.line = []

class RUTimeTable:
	def __init__ (self):
		self.line_list = []
		self.all_station_list = []
		self.all_train_list = []
	


def main():
	# Create Time Table instance
	timetable = RUTimeTable()
	
	# Create 10 Stations
	for i in range(10):
		newStation = RUTTStationNode( str.format('Station{}', i), 100 + i )
		timetable.all_station_list.append(newStation)
	
	timetable.all_station_list.sort(key=attrgetter('id') )
				
	# Create Two Lines
	line1 = RULineListNode('主線')
	line2 = RULineListNode('副線')
	
	# Add Stations to Line 1
	# 
	# 0 - 1 - 2 - 3 - 4 - 5 - 6 
	index = [0,  1,  2,  3,  4,  5,  6]
	milestone = [0,  1,  2,  3,  4,  5,  6]
	for i in range( len(index) ):
		line1.line.append( RULineStationListNode(timetable.all_station_list[index[i]], milestone[i] ) )
	
	# Add Stations to Line 2
	#
	# 7 -  2 - 4 - 8 - 9
	index = [7,  2,  4,  8,  9]
	milestone = [0,  2,  5,  6,  7]
	for i in range( len(index) ):
		line2.line.append( RULineStationListNode(timetable.all_station_list[index[i]], milestone[i] ) )
	
	# Add station to timetable
	timetable.line_list.append(line1)
	timetable.line_list.append(line2)
	
	
	print('All Stations')
	for i in timetable.all_station_list:
		print(i.name, i.id)
	print('-'*20)
	print('All Lines')
	for i in timetable.line_list:
		print(i.name)
		for j in i.line:
			print(' ', j.station.name, j.milestone)
	pass
	

if __name__ == '__main__':
	main()