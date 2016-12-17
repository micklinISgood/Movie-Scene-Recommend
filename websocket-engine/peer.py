
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

socketIO = SocketIO('localhost', 6888)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)

while 1:

	data ={}
	data["uid"]="cl3469@gmail.com"
	data["rec_list"] = [("Quadrille (1938)","Comedy|Romance"),("Tall Man, The (2012)","Crime|Drama|Mystery]")]
	print json.dumps(data)
	socketIO.emit('recommendUser',json.dumps(data))

	time.sleep(2)

