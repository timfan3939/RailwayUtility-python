#!/usr/bin/env python3

import json
import RUTimeTable

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

def LoadTRAJsonTimetable(filename, encoding = None):
	with open(filename, encoding = encoding) as inputJson:
		data = json.load(inputJson)
	
	for trainInfo in data['TrainInfos']:
		print(trainInfo['Train'], trainInfo['Note'])

def LoadStation():
	pass

def main():
	LoadTRAJsonTimetable('file/20170913.json', encoding = 'utf8')

if __name__ == '__main__':
	main()