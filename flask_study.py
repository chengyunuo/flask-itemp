
import psutil
import time
from threading import Lock
from flask import Flask, render_template, session, request, url_for
from flask_socketio import SocketIO, emit
# from serial_control1 import SerialControl
from serial_control import *
from utils import log
from utils import temp_parse
# from flask import g


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
ser = serial_init()
serial_flag = True


thread = None
thread_lock = Lock()


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    """Example of how to send server generated events to clients."""
    global ser
    global serial_flag

    send_cmd = b':010301000001FA\r\n'

    while True:
        if serial_flag is True:
            # log('flag1', serial_flag)
            # if serial_flag is True:
            # 获取系统时间（只取分:秒）
            t = time.strftime('%H:%M:%S', time.localtime())
            # # 接收到的字符串
            # recv_data = ser.serial_cmd(data)
            # # 格式化接收到的字符串
            # temp = temp_parse(recv_data)
            # temp = read_temperature(ser, data_send1, data_send2)
            current_temperature = read_temperature(ser, send_cmd)
            # log('current_temperature', current_temperature)
            # temp = read_temperature(ser, data_send)
            # temp = read_cmd(ser)
            # log('receive_data', temp)
            socketio.emit('server_response',
                          {'data': current_temperature, 'time': t},
                          # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！
                          namespace='/api/current_temp')
            # 延时
            socketio.sleep(0.5)
        else:
            socketio.sleep(0.01)
            continue
    # else:
    #     # 延时
    #     log('flag2', serial_flag)
    #     time.sleep(0.1)





@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/api/stop_temp', methods=['GET', 'POST'])
def stop_temp():
    global ser
    global serial_flag
    stop_cmd = b':010608000000f1\r\n'

    if serial_flag is True:
        serial_flag = False
        # ser.close()
        # time.sleep(0.1)
        # stop_temperature(ser)
        while True:
            status_code = stop_temperature(ser, stop_cmd)
            if status_code == '':
                time.sleep(0.1)
            else:
                break
        serial_flag = True
    else:
        # ser.close()
        # time.sleep(0.1)
        while True:
            status_code = stop_temperature(ser, stop_cmd)
            if status_code == '':
                time.sleep(0.1)
            else:
                break
        serial_flag = True
    # stop_temperature(ser)
    return 'ok'


@app.route('/api/set_temp', methods=['GET', 'POST'])
def set_temp():
    global ser
    global serial_flag
    set_temp_value = request.json.get('inputTemp')
    set_ramp_value = request.json.get('inputRamp')
    if set_temp_value != '' and set_ramp_value != '':
        set_temp_value = int(set_temp_value)
        set_ramp_value = int(set_ramp_value)
        log(set_temp_value, set_ramp_value)
        # set_temperature(ser, set_temp_value, set_ramp_value)
        if serial_flag is True:
            serial_flag = False
            # ser.close()
            # time.sleep(0.1)
            # log('ser status', ser.isOpen())
            log('flag1', serial_flag)
            while True:
                status_code = set_temperature(ser, set_temp_value, set_ramp_value)
                if status_code == '':
                    time.sleep(0.1)
                else:
                    break
            log(22222, serial_flag)
            serial_flag = True
        else:
            # ser.close()
            # time.sleep(0.1)
            # set_temperature(ser, set_temp_value, set_ramp_value)
            while True:
                status_code = set_temperature(ser, set_temp_value, set_ramp_value)
                if status_code == '':
                    time.sleep(0.1)
                else:
                    break
            serial_flag = True
    elif set_temp_value != '' and set_ramp_value == '':
        set_ramp_value = '100.00'
        log(set_ramp_value)
    else:
        log('oooo')
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

    # while True:
    #     if serial_flag is True:
    #         while True:
    #             log('flag1', serial_flag)
    #             # if serial_flag is True:
    #             # 获取系统时间（只取分:秒）
    #             t = time.strftime('%H:%M:%S', time.localtime())
    #             # # 接收到的字符串
    #             # recv_data = ser.serial_cmd(data)
    #             # # 格式化接收到的字符串
    #             # temp = temp_parse(recv_data)
    #             # temp = read_temperature(ser, data_send1, data_send2)
    #             temp = read_temperature(ser)
    #             # temp = read_temperature(ser, data_send)
    #             # temp = read_cmd(ser)
    #             # log('receive_data', temp)
    #             socketio.emit('server_response',
    #                           {'data': temp, 'time': t},
    #                           # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！
    #                           namespace='/api/current_temp')
    #             # 延时
    #             socketio.sleep(0.5)
    #         # else:
    #         #     socketio.sleep(0.5)
    #         #     continue
    #     else:
    #         # 延时
    #         log('flag2', serial_flag)
    #         time.sleep(0.1)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
