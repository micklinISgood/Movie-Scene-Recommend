import boto.sqs,boto.sns,json, inspect, threading, logging, time, requests
conn = boto.sqs.connect_to_region("us-east-1",profile_name='movie')
q=conn.get_queue('watch_interval')
for message in q.get_messages():
	body = json.loads(message.get_body())
	msg =json.loads(body["Message"])
	print body["Message"]