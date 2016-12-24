import json
from watson_developer_cloud import NaturalLanguageClassifierV1
from credential import *
from collections import defaultdict
import os
import random
import sys
import csv

import keyword_to_theme as run

upper_dir = os.path.dirname(os.getcwd())

data_dir = os.path.join(upper_dir, 'data')
filename = os.path.join(data_dir, 'Allmovie_Title_theme.csv')
 
natural_language_classifier = NaturalLanguageClassifierV1(
  username = username,
  password = password)

# New model
#classifier_id = "ff1c34x160-nlc-444"

# Old model
classifier_id = "ff189ax155-nlc-305"



def predict(keyword):
	classes = natural_language_classifier.classify(classifier_id, keyword)
	return classes

def load_data():
    """
    This method reads the dataset, and returns a list of rows.
    Each row is a list containing the values in each column.
    """    
    with open(filename, 'rb') as f:
        f.seek(0)
        reader = csv.reader(f)
        return [l for l in reader]

def get_movie(themes):
	print themes
	data = load_data()
	ThemeCollect = dict()
	ThemeTitle = defaultdict(list)
	for row in data:
	    for i in xrange(1,len(row)):
	        if row[i] == "":
	            break
	        ThemeCollect[row[i].strip()] = ThemeCollect.get(row[i].strip(), 0) + 1
	        ThemeTitle[row[i].strip()].append(row[0])

	#remove empty list
	if '""' in ThemeCollect:
	    del ThemeCollect['""']
	if '""' in ThemeTitle:
	    del ThemeTitle['""']	    
	#remove themes with only one or two movie
	for key, value in ThemeCollect.items():
	    if value < 3:
	        del ThemeCollect[key]
	        del ThemeTitle[key]
	
	list_1 = ThemeTitle[themes[0]]
	list_2 = ThemeTitle[themes[1]]
	list_3 = ThemeTitle[themes[2]]

	threeIntersect = set(list_1).intersection(list_2).intersection(list_3)
	twoIntersect = set(list_1).intersection(list_2).intersection(list_3)

	# recommend 3 movie if intersection > 3
	if len(threeIntersect) != 0: return list(threeIntersect)

	# recommend from first selected theme if intersection = 0
	elif len(twoIntersect) != 0: return list(twoIntersect)

	elif len(list_1) > 3: return random.sample(set(list_1), 3)

	else: return list_1

def get_movie_user(themes):
	print themes[0]
	data = load_data()
	ThemeCollect = dict()
	ThemeTitle = defaultdict(list)
	for row in data:
	    for i in xrange(1,len(row)):
	        if row[i] == "":
	            break
	        ThemeCollect[row[i].strip().replace('"',"").lower()] = ThemeCollect.get(row[i].strip().replace('"',"").lower(), 0) + 1
	        ThemeTitle[row[i].strip().replace('"',"").lower()].append(row[0])

	#remove empty list
	if '""' in ThemeCollect:
	    del ThemeCollect['""']
	if '""' in ThemeTitle:
	    del ThemeTitle['""']	    
	#remove themes with only one or two movie
	for key, value in ThemeCollect.items():
	    if value < 3:
	        del ThemeCollect[key]
	        del ThemeTitle[key]
	
	result = defaultdict(list)
	for i in xrange(len(themes)):
		theme = themes[i]
		result[themes[i]].append(ThemeTitle[theme])
	return result


##--- From Keyword to theme ---###
def get_theme(keywords):
	# result = predict(raw_input("Enter Keyword: "))
	result = predict(keywords)
	theme_class =  result['classes']

	recommendTheme =[]
	for i in xrange(3):
		# print "Theme: {0}. Confidence: {1}".format(theme_class[i]['class_name'], theme_class[i]['confidence'])
		recommendTheme.append(theme_class[i]['class_name'])

	##--- From Theme to movie ---##
	recommendMovie = get_movie(recommendTheme)
	# print "\nRecommended movies: "
	# for r in recommendMovie:
	# 	print r
	return recommendTheme, recommendMovie

if __name__ == "__main__":
	result = get_theme(raw_input("Clicked Movie Keyword: "))

