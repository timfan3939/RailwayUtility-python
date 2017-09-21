#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#coding=utf-8

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import cgi
import cgitb
cgitb.enable()

from CommonHTML import *

print( 'Content-Type: text/html\n\n' )
print( '<meta charset="utf8" />')
print( '<meta name="viewport" content="width=device-width, initial-scale=1.0">' )
print( 'Hello World!<br/>' )

timetable = RUTimeTable()
	
LoadStation( timetable )
LoadTRAJsonTimetable( timetable, '/var/www/html/RUpy/file/20170913.json', encoding='utf-8' )
timetable.SortAllNode()

printForm( timetable )

print('<h1><a href="../transport.html">Please Go Here for main site</a></h1><br />')
print('<h2><a href="../ganglia/">System Info Monitored by Ganglia</a></h2><br />')

