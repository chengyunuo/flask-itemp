
import psutil
import time
from threading import Lock
from flask import Flask, render_template, session, request, url_for
from flask_socketio import SocketIO, emit
from serial_control1 import SerialControl
from utils import log
from utils import temp_parse


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
ser = SerialControl()


thread = None
thread_lock = Lock()


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    """Example of how to send server generated events to clients."""
    global ser

    while True:
        # 延时0.3秒
        socketio.sleep(0.3)
        # 获取系统时间（只取分:秒）
        t = time.strftime('%H:%M:%S', time.localtime())
        data = '3A30313033303130303030303146410D0A'
        # 接收到的字符串
        recv_data = ser.serial_cmd(data)
        # 格式化接收到的字符串
        temp = temp_parse(recv_data)
        log('receive_data', temp)
        socketio.emit('server_response',
                      {'data': temp, 'time': t},
                      namespace='/api/current_temp')  # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！


@app.route('/')
def index():
    # form = SetTemp()

    # set_temp = form.set_temp.data
    #
    # set_ramp = form.set_ramp.data
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/api/set_temp', methods=['GET', 'POST'])
def set_temp():
    set_temp = request.json.get('inputTemp')
    set_ramp = request.json.get('inputRamp')
    # global ser


    # data = request.json
    # set_data = int(set_temp) + int(set_ramp)
    if set_temp != '' and set_ramp != '':
        print(set_temp)
    elif set_temp != '' and set_ramp == '':
        set_ramp = '100.00'
        print(set_ramp)
    else:
        print('oooo')
    # print(set_ramp)
    return 'ok'


@app.route('/api/set_config', methods=['GET', 'POST'])
def set_config():

    return 'config'


# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/api/current_temp')
def ws_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app, debug=True)
