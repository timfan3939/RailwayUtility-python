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

def main():
	print('<head><title>Look up timetable</title>')
	print( '<meta name="viewport" content="width=device-width, initial-scale=1.0">' )
	print('</head>')

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
	

	
	print('Train No. {}<br />'.format(train.id))
	print('<table>')
	print('<thead><tr><th>{}</th><th>&nbsp;</th><th>{}</th><th>{}</th></tr></thead>'.format('車站', '抵達時間', '開車時間'))
	print('<tbody>')

	i = 0
	while i < len(train.schedules):
		node = train.schedules[i]
		i += 1

		if node.node_type == RUTTNodeType.RUTTArrival or node.node_type == RUTTNodeType.RUTTStopOnly:
			if i < len(train.schedules) and train.schedules[i].station == node.station:
				node2 = train.schedules[i]
				i += 1
				print('<tr><td>{}</td><td>↓</td><td>{}</td><td>{}</td></tr>'.format( node.station.name, node.time_stamp, node2.time_stamp ))
			else:
				print('<tr><td>{}</td><td>↓</td><td>{}</td><td>{}</td></tr>'.format( node.station.name, node.time_stamp, ''))
		else:
			print('<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format( node.station.name, '', node.time_stamp))
	

	print('</tbody>')
	print('</table>')


if __name__ == '__main__':
	print('Content-Type: text/html; charset=utf-8 \n\n')
	print('<meta charset="utf-8" />')
	main()


