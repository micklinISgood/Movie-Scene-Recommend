import csv,sys,heapq
from collections import *

user_p = open('personality.csv', 'rb')
person_reader = csv.reader(user_p, delimiter=',')
h =[]
for row in person_reader:

	if len(row[0]) ==0: continue

	if len(h) < 20:
		heapq.heappush(h, (len(row[1].split("|")),row[0]))
	else:

		heapq.heappushpop(h,  (len(row[1].split("|")),row[0]))


for row in sorted(h, key= lambda x: -x[0]):
	print "personality: %s \npopulation: %d\n"%(row[1],row[0])
user_p.close()