import json, csv, thread
from collections import *
import boto3, json, inspect, threading, logging, time, requests
import ast
from pyes import *
from dateutil import parser
from HTMLParser import HTMLParser
# conn = boto.sqs.connect_to_region("us-east-1")
# print conn.get_all_queues()
# queue= conn.get_queue('Watch_interval')
# print queue
# sns_conn = boto.sns.connect_to_region("us-west-2")

# sqs = boto3.resource('sqs')
# queue = sqs.get_queue_by_name(QueueName='watch_interval')
import time

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='watch_interval')

conn = ES('https://search-test-qmyiuzwgkz4c6jmlzhhy6p2t7y.us-east-1.es.amazonaws.com/')

def Recommend(mystring):

    print mystring

def worker(rate_map, movielen):

	while True:

		for message in queue.receive_messages(MaxNumberOfMessages = 10, WaitTimeSeconds=1):

			body = json.loads(message.body)
			msg =json.loads(body["Message"])
			#print msg

			

			if msg["uid"] not in rate_map:
				search_es(rate_map, movielen, msg["uid"], msg["epoch"])

			# if msg["uid"] == "3333" and "mid" not in msg:
			# 	print "found"
				

			if "mid" not in msg:
				continue
			if msg["mid"] not in movielen:
				continue

			if msg["event"] == "watch_interval":

				#print msg["uid"], msg["watch_interval"],msg["mid"]
				intterval = msg["watch_interval"].split(":")
				diff = float(intterval[1])-float(intterval[0])

				if msg["uid"] not in rate_map:
					rate_map[msg["uid"]][msg["mid"]] = round(diff*3/movielen[msg["mid"]],2) 
				else:
					rate_map[msg["uid"]][msg["mid"]]+= round(diff*3/movielen[msg["mid"]],2) 

			if msg["event"] == "click_video":
				#print msg
				
				if msg["uid"] not in rate_map:

					rate_map[msg["uid"]][msg["mid"]] = 1

				else:
					rate_map[msg["uid"]][msg["mid"]] += 1


			# try:

			# 	#print rate_map
			# 	thread.start_new_thread(Recommend,('MyStringHere',))

			# except Exception , errtxt:
			# 	print errtxt
		print rate_map
		time.sleep(2)

def search_es(rate_map, movielen, uid, time_data):

	#print type(uid)
	rec = []

	q = QueryStringQuery(uid)

	#if "uid" == ""
	results=conn.search(query = q)


	#results=conn.search(MatchAllQuery())
	try:

		for result in results:
			#print result, "result"
			result = json.dumps(result)
			result = ast.literal_eval(result)


			#print result

			if "uid" not in result or result["uid"] != uid:
				continue


			# if int(result["epoch"]) < time_data - 24*60*60*1000:
			if int(result["epoch"]) < int(time_data):

				if result["event"] == "watch_interval":
					if result["mid"] not in movielen:
						continue
					#print msg["uid"], msg["watch_interval"],msg["mid"]

					intterval = result["watch_interval"].split(":")
					diff = float(intterval[1])-float(intterval[0])
					rate_map[result["uid"]][result["mid"]]+= round(diff*3/movielen[result["mid"]],2) 

				if result["event"] == "click_video":
					#print msg
					rate_map[result["uid"]][result["mid"]]+=1
			
	except:

		print "skip"
		print uid



if __name__ == '__main__':
	movielen = {}
	rate_map = defaultdict(lambda: defaultdict( lambda:0))
	movies = open('movie_len.csv', 'rb')
	spamreader = csv.reader(movies, delimiter=',')
	for row in spamreader:
		movielen[row[-1]] = int(row[4])

	
	
	worker(rate_map, movielen)
