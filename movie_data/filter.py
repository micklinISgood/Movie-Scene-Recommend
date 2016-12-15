import csv
from path import path


header = open('vc.csv', 'rb')
movies = open('movies.csv', 'rb')

spamreader = csv.reader(header, delimiter=',')
mreader = csv.reader(movies, delimiter=',')

collect ={} 
for row in spamreader:
		collect[row[2]] = row

# print collect
out = open('joined.csv', 'wb') 
spamwriter = csv.writer(out, delimiter=',', quoting=csv.QUOTE_MINIMAL)


ret ={}
for row in mreader:
	# if "up (2009)" in row[1].lower():
	# 	print row
	for s in collect.keys():
		if s.lower() == row[1].lower():
			# print row
			collect[s].append(row[0])
			spamwriter.writerow(collect[s])
			ret[s] = row
			break

	# print row
ret = sorted(ret.items(),key= lambda x:x[0])
# collect = sorted(collect)

print "Matched movies: %d, csv file path: %s"%(len(ret), path('joined.csv').abspath())
print "Unmatched movies:"
for k,v in collect.items():
	if len(v) != 7:
		print k

out.close()
movies.close()	
header.close()
