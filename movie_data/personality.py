import csv,sys
from collections import *


rate = open('/Users/micklin/Documents/ml-20m/ratings.csv', 'rb')
movies = open('movies.csv', 'rb')

mreader = csv.reader(movies, delimiter=',')
genre_hash = defaultdict(lambda: [])
for row in mreader:
	genre_hash[row[0]]=row[2].split("|")


rreader = csv.reader(rate, delimiter=',')

i=0
user_personality = defaultdict(lambda: defaultdict( lambda:0))
rate_count = defaultdict(lambda: 0)
for row in rreader:
	if i ==0:
		i+=1 
		continue
	rate_count[row[0]]+=1
	if float(row[2]) >= 4.0:
		# print genre_hash[row[1]]
		s = set()
		for gen in genre_hash[row[1]]:
			user_personality[row[0]][gen]+=1 
			s.add(gen)
		# if row[0] not in user_personality:
		# 	user_personality[row[0]] = s
		# else:
		# 	# print user_personality[row[0]]
		# 	user_personality[row[0]] = user_personality[row[0]].union(s)
		# print row 
		i+=1

	# if i==1000: break

filter_personality =defaultdict(lambda: set())
for uid, gen_list in user_personality.items():
	i=0
	s= set()
	for gen, count in sorted(gen_list.items(), key= lambda x: -x[1]):
		# print uid ,gen, count
		if count >3 and i <7:
			s.add(gen)
			i+=1
	filter_personality[uid] |= s
# print rate_count
# print filter_personality
total_personality = defaultdict(lambda: [])
for k, v in  filter_personality.items():
	if rate_count[k] >5:
		sortl = sorted(list(v))
		total_personality["|".join(sortl)].append(k)

# print  total_personality
out = open('personality.csv', 'wb') 
spamwriter = csv.writer(out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
for k, v in total_personality.items():
	spamwriter.writerow([k, "|".join(v)])
rate.close()
movies.close()