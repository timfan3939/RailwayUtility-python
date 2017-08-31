#!/usr/bin/env python3

import json
from RUTimeTable import *
from datetime import datetime, time

# TrainInfos
# |- Type
# |- Train
# |- BreastFeed
# |- Route
# |- Package
# |- OverNightStn
# |- LineDir
# |- Line
# |- Dinning
# |- Cripple
# |- CarClass
# |- Bike
# |- Note
# |- NoteEng
# \- TimeInfos
#    |- Route
#    |- Station
#    |- Order
#    |- DepTime
#    |- ArrTime

def LoadTRAJsonTimetable(timetable, filename, encoding = None):
	with open(filename, encoding = encoding) as inputJson:
		data = json.load(inputJson)
	
	for trainInfo in data['TrainInfos']:
		id = trainInfo['Train']
					
		newTrain = RUTTTrainNode(id)
			
		for timeInfo in trainInfo['TimeInfos']:	
			arrTime = None
			DepTime = None
			stationId = None
			station = None
			
			try:
				stationID = int(timeInfo['Station'])
			except ValueError:
				print('Station ID Error at Train {}: {}.'.format(newTrain.id, timeInfo['Station']))
				print('Skip this station.')
				continue
			
			station = timetable.station_dict_by_id[stationID]
			
			try:
				arrTime = datetime.strptime(timeInfo['ArrTime'],'%H:%M:%S').time()
			except ValueError:
				print('ArrTime Error at Train {} and Station {}({}): {}'.format(newTrain.id, station.name, station.id, timeInfo['ArrTime']))
				print('ArrTime set to None')
				arrTime = None
			
			try:
				depTime = datetime.strptime(timeInfo['DepTime'],'%H:%M:%S').time()
			except ValueError:
				print('depTime Error at Train {} and Station {}({}): {}'.format(newTrain.id, station.name, station.id, timeInfo['DepTime']))
				print('Deptime set to None')
				depTime = None
				
			arrTTnode = RUTTNode(station, newTrain, arrTime, RUTTNodeType.RUTTArrival)
			depTTnode = RUTTNode(station, newTrain, depTime, RUTTNodeType.RUTTDeparture)
			newTrain.schedules.append(arrTTnode)
			newTrain.schedules.append(depTTnode)
			
			station.schedules.append(arrTTnode)
			station.schedules.append(depTTnode)			
			
			#print(trainInfo['Train'], station.name, arrTime, '->', depTime)
		#print()
		timetable.all_train_list.append(newTrain)
		newTrain = None

def LoadStation(timetable):
	newLine = None
	newStation = None
	with open('file/TRAStation.csv', encoding = 'utf8') as stations:
		for line in stations:
			subLine = line.strip('\r\n\t').split(',')
			if subLine[0] == '':
				timetable.line_list.append(newLine)
				newLine = None
			elif subLine[0] != '' and subLine[1] == '' and subLine[2] == '' and subLine[3] == '' and subLine[4] == '':
				newLine = RULineListNode(subLine[0])
			elif subLine[0] == 'Seq':
				continue
			else:
				if subLine[2] == '':
					continue
					
				id1 = int(subLine[2])
				newStation = timetable.AddStation(subLine[3], id1)
				milestone = subLine[4]
				try:
					milestone = float(subLine[4])
				except ValueError:
					milestone = 0			
				
				newLine.line_stations.append(RULineStationListNode(newStation, milestone))
		if newLine is not None:
			timetable.line_list.append(newLine)
				
					
				
			

def main():
	m_timetable = RUTimeTable()
	LoadStation(m_timetable)
	
	for l in m_timetable.line_list:
		print(l)
		for s in l.line_stations:
			print('    ', s)
		print()
		
	LoadTRAJsonTimetable(m_timetable, 'file/20170913.json', encoding = 'utf8')
	
	m_timetable.all_train_list.sort()
	for train in m_timetable.all_train_list:
		print('第{}次:'.format(train.id))
		
		train.schedules.sort()
		
		for time in train.schedules:
			print('    {} {}'.format(time.station.name, time.time_stamp))
		print()
	
	for station in m_timetable.all_station_list:
		print('{}車站時刻表'.format(station.name))
		station.schedules.sort()
		for time in station.schedules:
			print('    {:4} - {}'.format(time.train.id, time.time_stamp))
		print()

if __name__ == '__main__':
	main()