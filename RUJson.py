#!/usr/bin/env python3

import json
from RUTimeTable import *

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
		for timeInfo in trainInfo['TimeInfos']:
			print(trainInfo['Train'], timetable.station_dict_by_id[int(timeInfo['Station'])].name, timeInfo['DepTime'])
		print()

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

if __name__ == '__main__':
	main()