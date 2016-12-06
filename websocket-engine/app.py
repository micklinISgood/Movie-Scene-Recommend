from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# print app.config
# app.config['PORT'] = 6888
# app.port = 6888
socketio = SocketIO(app)

@socketio.on('init')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


@socketio.on('watch_interval')
def handle_my_custom_event(json):
    print json["uid"]
    print('received watch: ' + str(json))

if __name__ == '__main__':


    socketio.run(app, port=6888)