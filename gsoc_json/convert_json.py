#! /usr/bin/python
import os, sys

json = sys.argv[1]

json = os.path.basename(json) 

json = open(json, 'r')

lines = json.readlines()

result = sys.argv[2]

result = open(result, 'w+') 

data = '[\n'

def setFwdBwd(lines, i):
	prev = lines[i-1]
	try:
		next = lines[i+1]
	except:
		next = ''	
	current = lines[i]
	return (prev, next, current)

for i in range(0, len(lines)):
	(prev, next, current) = setFwdBwd(lines, i)
	try:
		split = current.split(':',2)
		first_part = split[0]
		second_part = split[1]
	except:
		split = current
		first_part = current	
	if current.find('"id"') != -1 and current.find('P') != -1:
		data += prev
		data += current
		data += next
	i = i + 2
	(prev, next, current) = setFwdBwd(lines, i)				
	if current.find('"aliases"') != -1:
		data += current
		i = i+1
		(prev, next, current) = setFwdBwd(lines, i)		
		while 1:
			if current.find('"en": [') != -1:
				while current.find(']') == -1:
					data += current				
					i = i+1
					(prev, next, current) = setFwdBwd(lines, i)
			data += current		
			i = i + 1		
			(prev, next, current) = setFwdBwd(lines, i)		
			if current.find('"descriptions": {') != -1:
				data += current
				break;
	print data			
	while 1:			
		i = i + 1		
		(prev, next, current) = setFwdBwd(lines, i)		
		if current.find('"en": {') != -1:
			while current.find('}') != -1:
				data +=current
				i = i + 1		
				(prev, next, current) = setFwdBwd(lines, i)
		if current.find('"labels": {') != -1:
			data += current
		if current.find('"datatype"') != -1:
			data += current
			data += next
			break;
data += ']'		
print data		
	
