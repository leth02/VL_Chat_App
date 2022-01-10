from message_app import create_app
from message_app.send_message import socketio

if __name__ == "__main__":
    socketio.run(create_app())