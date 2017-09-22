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
	print( '<h1>RailwayUtility Python</h1>' )

	timetable = RUTimeTable()
		
	LoadStation( timetable )
	LoadTRAJsonTimetable( timetable, '/var/www/html/RUpy/file/20170913.json', encoding='utf-8' )
	timetable.SortAllNode()

	printForm( timetable )
	
	print( '<ul>' )
	print( '<li><a href="../transport.html">Please Go Here for main site</a></li>' )
	print( '<li><a href="../ganglia/">System Info Monitored by Ganglia</a></li>' )
	print( '</ul>' )
	
	
	print( '</body>' )


if __name__ == '__main__':	
	print( 'Content-Type: text/html; charset=utf-8\n' )
	print( '<HTML lang="utf-8">')
	printHead()
	main()
	print( '</HTML>' )