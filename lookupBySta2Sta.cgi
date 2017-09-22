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
	print( '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">' )

def main():
	print( '<body>' )
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
	table += '<table width="100%">'
	table += '<thead>'
	table += '<tr>'
	table += '<th>車次</th>'
	table += '<th>{}</th>'.format(station1.name)
	table += '<th>{}</th>'.format('-->')
	table += '<th>{}</th>'.format(station2.name)
	table += '<th>{}</th>'.format('行駛時間')
	table += '</tr>'
	table += '</thead>'
	table += '<tbody>'

	
	for node in station1.schedules:
		if node.node_type in {RUTTNodeType.RUTTArrival, RUTTNodeType.RUTTUnknown}:
			continue
		train = node.train
		for node2 in station2.schedules:
			if node2.train.id == train.id and \
			   node2.node_type in {RUTTNodeType.RUTTArrival, RUTTNodeType.RUTTBypass} and \
			   train.schedules.index(node) < train.schedules.index(node2):
				table += '<tr>'
				table += '<td><a href="lookupByTrainID.cgi?id={}">{}次</a></td>'.format(train.id, train.id)
				table += '<td>{}</td>'.format(node.time_stamp)
				table += '<td>--></td>'
				table += '<td>{}</td>'.format(node2.time_stamp)
				table += '<td>{}</td>'.format('?')
				table += '</tr>'
	table += '</tbody></table>'

	print(table)
	
	print( '</body>' )

	
	

if __name__ == '__main__':
	print('Content-Type: text/html; charset=utf-8\n')
	print( '<HTML lang="utf-8">')
	printHead()
	main()
	print( '</HTML>' )
