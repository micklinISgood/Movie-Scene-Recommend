import csv

header = open('vc.csv', 'rb')
movies = open('movies.csv', 'rb')

spamreader = csv.reader(header, delimiter=',')
mreader = csv.reader(movies, delimiter=',')

collect = [row[1] for row in spamreader]

# print collect

ret ={}
for row in mreader:
	# if "up (2009)" in row[1].lower():
	# 	print row
	for s in collect:
		if s.lower() == row[1].lower():
			# print row
			ret[s]=(row)
			break

	# print row
ret = sorted(ret.items(),key= lambda x:x[0])
collect = sorted(collect)

for k in ret:
	print k
print len(ret)

movies.close()	
header.close()
