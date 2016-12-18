from flask import Flask, render_template,request
from flask_socketio import SocketIO,send,emit
import boto.sns,json,inspect
sns_conn = boto.sns.connect_to_region("us-east-1", profile_name='movie')
# print sns_conn.aws_access_key_id

app = Flask(__name__)
socketio = SocketIO(app)


online = {}
SidToUid = {}


def cleanUserByUid(uid):
    try :
        sid = online[uid]
        if uid in online: del online[uid]
        if sid in SidToUid: del SidToUid[sid]
    except Exception as e:
          print e 

def cleanUserBySid(sid):
    try : 
        uid = SidToUid[sid]
        if uid in online: del online[uid]
        if sid in SidToUid: del SidToUid[sid]
    except Exception as e:
          print e    

@socketio.on('connect')
def remote():
    print request.sid
    # print [name for name,thing in inspect.getmembers(request)]
    print 'remote connected ip: %s , %s'%(request.remote_addr,request.user_agent)

@socketio.on('disconnect')
def close():
    cleanUserBySid(request.sid)
    print 'remote close ip: %s'%request.remote_addr
    # print online
    
        # print online
        # for k,v in online.items():
            # send to specific user
            # emit('message',uid+" left",room=v)
        # print request.sid
 

@socketio.on('init')
def handle_my_custom_event(json_data):
    print('received json_data: ' + str(json_data))


@socketio.on('watch_interval')
def handle_my_custom_event(json_data):
    # print json_data["uid"]
    # print 'remote connected ip: %s'%request.remote_addr
    uid = json_data["uid"]
    if uid != "non-login" and uid not in online:
        online[uid] = request.sid
        SidToUid[request.sid] = uid

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
    uid = json_data["uid"]
    if uid != "non-login" and uid not in online:
        online[uid] = request.sid
        SidToUid[request.sid] =uid

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
    uid = json_data["uid"]
    if uid != "non-login" and uid not in online:
        online[uid] = request.sid
        SidToUid[request.sid] =uid

    json_data["remote_addr"] = request.remote_addr
    json_data["event"] = 'rec_list'
    print json.dumps(json_data)
    sns_conn.publish(
					topic="arn:aws:sns:us-east-1:612129620405:watch_interval",
					message=json.dumps(json_data)
	)

@socketio.on('recommendUser')
def handle_message(message):
    # print('received message: ' + message)
    data = json.loads(message)
    print data
    sendRecommendation(data["uid"], data["rec_list"])


def sendRecommendation(uid, rec_list):
    if uid in online:
        data = {}
        data["action"] = "rec"
        data["rec_list"] = rec_list
        try:
            emit('message',json.dumps(data),room=online[uid])
        except Exception as e:
            cleanUserByUid(uid)
            print e 

@socketio.on('recommendUserScene')
def handleScene_message(message):
    # print('received message: ' + message)
    data = json.loads(message)
    print data
    sendSceneRecommendation(data["uid"], data["rec_list"])


def sendSceneRecommendation(uid, rec_list):
    if uid in online:
        data = {}
        data["action"] = "recScene"
        data["rec_list"] = rec_list
        try:
            emit('message',json.dumps(data),room=online[uid])
        except Exception as e:
            cleanUserByUid(uid)
            print e


if __name__ == '__main__':

    #open external connections
    host = '0.0.0.0'
    port = 6888
    print "WebSocket engine listen @ %d"%port
    socketio.run(app, host=host,port=port)
