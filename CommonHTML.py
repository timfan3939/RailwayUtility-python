#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#coding=utf-8

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from RUJson import *
from RUTimeTable import *
from datetime import time


def printForm(timetable = None):
	if timetable is None:
		return

	selection = ''
	for station in timetable.all_station_list:
		selection += '<option value="{}">{}: {}</option>'.format(station.id, station.id, station.name)

	content = ''
	content += '<form method="POST" action="RunningTime.cgi">'
	content += '<fieldset><legend>起迄站</legend>'
	content += '起始站：<select name="sta1">'
	content += selection
	content += '</select><br />'
	content += '終點站：<select name="sta2">'
	content += selection
	content += '</select><br />'
	content += '<input type="submit" value="送出" />'
	content += '</fieldset>'
	content += '</form>'
	
	content += '<p />'

	content += '<form method="POST" action="lookup.cgi">'
	content += '<fieldset><legend>以車次查詢</legend>'
	content += '車次：<input name="id" /><br /><input type="submit" value="送出" />'
	content += '</fieldset>'
	content += '</form>'

	print(content)


