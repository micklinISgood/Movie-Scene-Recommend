import csv,sys
from collections import *


movies = open('movies.csv', 'rb')


mreader = csv.reader(movies, delimiter=',')



if len(sys.argv) !=2:
	print "verifier.py movie_name"
	sys.exit(1)
# print collect
genre_hash = defaultdict(lambda: [])

ret ={}
first = True
for row in mreader:
	if first :
		first = not first
		continue
	for x in row[2].split("|"):
			genre_hash[x].append(row[0])
	if sys.argv[1].lower() in row[1].lower():

		print row

out = open('genre.csv', 'wb') 
spamwriter = csv.writer(out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
for k, v in genre_hash.items():
	spamwriter.writerow([k, v])
movies.close()	

