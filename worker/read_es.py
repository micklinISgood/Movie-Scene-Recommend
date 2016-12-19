from pyes import *
import ast
import json
# from pyspark import SparkContext, SparkConf

# conf = SparkConf().setAppName("test").setMaster("local")

# sc = SparkContext(conf=conf)

conn = ES('https://search-test-qmyiuzwgkz4c6jmlzhhy6p2t7y.us-east-1.es.amazonaws.com/')

def find_time_data(time_data):
	
	rec = []

	results=conn.search(MatchAllQuery())

	for result in results:
		result = json.dumps(result)
		result = ast.literal_eval(result)

		if int(result["epoch"]) < time_data - 24*60*60*1000:
			rec.append(result)
	return rec
	
def find_by_keyword(keyword):

	rec = []
	q = QueryStringQuery(keyword)

	results=conn.search(query = q)

	for result in results:
		result = json.dumps(result)
		result = ast.literal_eval(result)
		rec.append(result)
	return rec


if __name__ == '__main__':

	results=conn.search(MatchAllQuery())

	for result in results:
		result = json.dumps(result)
		result = ast.literal_eval(result)
		print result


		