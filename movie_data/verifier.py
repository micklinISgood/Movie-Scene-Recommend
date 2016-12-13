import csv,sys


movies = open('movies.csv', 'rb')


mreader = csv.reader(movies, delimiter=',')



if len(sys.argv) !=2:
	print "verifier.py movie_name"
	sys.exit(1)
# print collect

ret ={}
for row in mreader:
	if sys.argv[1].lower() in row[1].lower():
		print row

movies.close()	

