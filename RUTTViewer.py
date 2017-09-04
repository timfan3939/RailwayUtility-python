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
# viewerType = 1 ： 王
# viewerType = 2 ： 卅
	
def printNodes(TTNodes, size, viewerType = 1):
		mid = int(size/2)
		
		# print train no header
		output = ' ' * 8
		if viewerType == 1:
			output += '          ' * size
		else:
			for i in range(size):
				output += '  {:>5} 次'.format(TTNodes[mid*size + i].train.id)
		
		print(output)
		
		# for each row, print information
		for i in range(size):
		
			if i == 0:
				print()
			elif viewerType == 1:
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
			if viewerType == 1:
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
			
			
			if viewerType == 1:
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
				if (i == int(size/2) or viewerType == 1) and j != 0:
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
			
def refreshWithNode(ttnode, size, viewerType = 1, directionType = 1):

	result = [emptyNode] * (size*size)	
	mid = int(size/2)	
	result[mid * size + mid] = ttnode
	
	if viewerType == 1:
		schedules = ttnode.train.schedules
		seq = schedules.index(ttnode)
		
		# center toward top
		offset = 0
		step = 1
		while step <= mid:
			offset -= 1
			if seq + offset < 0:
				break
			result[ (mid-step) * size + mid ] = schedules[seq + offset]
			step += 1
		
		# center toward bottom
		offset = 0
		step = 1
		while step <= mid:
			offset += 1
			if seq + offset >= len(schedules):
				break
			result[ (mid+step) * size + mid ] = schedules[seq + offset]
			step += 1
		
		# Horizontal nodes expansion
		for i in range(-mid, mid+1):
			print('i =', i)
			c_node = result[ (mid+i) * size + mid ]
			if c_node is emptyNode:
				continue
				
			t_schedules = c_node.station.schedules
			t_seq = t_schedules.index(c_node)
			
			# Left Horizontal node expansion
			offset = 0
			step = 1
			while step <= mid:
				offset -= 1
				if t_seq + offset < 0:
					break
				print('({},{}), offset = {}'.format(mid+i, mid-step, offset))
				print(c_node.train.id, t_schedules[t_seq + offset].train.id)
				if directionType == 2 and c_node.train.direction != t_schedules[t_seq + offset].train.direction:
					print(c_node.train.id, '!=' , t_schedules[t_seq + offset].train.id)
					continue
				result[ (mid+i) * size + (mid - step) ] = t_schedules[t_seq + offset]
				step += 1
			
			offset = 0
			step = 1
			while step <= mid:
				offset += 1
				if t_seq + offset >= len(t_schedules):
					break
				print('({},{}), offset = {}'.format(mid+i, mid+step, offset))
				print(c_node.train.id, t_schedules[t_seq + offset].train.id)
				if directionType == 2 and c_node.train.direction != t_schedules[t_seq + offset].train.direction:
					print(c_node.train.id, '!=' , t_schedules[t_seq + offset].train.id)
					continue
				result[ (mid+i) * size + (mid + step) ] = t_schedules[t_seq + offset]
				step += 1		
		
	else:
		schedules = ttnode.station.schedules
		seq = schedules.index(ttnode)
		
		
		# Center toward left
		offset = 0
		step = 1
		while step <= mid:
			offset -= 1
			if seq + offset < 0:
				break
			if directionType == 2 and ttnode.train.direction != schedules[seq + offset].train.direction:
				continue
			result[ (mid - step) + size * mid] = schedules[seq + offset]
			print('( {}, {} )'.format(mid-step, mid))
			step +=1 
		
		# Center toward right
		offset = 0
		step = 1
		while step <= mid:
			offset += 1
			if seq + offset >= len(schedules):
				break
			if directionType == 2 and ttnode.train.direction != schedules[seq + offset].train.direction:
				continue
			result[ (mid + step) + size * mid] = schedules[seq + offset]
			print('( {}, {} )'.format(mid+step, mid))
			step += 1
		
	
	
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
	
	printNodes(result, size, viewerType)
	
	
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
	viewerType = 1
	
	# 1 = don't caire
	# 2 = same as currentNode
	directionType = 1
	
	while True:
		refreshWithNode(currentNode, testSize, viewerType, directionType)
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
			viewerType = 2 if viewerType == 1 else 1
		elif c == 'x':
			directionType = 2 if directionType == 1 else 1
		else:
			pass
			
	
if __name__ == '__main__':
	main()