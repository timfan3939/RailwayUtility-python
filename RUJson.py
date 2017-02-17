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

def main():
	with open('file/20161106.json', encoding='utf8') as inputJson:
		data = json.load(inputJson)
	
	for trainInfo in data['TrainInfos']:
		print(trainInfo['Train'], trainInfo['Note'])

if __name__ == '__main__':
	main()