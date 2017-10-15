#!/usr/bin/env python3

from xml.dom.minidom import *
from RUTimeTable import *
from datetime import datetime, time, timedelta


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
	
	print(xmlRoot.tagName)
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
	

def main():
	m_timetable = RUTimeTable()
	LoadStation(m_timetable)
	
	for line in m_timetable.line_list:
		print(line.name)
		for sta in line.line_stations:
			print(sta)
	LoadTHSRCXMLTimetable(m_timetable, 'file/20171016.xml', 'utf-8')
	
	m_timetable.all_train_list.sort()
	m_timetable.SortAllNode()
	
	for train in m_timetable.all_train_list:
		print('Train {}'.format(train.id))
		
		for time in train.schedules:
			print('    {} {}'.format(time.station.name, time.time_stamp))
			

if __name__ == '__main__':
	main()