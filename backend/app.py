from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
from conf import CONFIG_PATH,ensure_config_exists
from tree import TREE_PATH,tree

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

def read_json(j):
    with open(j, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def push_data(to=None):    
    emit('update_conf', read_json(CONFIG_PATH), to=to)
    emit('update_tree', read_json(TREE_PATH), to=to)


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    push_data()

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('change_data')
def handle_send_data(path, new):
    tree_data = read_json(TREE_PATH)
    exec(f"tree_data{path} = new")
    with open(TREE_PATH, 'w', encoding='utf-8') as file:
        json.dump(tree_data, file, ensure_ascii=False, indent=4)
    push_data()

@socketio.on('change_conf')
def handle_send_data(new):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
        json.dump(new, file, ensure_ascii=False, indent=4)
    push_data()

if __name__ == '__main__':
    ensure_config_exists()
    tree()
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)