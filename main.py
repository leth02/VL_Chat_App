from message_app import create_app
from message_app.send_message import socketio
from message_app.config import SERVER_ENV

if __name__ == "__main__":
    # Because we use socketio, we will not use `flask run` to initialize the app
    # Instead, we use `python main.py`
    # We pass the app instance to socketio instance, and call the custom `run()` method of socketio.
    # This function will call `app.run()` (equivalent to using `flask run`) on behalf of developer.
    # With that being said, the run Flask app will not have the debug setting set like when we use `flask run`.
    # The fix is to explicitly pass the debug option(s) we need
    # References:
    #   https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent
    #   https://github.com/miguelgrinberg/Flask-SocketIO/blog/main/src/flask_socketio/__init__.py#516
    if SERVER_ENV == "DEBUG":
        socketio.run(create_app(), debug=True, use_reloader=True)
    else:
        socketio.run(create_app())
