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
		self.schedules = []
		self.operate_days = ''
		self.departure_station = None
		self.destination_station = None
		
	def __str__ (self):
		return str.format( 'RUTTTrainNode\n-\\{0}', self.id )
	
class RULineStationListNode:
	def __init__ (self, station, milestone):
		self.station = station
		self.milestone = milestone

class RULineListNode:
	def __init__ (self, name):
		self.name = name
		self.line_stations = []

class RUTimeTable:
	def __init__ (self):
		self.line_list = []
		self.all_station_list = []
		self.all_train_list = []
		self.sort_on_node_added = True
	
	def StartBulkAddNode(self):
		self.sort_on_node_added = False
	
	def StopBulkAddNode(self):
		for station in self.all_station_list:
			station.schedules.sort()
		for train in self.all_train_list:
			train.schedules.sort()
		self.sort_on_node_added = True
	
	def AddTTNode(self, station, train, time_stamp, type):
		node = (station, train, time_stamp, type)
		train.schedules.append(node)
		station.schedules.append(node)
		if self.sort_on_node_added:
			train.schedules.sort()
			station.schedules.sort()
	
	def FindTrain(self, id):
		pass
		# TODO here
		

def main():
	# Create Time Table instance
	timetable = RUTimeTable()
	
	# Create 10 Stations
	for i in range(10):
		newStation = RUTTStationNode( str.format('SN {}', i), 100 + i )
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
		line1.line_stations.append( RULineStationListNode(timetable.all_station_list[index[i]], milestone[i] ) )
	
	# Add Stations to Line 2
	#
	# 7 -  2 - 4 - 8 - 9
	index = [7,  2,  4,  8,  9]
	milestone = [0,  2,  5,  6,  7]
	for i in range( len(index) ):
		line2.line_stations.append( RULineStationListNode(timetable.all_station_list[index[i]], milestone[i] ) )
	
	# Add station to timetable
	timetable.line_list.append(line1)
	timetable.line_list.append(line2)
	
	# Add Trains 10x to Line 1
	# Test case Train added first
	for i in range(1, 10, 2):
		train = RUTTTrainNode( str.format('10{}', i) )
		for j in range( len(line1.line_stations) ):
			if j != 0:
				train.schedules.append( RUTTNode( line1.line_stations[j], train,  300+30*i+3*j, RUTTNodeType.RUTTArrival ) )
			if j != len(line1.line_stations):
				train.schedules.append( RUTTNode( line1.line_stations[j], train, 300+30*i+3*j+1, RUTTNodeType.RUTTDeparture ) )
		timetable.all_train_list.append(train)
	
	# TODO: transfer train's schedule to station's schedule
	
	
	print('All Stations')
	for i in timetable.all_station_list:
		print(i.name, i.id)
	print('-'*20)
	print('All Lines')
	for i in timetable.line_list:
		print(i.name)
		for j in i.line_stations:
			print(' ', j.station.name, j.milestone)
	
	print('-'*20)
	print('All Train')
	for i in timetable.all_train_list:
		print('Train No.', i.id)
		for j in i.schedules:
			print ( j.station.station.name, j.time_stamp )
		print()
	pass
	

if __name__ == '__main__':
	main()