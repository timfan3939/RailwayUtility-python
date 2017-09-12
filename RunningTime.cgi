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
	
	
	printForm()
	
def printForm():
	content = ''
	content += '<form method="POST" action="RUpy/RunningTime.cgi">'
	content += '起始站：<input name="sta1" /><br />'
	content += '終點站：<input name="sta2" /><br />'
	content += 'input type="submit" value="送出" />'
	content += '</form>'
	
	print(content)
	

if __name__ == '__main__':
	print('Content-Type: text/html; charset=utf-8\n')
	print('<meta charset="utf-8">')
	main()