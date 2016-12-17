import json, csv, thread
from collections import *
import boto.sqs,boto.sns,json, inspect, threading, logging, time, requests
conn = boto.sqs.connect_to_region("us-east-1")
print conn.get_all_queues()
queue= conn.get_queue('Watch_interval')
print queue
# sns_conn = boto.sns.connect_to_region("us-west-2")

# sqs = boto3.resource('sqs')
# queue = sqs.get_queue_by_name(QueueName='watch_interval')
def Recommend(mystring):
    print mystring

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
			thread.start_new_thread(Recommend,('MyStringHere',))

		except Exception , errtxt:
			print errtxt
	

if __name__ == '__main__':
    movies = open('movie_len.csv', 'rb')
    spamreader = csv.reader(movies, delimiter=',')
    for row in spamreader:
    	movielen[row[-1]] = int(row[4])
    # print movielen



    worker()
