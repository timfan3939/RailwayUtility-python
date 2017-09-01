#!/usr/bin/env python3

from RUJson import *
from RUTimeTable import *
from datetime import time




def main():
	filename1 = 'file/20161106.json'
	filename2 = 'file/20170913.json'
	
	timetable1 = RUTimeTable()
	timetable2 = RUTimeTable()

	LoadStation( timetable1 )
	LoadStation( timetable2 )
	
	
	LoadTRAJsonTimetable( timetable1, filename1, encoding = 'utf8' )
	timetable1.SortAllNode()
	LoadTRAJsonTimetable( timetable2, filename2, encoding = 'utf8' )
	timetable2.SortAllNode()
	
	timetable1.all_train_list.sort()
	timetable2.all_train_list.sort()
	
	index1 = 0
	index2 = 0
	
	while True:
		if index1 >= len(timetable1.all_train_list):
			for i in range(index2, len(timetable2.all_train_list)):
				print('>>', timetable2.all_train_list[i].id)
			break
		elif index2 >= len(timetable2.all_train_list):
			for i in range(index1, len(timetable1.all_train_list)):
				print('<<', timetable1.all_train_list[i].id)
			break
		
		if timetable1.all_train_list[index1].id == timetable2.all_train_list[index2].id:
			index1 += 1
			index2 += 1
			continue
		elif timetable1.all_train_list[index1].id < timetable2.all_train_list[index2].id:
			print('<<', timetable1.all_train_list[index1].id)
			index1 += 1
			continue
		else:
			print('>>', timetable2.all_train_list[index2].id)
			index2 += 1
			continue
			
	


if __name__ == '__main__':
	main()