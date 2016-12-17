
from socketIO_client import SocketIO
import time,json

def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_aaa_response(*args):
    print('on_aaa_response', args)

socketIO = SocketIO('http://54.221.40.5', 6888)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

while 1:

	data ={}
	data["uid"]="cl3469@gmail.com"
	data["rec_list"] = ["haha","hello"]
	socketIO.emit('message',json.dumps(data))
	time.sleep(20)
