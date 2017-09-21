#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#coding=utf-8

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import cgi

import cgitb
#cgitb.enable(display = 0, logdir = '/var/log/RUTT/', format='txt')
cgitb.enable(display = 0, logdir = '/home/timfan3939/log/', format='txt')

from RUJson import *
from RUTimeTable import *
from datetime import time

from CommonHTML import *

_ = '一'

def printHead():
	print( '<head><title>RailwayUtility Python</title>' )
	printMeta()
	print( '</head>' )

def printMeta():
	print( '<meta charset="utf-8" \> ')
	print( '<meta name="viewport" content="width=device-width, initial-scale=1.0" \>' )

def main():
	print( '<body' )
	timetable = RUTimeTable()
	
	LoadStation( timetable )
	LoadTRAJsonTimetable( timetable, '/var/www/html/RUpy/file/20170913.json', encoding='utf-8' )
	timetable.SortAllNode()
	timetable.UpdateStationDict()
	
	printForm(timetable)

	form = cgi.FieldStorage()
	if 'sta1' not in form or 'sta2' not in form:
		return

	sta1 = int(form['sta1'].value)
	sta2 = int(form['sta2'].value)
	
	
	station1 = timetable.station_dict_by_id[ sta1 ]
	station2 = timetable.station_dict_by_id[ sta2 ]
	
	table = ''
	table += '<table><thead><th>車次</th><th>{}</th><th>--></th><th>{}</th><th>{}</th></thead><tbody>'.format(station1.name, station2.name, '行駛時間')

	
	for node in station1.schedules:
		if node.node_type in {RUTTNodeType.RUTTArrival, RUTTNodeType.RUTTUnknown}:
			continue
		train = node.train
		for node2 in station2.schedules:
			if node2.train.id == train.id and \
			   node2.node_type in {RUTTNodeType.RUTTArrival, RUTTNodeType.RUTTBypass} and \
			   train.schedules.index(node) < train.schedules.index(node2):	
				table += '<tr><td>{}次</td><td>{}</td><td>--></td><td>{}</td><td>{}</td></tr>'.format(train.id, node.time_stamp, node2.time_stamp, '?')
	table += '</tbody></table>'

	print(table)
	
	print( '</body>' )

	
	

if __name__ == '__main__':
	print('Content-Type: text/html; charset=utf-8\n')
	printHead()
	main()
