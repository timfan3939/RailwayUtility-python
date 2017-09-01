#!/usr/bin/env python3

from RUJson import *
from RUTimeTable import *
from datetime import time

#	         1234A 次  --  1234A 次  --  1234A 次 	
# 	
#	         1234A 次  --  車站名稱  --  1234A 次   
#  車站名稱  xx:xx:xx  --  xx:xx:xx  --  xx:xx:xx
#                到達          到達          到達
#
#	            ||            ||            ||   
#
#	         車站名稱  --  1234A 次  --  車站名稱   
#  車站名稱  xx:xx:xx  --  xx:xx:xx  --  xx:xx:xx
#                到達          到達          到達
#
#	            ||            ||            ||   
#
#	         1234A 次  --  車站名稱  --  1234A 次   
#  車站名稱  xx:xx:xx  --  xx:xx:xx  --  xx:xx:xx
#                到達          到達          到達
#
#
# type = 1 ： 王
# type = 2 ： 卅
	
def printNodes(TTNodes, size, type = 1):
		mid = int(size/2)
		
		# print train no header
		output = ' ' * 8
		if type == 1:
			output += '          ' * size
		else:
			for i in range(size):
				output += '  {:>5} 次'.format(TTNodes[mid*size + i].train.id)
		
		print(output)
		
		# for each row, print information
		for i in range(size):
		
			if i == 0:
				print()
			elif type == 1:
				output = ' ' * 8
				for j in range(size):
					if j == int(size/2) :
						output += '      |   '	
					else:
						output += '          '	
				print(output)
			else:
				output = ' ' * 8
				for j in range(size):
					output += '      |   '				
				print(output)
		
		
			output = ' ' * 8
			if type == 1:
				for j in range(size):
					output += '  {:>5} 次'.format(TTNodes[i*size+j].train.id)
			else:
				for j in range(size):
					if len(TTNodes[i*size+j].station.name) == 1:
						output += '  {:>7}'.format(TTNodes[i*size+j].station.name)
					elif len(TTNodes[i*size+j].station.name) == 2:
						output += '  {:>6}'.format(TTNodes[i*size+j].station.name)
					elif len(TTNodes[i*size+j].station.name) == 3:
						output += '  {:>5}'.format(TTNodes[i*size+j].station.name)
					elif len(TTNodes[i*size+j].station.name) == 4:
						output += '  {:>4}'.format(TTNodes[i*size+j].station.name)
					else:
						output += '  {}'.format(TTNodes[i*size+j].station.name)
			print(output)
			
			
			if type == 1:
				if len(TTNodes[i*size+mid].station.name) == 1:
					output =  '{:>7}'.format(TTNodes[i*size+mid].station.name)
				elif len(TTNodes[i*size+mid].station.name) == 2:
					output =  '{:>6}'.format(TTNodes[i*size+mid].station.name)
				elif len(TTNodes[i*size+mid].station.name) == 3:
					output =  '{:>5}'.format(TTNodes[i*size+mid].station.name)
				elif len(TTNodes[i*size+mid].station.name) == 4:
					output =  '{:>4}'.format(TTNodes[i*size+mid].station.name)
				else :
					output =  '{}'.format(TTNodes[i*size+mid].station.name)
			else:
				output = ' ' * 8
					
			for j in range(size):
				if (i == int(size/2) or type == 1) and j != 0:
					output += '--{:>8s}'.format(TTNodes[i*size+j].time_stamp.__str__())			
				else:
					output += '  {:>8s}'.format(TTNodes[i*size+j].time_stamp.__str__())			
			print(output)
			
			output = ' ' * 8
			for j in range(size):
				if TTNodes[i*size+j].node_type == RUTTNodeType.RUTTArrival:
					output += '      抵達'
				elif TTNodes[i*size+j].node_type == RUTTNodeType.RUTTDeparture:
					output += '      開車'
				else:
					output += ' unknowned'
			print(output)
			
emptyNode = RUTTNode( RUTTStationNode('        ', '        '), RUTTTrainNode('    '), time(), RUTTNodeType.RUTTUnknown)
			
def refreshWithNode(ttnode, size, type = 1):

	result = [emptyNode] * (size*size)	
	mid = int(size/2)	
	result[mid * size + mid] = ttnode
	
	if type == 1:
		schedules = ttnode.train.schedules
		seq = schedules.index(ttnode)
		
		for i in range(-mid, mid+1):
			if i == 0 or seq + i < 0 or seq + i >= len(schedules):
				continue
			result[ (mid + i) * size + mid ] = schedules[seq + i]
					
		for i in range(-mid, mid+1):
			t_node = result[ (mid + i) * size + mid ]
			if t_node is emptyNode:
				continue
				
			t_schedules = t_node.station.schedules
			t_seq = t_schedules.index(t_node)
						
			for j in range(-mid, mid+1):
				if j == 0 or t_seq + j < 0 or t_seq + j >= len(t_schedules):
					continue
				result[ (mid + i) * size + (mid + j) ] = t_schedules[ t_seq + j ]
	else:
		schedules = ttnode.station.schedules
		seq = schedules.index(ttnode)
		
		for j in range(-mid, mid+1):
			if j == 0 or seq + j < 0 or seq + j >= len(schedules):
				continue
			result[ (mid + j) + size * mid ] = schedules[seq + j]
		
		for j in range(-mid, mid+1):
			t_node = result[ (mid + j) + size * mid ]
			if t_node is emptyNode:
				continue		
		
			t_schedules = t_node.train.schedules
			t_seq = t_schedules.index(t_node)	
						
			for i in range(-mid, mid+1):
				if i == 0 or t_seq + i < 0 or t_seq + i >= len(t_schedules):
					continue
				result[ (mid + i) * size + (mid + j) ] = t_schedules[ t_seq + i ]
	
	printNodes(result, size, type)
	
	
####################
# Test Function
####################
# Create a viewer with Timetable
# Read Station
# Read Time Table
# Show interactive view of RUTimeTable


def main():
	timetable = RUTimeTable()
	
	LoadStation( timetable )
	LoadTRAJsonTimetable( timetable, 'file/20170913.json', encoding = 'utf8' )
	timetable.SortAllNode()
	
	testSize = 5
	train = None
	for t in timetable.all_train_list:
		if len(t.schedules) > testSize * testSize:
			train = t
			break
	
	if train is None:
		return
	
	currentNode = train.schedules[5]
	type = 1
	
	while True:
		refreshWithNode(currentNode, testSize, type)
		line = input( '\n\nw a s d for moving, q for leaving, f for flipping: ')
		if line != '':
			c = line[0]
		else:
			c = 'p'
		
		if c == 'w':
			schedule = currentNode.train.schedules
			seq = schedule.index(currentNode) - 1			
			if seq >= 0:
				currentNode = schedule[seq]
		elif c == 'a':
			schedule = currentNode.station.schedules
			seq = schedule.index(currentNode) - 1			
			if seq >= 0:
				currentNode = schedule[seq]
			pass
		elif c == 's':
			schedule = currentNode.train.schedules
			seq = schedule.index(currentNode) + 1			
			if seq < len(schedule):
				currentNode = schedule[seq]
			pass
		elif c == 'd':
			schedule = currentNode.station.schedules
			seq = schedule.index(currentNode) + 1			
			if seq < len(schedule):
				currentNode = schedule[seq]
			pass
		elif c == 'q':
			break
		elif c == 'f':
			type = 2 if type == 1 else 1
		else:
			pass
			
	
if __name__ == '__main__':
	main()