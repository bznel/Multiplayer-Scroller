import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print(f"Player {sid} connected")
    sio.emit('player_joined', sid, skip_sid=sid)
    sio.emit('your_id', sid, room=sid)  

@sio.event
def disconnect(sid):
    print(f"Player {sid} disconnected")
    sio.emit('player_left', sid, skip_sid=sid)

@sio.on('update_player')
def update_player(sid, data):
    
    sio.emit('player_data', {'pos': data['pos'], 'anim': data['anim'], 'facing': data['facing'], 'sid': sid}, skip_sid=sid) 


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 80)), app)
