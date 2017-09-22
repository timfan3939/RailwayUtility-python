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
	form  = cgi.FieldStorage()
	if 'id' not in form:
		print('<H1>ID is not given</H1>')
		return
		
	timetable = RUTimeTable()
	
	LoadStation( timetable )
	LoadTRAJsonTimetable( timetable, '/var/www/html/RUpy/file/20170913.json', encoding='utf-8' )
	timetable.SortAllNode()	
	
	printForm( timetable )

	trainID = form['id'].value
	if trainID not in timetable.train_dict_by_id:
		print('<H1> Train No. {} does not exists.</H1>'.format(trainID))
		return
		
	train = timetable.train_dict_by_id[trainID]
	
	
	table = ''
	table += 'Train No. {}<br />'.format(train.id)
	table += '<table>'
	table += '<thead>'
	table += '<tr>'
	table += '<th></th>'.format('順序')
	table += '<th></th>'.format('車站')
	table += '<th></th>'.format('&nbsp;')
	table += '<th></th>'.format('抵達時間')
	table += '<th></th>'.format('開車時間')	
	table += '</tr>'
	table += '</thead>'
	
	table += '<tbody>'
	
	i = 0
	counter = 0
	while i < len(train.schedules):
		node = train.schedules[i]
		i += 1
		counter += 1

		if node.node_type == RUTTNodeType.RUTTArrival or node.node_type == RUTTNodeType.RUTTStopOnly:
			if i < len(train.schedules) and train.schedules[i].station == node.station:
				node2 = train.schedules[i]
				i += 1
				table += '<tr>'
				table += '<td>{}</td>'.format(counter)
				table += '<td>{}</td>'.format(node.station.name)
				table += '<td>↓</td>'
				table += '<td>{}</td>'.format(node.time_stamp)
				table += '<td>{}</td>'.format(node2.time_stamp)
				table += '</tr>'
			else:
				table += '<tr>'
				table += '<td>{}</td>'.format(counter)
				table += '<td>{}</td>'.format(node.station.name)
				table += '<td>↓</td>'
				table += '<td>{}</td>'.format(node.time_stamp)
				table += '<td>{}</td>'.format('&nbsp;')
				table += '</tr>'
		else:
			table += '<tr>'
			table += '<td>{}</td>'.format(counter)
			table += '<td>{}</td>'.format(node.station.name)
			table += '<td>↓</td>'
			table += '<td>{}</td>'.format('&nbsp;')
			table += '<td>{}</td>'.format(node.time_stamp)
			table += '</tr>'
	

	table += '</tbody>'
	table += '</table>'
	
	print( table )
	print( '</body>' )


if __name__ == '__main__':
	print('Content-Type: text/html; charset=utf-8\n')
	printHead()
	main()
