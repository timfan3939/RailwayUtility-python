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
		return str.format('RUTTNode\n|- {0}\n|- {1}\n|- {2}\n\\- {3}', self.station, self.train, self.time_stamp, self.node_type)

	def __lt__(self, other):
		return (self.time_stamp < other.time_stamp) or (self.train.id < other.train.id)

	def __le__(self, other):		
		return (self.time_stamp <= other.time_stamp) or (self.train.id <= other.train.id)

	def __eq__(self, other):
		return (self.time_stamp == other.time_stamp) and (self.train.id == other.train.id)

	def __ne__(self, other):
		return not self == other

	def __gt__(self, other):
		return (self.time_stamp > other.time_stamp) or (self.train.id > other.train.id)

	def __ge__(self, other):
		return (self.time_stamp >= other.time_stamp) or (self.train.id >= other.train.id)


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
		self.station_dict_by_id = {}
		self.station_dict_by_name = {}
		
	def UpdateStationDict(self):
		self.station_dict_by_id		= { s.id : s for s in self.all_station_list }
		self.station_dict_by_name 	= { s.name : s for s in self.all_station_list }
	
	def SortAllNode(self):
		for station in self.all_station_list:
			station.schedules.sort()
		for train in self.all_train_list:
			train.schedules.sort()

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
		newStation = RUTTStationNode( str.format('SN{}', i), 100 + i )
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
	
	localTrainMainLineOffset1 = [	('SN0',  5, RUTTNodeType.RUTTDeparture),
									('SN1', 11, RUTTNodeType.RUTTArrival),
									('SN1', 12, RUTTNodeType.RUTTDeparture),
									('SN2', 19, RUTTNodeType.RUTTArrival),
									('SN2', 20, RUTTNodeType.RUTTDeparture),
									('SN3', 27, RUTTNodeType.RUTTArrival),
									('SN3', 33, RUTTNodeType.RUTTDeparture),
									('SN4', 40, RUTTNodeType.RUTTArrival),
									('SN4', 41, RUTTNodeType.RUTTDeparture),
									('SN5', 48, RUTTNodeType.RUTTArrival),
									('SN5', 49, RUTTNodeType.RUTTDeparture),
									('SN6', 56, RUTTNodeType.RUTTArrival)]
					
	localTrainMainLineOffset2 = [	('SN6',  5, RUTTNodeType.RUTTDeparture),
									('SN5', 11, RUTTNodeType.RUTTArrival),
									('SN5', 12, RUTTNodeType.RUTTDeparture),
									('SN4', 19, RUTTNodeType.RUTTArrival),
									('SN4', 20, RUTTNodeType.RUTTDeparture),
									('SN3', 27, RUTTNodeType.RUTTArrival),
									('SN3', 33, RUTTNodeType.RUTTDeparture),
									('SN2', 40, RUTTNodeType.RUTTArrival),
									('SN2', 41, RUTTNodeType.RUTTDeparture),
									('SN1', 48, RUTTNodeType.RUTTArrival),
									('SN1', 49, RUTTNodeType.RUTTDeparture),
									('SN0', 56, RUTTNodeType.RUTTArrival)]
	
	fastTrainMainLineOffset1 = [	('SN0', 11, RUTTNodeType.RUTTDeparture),
									('SN1', 17, RUTTNodeType.RUTTBypass),
									('SN2', 23, RUTTNodeType.RUTTArrival),
									('SN2', 24, RUTTNodeType.RUTTDeparture),
									('SN3', 30, RUTTNodeType.RUTTBypass),
									('SN4', 36, RUTTNodeType.RUTTArrival),
									('SN4', 37, RUTTNodeType.RUTTDeparture),
									('SN5', 43, RUTTNodeType.RUTTBypass),
									('SN6', 49, RUTTNodeType.RUTTArrival)]
	
	fastTrainMainLineOffset2 = [	('SN6', 11, RUTTNodeType.RUTTDeparture),
									('SN5', 17, RUTTNodeType.RUTTBypass),
									('SN4', 23, RUTTNodeType.RUTTArrival),
									('SN4', 24, RUTTNodeType.RUTTDeparture),
									('SN3', 30, RUTTNodeType.RUTTBypass),
									('SN2', 36, RUTTNodeType.RUTTArrival),
									('SN2', 37, RUTTNodeType.RUTTDeparture),
									('SN1', 43, RUTTNodeType.RUTTBypass),
									('SN0', 49, RUTTNodeType.RUTTArrival)]
	
	
	localTrainExtLineOffset1 = [	('SN7', 16, RUTTNodeType.RUTTDeparture),
									('SN2', 23, RUTTNodeType.RUTTArrival),
									('SN2', 24, RUTTNodeType.RUTTDeparture),
									('SN4', 36, RUTTNodeType.RUTTArrival),
									('SN4', 41, RUTTNodeType.RUTTDeparture),
									('SN8', 48, RUTTNodeType.RUTTArrival),
									('SN8', 49, RUTTNodeType.RUTTDeparture),
									('SN9', 56, RUTTNodeType.RUTTArrival)]
	
	localTrainExtLineOffset2 = [	('SN7', 48, RUTTNodeType.RUTTArrival),
									('SN2', 41, RUTTNodeType.RUTTDeparture),
									('SN2', 36, RUTTNodeType.RUTTArrival),
									('SN4', 34, RUTTNodeType.RUTTDeparture),
									('SN4', 33, RUTTNodeType.RUTTArrival),
									('SN8', 26, RUTTNodeType.RUTTDeparture),
									('SN8', 25, RUTTNodeType.RUTTArrival),
									('SN9', 18, RUTTNodeType.RUTTDeparture)]
	
	timetable.UpdateStationDict()
	
	for i in range(3):
		trainID = 201 + i * 2
		train = RUTTTrainNode( str(trainID) )
		for node in localTrainMainLineOffset1:
			stationName = node[0]
			station = timetable.station_dict_by_name[node[0]]
			time = (6+i)*3600 + node[1]*60
			type = node[2]
			newNode = RUTTNode(station, train, time, type)
			train.schedules.append(newNode)
			station.schedules.append(newNode)
		timetable.all_train_list.append(train)
		
		trainID = 202 + i * 2
		train = RUTTTrainNode( str(trainID) )
		for node in localTrainMainLineOffset2:
			stationName = node[0]
			station = timetable.station_dict_by_name[node[0]]
			time = (6+i)*3600 + node[1]*60
			type = node[2]
			newNode = RUTTNode(station, train, time, type)
			train.schedules.append(newNode)
			station.schedules.append(newNode)
		timetable.all_train_list.append(train)
			
		
		trainID = 301 + i * 2
		train = RUTTTrainNode( str(trainID) )
		for node in fastTrainMainLineOffset1:
			stationName = node[0]
			station = timetable.station_dict_by_name[node[0]]
			time = (6+i)*3600 + node[1]*60
			type = node[2]
			newNode = RUTTNode(station, train, time, type)
			train.schedules.append(newNode)
			station.schedules.append(newNode)
		timetable.all_train_list.append(train)
		
		trainID = 302 + i * 2
		train = RUTTTrainNode( str(trainID) )
		for node in fastTrainMainLineOffset2:
			stationName = node[0]
			station = timetable.station_dict_by_name[node[0]]
			time = (6+i)*3600 + node[1]*60
			type = node[2]
			newNode = RUTTNode(station, train, time, type)
			train.schedules.append(newNode)
			station.schedules.append(newNode)
		timetable.all_train_list.append(train)
			
		trainID = 401 + i * 2
		train = RUTTTrainNode( str(trainID) )
		for node in localTrainExtLineOffset1:
			stationName = node[0]
			station = timetable.station_dict_by_name[node[0]]
			time = (6+i)*3600 + node[1]*60
			type = node[2]
			newNode = RUTTNode(station, train, time, type)
			train.schedules.append(newNode)
			station.schedules.append(newNode)
		timetable.all_train_list.append(train)
		
		trainID = 402 + i * 2
		train = RUTTTrainNode( str(trainID) )
		for node in localTrainExtLineOffset2:
			stationName = node[0]
			station = timetable.station_dict_by_name[node[0]]
			time = (6+i)*3600 + node[1]*60
			type = node[2]
			newNode = RUTTNode(station, train, time, type)
			train.schedules.append(newNode)
			station.schedules.append(newNode)
		timetable.all_train_list.append(train)
	
	timetable.SortAllNode()

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
			print ( j.station.name, divmod(j.time_stamp/60,60) )
		print()
		
	print('-'*20)
	for i in timetable.all_station_list:
		print('Station ', i.name)
		for j in i.schedules:
			print( j.train.id, divmod(j.time_stamp/60,60), j.node_type)
		print()
	pass



if __name__ == '__main__':
	main()
