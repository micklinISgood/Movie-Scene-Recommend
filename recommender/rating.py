import json, csv, thread
from collections import *
import boto.sqs,boto.sns,json, inspect, threading, logging, time, requests
from engine import RecommendationEngine
from pyspark import SparkContext, SparkConf

conn = boto.sqs.connect_to_region("us-east-1",profile_name='movie')
queue=conn.get_queue('watch_interval')

def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("movie_recommendation-server")
    # IMPORTANT: pass aditional Python modules to each worker
    sc = SparkContext(conf=conf, pyFiles=['engine.py'])
 
    return sc

recommendation_engine = RecommendationEngine(init_spark_context())    
# sns_conn = boto.sns.connect_to_region("us-west-2")

# sqs = boto3.resource('sqs')
# queue = sqs.get_queue_by_name(QueueName='watch_interval')
def Recommend(uid):
	intput_table =[]
	for k,v in rate_map[uid].items():
		intput_table.append((0,k,v))
	rec_list = recommendation_engine.recommends(intput_table)
	for row in rec_list:
		print row



movielen = {}
rate_map = defaultdict(lambda: defaultdict( lambda:0))

def worker():
    while True:
        for message in queue.get_messages(1):

		body = json.loads(message.get_body())
		msg =json.loads(body["Message"])
		if msg["event"] == "watch_interval":
			print msg["uid"], msg["watch_interval"],msg["mid"]
			intterval = msg["watch_interval"].split(":")
			diff = float(intterval[1])-float(intterval[0])
			rate_map[msg["uid"]][msg["mid"]]+= round(diff*3/movielen[msg["mid"]],2) 
		if msg["event"] == "click_video":
			print msg["uid"],msg["mid"] 
			rate_map[msg["uid"]][msg["mid"]]+=1
		try:

			print rate_map
			thread.start_new_thread(Recommend,(msg["uid"],))

		except Exception , errtxt:
			print errtxt
	

if __name__ == '__main__':
    movies = open('movie_len.csv', 'rb')
    spamreader = csv.reader(movies, delimiter=',')
    for row in spamreader:
    	movielen[row[-1]] = int(row[4])
    # print movielen



    worker()
