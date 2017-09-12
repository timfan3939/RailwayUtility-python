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

_ = '一'

def main():
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
	table += '<table><thead><th>車次</th><th>{}</th><th>--></th><th>{}</th></thead><tbody>'.format(station1.name, station2.name)

	
	for node in station1.schedules:
		if node.node_type in {RUTTNodeType.RUTTArrival, RUTTNodeType.RUTTUnknown}:
			continue
		train = node.train
		for node2 in station2.schedules:
			if node2.train.id == train.id and \
			   node2.node_type in {RUTTNodeType.RUTTArrival, RUTTNodeType.RUTTBypass} and \
			   train.schedules.index(node) < train.schedules.index(node2):	
				table += '<tr><td>{}次</td><td>{}</td><td>--></td><td>{}</td></tr>'.format(train.id, node.time_stamp, node2.time_stamp)
	table += '</tbody></table>'

	print(table)

	
def printForm(timetable = None):
	if timetable is None:
		return

	selection = ''
	for station in timetable.all_station_list:
		selection += '<option value="{}">{}: {}</option>'.format(station.id, station.id, station.name)

	content = ''
	content += '<form method="POST" action="RunningTime.cgi">'
	content += '起始站：<select name="sta1">'
	content += selection
	content += '</select><br />'
	content += '終點站：<select name="sta2">'
	content += selection
	content += '</select><br />'
	content += '<input type="submit" value="送出" />'
	content += '</form>'
	
	print(content)
	

if __name__ == '__main__':
	print('Content-Type: text/html; charset=utf-8\n')
	print('<meta charset="utf-8">')
	main()
