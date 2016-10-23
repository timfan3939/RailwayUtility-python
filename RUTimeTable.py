from enum import Enum

class RUTTNodeType (Enum):
	RUTTArrival = 0x01
	RUTTDeparture = 0x02
	RUTTBypass = 0x03
	RUTTStopOnly = 0x04
	RUTTUnknown = 0x05
	
class RUTTNode:
	def __init__(self, thisStation, thisTrain, timeStamp, nodeType):
		self.thisStation = thisStation
		self.thisTrain = thisTrain
		self.timeStamp = timeStamp
		self.nodeType = nodeType
	
	def __str__(self):
		return str.format('RUTTNode\n|- {0}\n|- {1}\n|- {2}\n\\- {3}', self.thisStation, self.thisTrain, self.timeStamp, self.nodeType)
	
class RUTTStationNode:
	def __init__ (self, name, id):
		self.name = name
		self.id = id
		self.schedules = []
		self.existLine = []
	
	def __str__(self):
		return str.format('RUTTStationNode\n|- {0}\n\\- {1}', self.name, self.id)

class RUTTTrainNode:
	def __init__ (self, id):
		self.id = id
		schedule = []
		operateDay = ''
		departureStation = None
		destinationStation = None
		
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
		self.lineList = []
		self.allStationList = []
		self.allTrainList = []


def main():
	# Create Time Table instance
	timetable = RUTimeTable()

	# Create Lines and Stations
	line = RULineListNode('主線')
	timetable.lineList.append(line)
	
	print (timetable.lineList)
	

if __name__ == '__main__':
	main()