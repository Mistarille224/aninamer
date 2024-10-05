from flask import Flask, request, jsonify
import toml
from conf import data,modify_conf

app = Flask(__name__)


@app.route('/api/start', methods=['POST'])
def start_app():
    # 启动逻辑
    return '后端应用已启动', 200

@app.route('/api/stop', methods=['POST'])
def stop_app():
    # 关闭逻辑
    return '后端应用已关闭', 200

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'GET':
        return jsonify(data), 200
    elif request.method == 'POST':
        new_config = request.json
        modify_conf(new_config)
        return '配置已更新', 200

    app.run(debug=True)