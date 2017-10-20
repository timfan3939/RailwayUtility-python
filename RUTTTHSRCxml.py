#!/usr/bin/env python3

from xml.dom.minidom import *
from RUTimeTable import *
from datetime import datetime, time, timedelta, date


def LoadStation(timetable):
	stationName = ['南港', '臺北', '板橋', '桃園', '新竹', '苗栗', '臺中', '彰化', '雲林', '嘉義', '臺南', '左營']
	stationid = [990, 1000, 1010, 1020, 1030, 1035, 1040, 1043, 1047, 1050, 1060, 1070]
	line = RULineListNode('臺灣高鐵')
	
	for i in range(12):
		newStation = timetable.AddStation(stationName[i], stationid[i])
		line.line_stations.append(RULineStationListNode(newStation, 1.0) )
	
	timetable.line_list.append(line)

def LoadTHSRCXMLTimetable(timetable, filename, encoding = None):
	xmlFile = xml.dom.minidom.parse(filename)
	xmlRoot = xmlFile.documentElement
	
	if xmlRoot.tagName != 'TWHSRTrainList':
		print('Error parsing the root of document')
		return
	
	trains = xmlRoot.getElementsByTagName('TrainInfo')
	
	for train in trains:		
		newTrain = timetable.AddTrain(train.getAttribute('Train'))
		newTrain.direction = train.getAttribute('LineDir')
		
		schedules = train.getElementsByTagName('TimeInfo')		
		length = len(schedules)
		
		for schedule in schedules:
			arrTime = schedule.getAttribute('ARRTime')
			depTime = schedule.getAttribute('DEPTime')
			stationId = int(schedule.getAttribute('Station'))
			station = timetable.station_dict_by_id[stationId]
			order = int(schedule.getAttribute('Order'))
			
			
			if order != 1:			
				arrTime = datetime.strptime(arrTime,'%H%M').time()
				arrTTNode = RUTTNode(station, newTrain, arrTime, RUTTNodeType.RUTTArrival)
				newTrain.schedules.append(arrTTNode)
				station.schedules.append(arrTTNode)
			
			if order != length:
				depTime = datetime.strptime(depTime,'%H%M').time()				
				depTTNode = RUTTNode(station, newTrain, depTime, RUTTNodeType.RUTTDeparture)				
				newTrain.schedules.append(depTTNode)				
				station.schedules.append(depTTNode)
				
				
#           staA        staB
#  TrainA  node1  -->  node3
#    ...   
#  TrainB  node2  -->  node4
	
				
def ComputeByPass(timetable):
	len_trainList = len(timetable.all_train_list)
	dummyDate = date(2017,1,1)
	
	for num_traA in range(len_trainList):
		for num_traB in range(num_traA+1, len_trainList):
			trainA = timetable.all_train_list[num_traA]
			trainB = timetable.all_train_list[num_traB]
			
			if trainA.direction != trainB.direction:
				continue
			
			for node1 in trainA.schedules:
				
				staA = node1.station				
				index1sta = staA.schedules.index(node1)
				
				node2 = None
				for index2sta in range(0, len(staA.schedules)):
					if staA.schedules[index2sta].train == trainB:
						node2 = staA.schedules[index2sta]
						break
				
				if node2 is None:
					continue
					
				index1tra = trainA.schedules.index(node1)
				node4found = False
				for index3tra in range(index1tra+1, len(trainA.schedules)):
					if node4found is True:
						break
						
					node3 = trainA.schedules[index3tra]
					
					staB = node3.station
					index3sta = staB.schedules.index(node3)
					
					node4 = None
					for index4sta in range(0, len(staB.schedules)):
						if staB.schedules[index4sta] == node2:
							continue
						if staB.schedules[index4sta].train == trainB:
							node4 = staB.schedules[index4sta]
							break
						
					if node4 is None:
						continue

					time1 = datetime.combine(dummyDate, node1.time_stamp)
					time2 = datetime.combine(dummyDate, node2.time_stamp)
					time3 = datetime.combine(dummyDate, node3.time_stamp)
					time4 = datetime.combine(dummyDate, node4.time_stamp)
											
					node4found = True	
											
					
					if time1 < time2 and time3 < time4:
						continue
					elif time1 > time2 and time3 > time4:
						continue	
					
					PrintSquare(node1, node2, node3, node4)

					
def PrintSquare(node1, node2, node3, node4):
	str = ''
	schA = node1.train.schedules
	schB = node2.train.schedules
	indexA = schA.index(node1)
	indexB = schB.index(node2)
	
	str = '{:>4}-> '.format(node1.train.id)	
	while indexA < len(schA):
		node = schA[indexA]
		str += '{}-{} '.format(node.station.name, node.time_stamp)
		if node == node3:
			break
		indexA += 1
	str += '\n'
	
	str += '{:>4}-> '.format(node2.train.id)
	while indexB < len(schB):
		node = schB[indexB]
		str += '{}-{} '.format(node.station.name, node.time_stamp)
		if node == node4:
			break
		indexB+= 1
	str += '\n'

	print(str)
		
		
	

def main():
	m_timetable = RUTimeTable()
	LoadStation(m_timetable)
	
#	for line in m_timetable.line_list:
#		print(line.name)
#		for sta in line.line_stations:
#			print(sta)
	LoadTHSRCXMLTimetable(m_timetable, 'file/20171016.xml', 'utf-8')
	
	m_timetable.all_train_list.sort()
	m_timetable.SortAllNode()
	
#	for train in m_timetable.all_train_list:
#		print('Train {}'.format(train.id))
#		
#		for time in train.schedules:
#			print('    {} {}'.format(time.station.name, time.time_stamp))
			
	ComputeByPass(m_timetable)
			

if __name__ == '__main__':
	main()