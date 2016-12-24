from __future__ import print_function
from watson_developer_cloud import AlchemyLanguageV1
from alchemyapi import AlchemyAPI
import json
import csv
import os

print('############################################')
print('#   Keyword Extraction Example             #')
print('############################################')
'''
the filename
'''
current_file_path = __file__
upper_dir = os.path.dirname(os.getcwd())

data_dir = os.path.join(upper_dir, 'data')
filename = os.path.join(data_dir, 'Allmovie_2.csv.csv')

alchemy_language = AlchemyLanguageV1(api_key= '7a454d32972b85fd2599536ba9063e4d1530014b')
alchemyapi = AlchemyAPI()
f = open(filename,'rb')
reader = csv.DictReader(f)
result = open('result_of_alchemyapi_overview_to_keywords.csv','w')
fieldnames = ['movie overview', 'movie keywords']
writer = csv.DictWriter(result, fieldnames = fieldnames)
writer.writeheader()
counter = 0
for line in reader:
	counter = counter +1
	if counter >= 2501:
		response = alchemyapi.combined('text', line['overview'])
		if response['status'] == 'OK':
			keywords = []
			for keyword in response['keywords']:
				if float(keyword['relevance']) > 0.5:
					keywords.append(keyword['text'].encode('utf-8'))
					print(keyword['text'], ' : ', keyword['relevance'])
			writer.writerow({'movie overview': line['overview'], 'movie keywords': keywords})
				
f.close()
data.close()

