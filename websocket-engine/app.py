from flask import Flask, render_template,request
from flask_socketio import SocketIO
import boto.sns,json
sns_conn = boto.sns.connect_to_region("us-east-1", profile_name='movie')
# print sns_conn.aws_access_key_id

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def remote():
	print 'remote connected ip: %s'%request.remote_addr

@socketio.on('init')
def handle_my_custom_event(json_data):
    print('received json_data: ' + str(json_data))


@socketio.on('watch_interval')
def handle_my_custom_event(json_data):
    # print json_data["uid"]
    # print 'remote connected ip: %s'%request.remote_addr
    json_data["remote_addr"] = request.remote_addr
    json_data["event"] = 'watch_interval'
    print json.dumps(json_data)
    sns_conn.publish(
					topic="arn:aws:sns:us-east-1:612129620405:watch_interval",
					message=json.dumps(json_data)
	)
    # print('received watch: ' + str(json_data))

@socketio.on('click_video')
def click_video(json_data):
    # print json_data["uid"]
    # print 'remote connected ip: %s'%request.remote_addr
    json_data["remote_addr"] = request.remote_addr
    json_data["event"] = 'click_video'
    print json.dumps(json_data)
    sns_conn.publish(
					topic="arn:aws:sns:us-east-1:612129620405:watch_interval",
					message=json.dumps(json_data)
	)

@socketio.on('rec_list')
def rec_list(json_data):
    # print json_data["uid"]
    # print 'remote connected ip: %s'%request.remote_addr
    json_data["remote_addr"] = request.remote_addr
    json_data["event"] = 'rec_list'
    print json.dumps(json_data)
    sns_conn.publish(
					topic="arn:aws:sns:us-east-1:612129620405:watch_interval",
					message=json.dumps(json_data)
	)
	
if __name__ == '__main__':

    #open external connections
    host = '0.0.0.0'
    socketio.run(app, host=host,port=6888)
