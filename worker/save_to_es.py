import json
import boto3
from pyes import *
from dateutil import parser
from HTMLParser import HTMLParser
import ast

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='watch_interval')

conn = ES('https://search-test-qmyiuzwgkz4c6jmlzhhy6p2t7y.us-east-1.es.amazonaws.com/')

event_list = ["watch_interval", "rec_list", "click_video"]

def worker():
    while True:
        for message in queue.receive_messages(MaxNumberOfMessages = 10, WaitTimeSeconds=20):

            movie = json.loads(message.body)
            #response = alchemyapi.sentiment('text', tweet['text'])
            #print movie
            temp = movie["Message"]
            temp = ast.literal_eval(temp)
            print(type(temp))

            if temp["event"] == "watch_interval":
                conn.index({'event':temp["event"] ,'watch_interval':temp["watch_interval"],'uid':temp["uid"],
                    'remote_addr': temp["remote_addr"], 'mid': temp["mid"], 'epoch': temp["epoch"]},'watch_interval', 'test-type')

            if temp["event"] == "rec_list":
                conn.index({'event':temp["event"] ,'rec_list':temp["rec_list"],'uid':temp["uid"],
                    'remote_addr': temp["remote_addr"], 'epoch': temp["epoch"]},"rec_list", 'test-type')
            if temp["event"] == "click_video":
                conn.index({'event':temp["event"],'uid':temp["uid"],
                    'remote_addr': temp["remote_addr"], 'mid': temp["mid"], 'epoch': temp["epoch"]},"click_video", 'test-type')

            #     if response['status'] == 'OK':
            #         tweet['sentiment'] = response['docSentiment']['type']
            #         encoded = json.dumps(tweet, ensure_ascii=False)
            #         # Push to Amazon SNS
            #         topic.publish(Message=encoded)
            message.delete()
            #conn.index({'message_id':movie['MessageId'] ,'message':movie['Message'],'time':movie['Timestamp']},'movie_interval', 'test-type')
if __name__ == '__main__':
    worker()

