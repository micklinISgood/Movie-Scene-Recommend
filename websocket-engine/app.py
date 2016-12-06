from flask import Flask, render_template,request
from flask_socketio import SocketIO
import boto.sns
sns_conn = boto.sns.connect_to_region("us-east-1", profile_name='movie')
# print sns_conn.aws_access_key_id

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def remote():
	print 'remote connected ip: %s'%request.remote_addr

@socketio.on('init')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


@socketio.on('watch_interval')
def handle_my_custom_event(json):
    # print json["uid"]
    # print 'remote connected ip: %s'%request.remote_addr
    json["remote_addr"] = request.remote_addr
    json["event"] = 'watch_interval'
    print json
    sns_conn.publish(
					topic="arn:aws:sns:us-east-1:612129620405:watch_interval",
					message=json
	)
    # print('received watch: ' + str(json))

@socketio.on('click_video')
def click_video(json):
    # print json["uid"]
    # print 'remote connected ip: %s'%request.remote_addr
    json["remote_addr"] = request.remote_addr
    json["event"] = 'click_video'
    print json
    sns_conn.publish(
					topic="arn:aws:sns:us-east-1:612129620405:watch_interval",
					message=json
	)

@socketio.on('rec_list')
def rec_list(json):
    # print json["uid"]
    # print 'remote connected ip: %s'%request.remote_addr
    json["remote_addr"] = request.remote_addr
    json["event"] = 'rec_list'
    print json
    sns_conn.publish(
					topic="arn:aws:sns:us-east-1:612129620405:watch_interval",
					message=json
	)
	
if __name__ == '__main__':


    socketio.run(app, port=6888)