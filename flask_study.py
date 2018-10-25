from threading import Lock
from flask import Flask, render_template, request
from flask import jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from serial_control import *
from utils import log


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求
CORS(app, resources=r'/*')
socketio = SocketIO(app, async_mode=async_mode)
# 串口初始化
ser = serial_init()


# 初始化线程
thread = None
thread_lock = Lock()


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    """Example of how to send server generated events to clients."""
    global ser

    # send_cmd = ':010301000001FA\r\n'
    # 读取当前温度指令
    read_cmd = ':010301000001FA\r\n'
    read_cmds = dict(
        read_cmd=read_cmd,
    )
    while True:
        # 串口一直打开的方式
        # 获取系统时间（只取分:秒）
        t = time.strftime('%H:%M:%S', time.localtime())
        # 接收到的数据
        read_datas = read_temperature(ser, read_cmds)
        current_temperature = read_datas.get('temperature')

        socketio.emit('server_response',
                      {'data': current_temperature, 'time': t},
                      # 注意：这里不需要客户端连接的上下文，默认 broadcast = True
                      namespace='/api/current_temp')
        # 延时
        socketio.sleep(0.8)

        # recv_data = ser.serial_cmd(data)
        # # 格式化接收到的字符串
        # temp = temp_parse(recv_data)
        # temp = read_temperature(ser, data_send1, data_send2)

        # log('current_temperature', current_temperature)
        # temp = read_temperature(ser, data_send)
        # temp = read_cmd(ser)
        # log('receive_data', temp)

        # 串口每次打开关闭的方式
        # if serial_flag is True:
        #     # log('flag1', serial_flag)
        #     # if serial_flag is True:
        #     # 获取系统时间（只取分:秒）
        #     t = time.strftime('%H:%M:%S', time.localtime())
        #     # # 接收到的字符串
        #     # recv_data = ser.serial_cmd(data)
        #     # # 格式化接收到的字符串
        #     # temp = temp_parse(recv_data)
        #     # temp = read_temperature(ser, data_send1, data_send2)
        #     current_temperature = read_temperature(ser, send_cmd)
        #     log('current_temperature', current_temperature)
        #     # temp = read_temperature(ser, data_send)
        #     # temp = read_cmd(ser)
        #     # log('receive_data', temp)
        #     socketio.emit('server_response',
        #                 {'data': current_temperature, 'time': t},
        #     # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！
        #                 namespace='/api/current_temp')
        #     # 延时
        #     socketio.sleep(0.5)
        #     log(111111)
        # else:
        #     socketio.sleep(0.5)
        #     log(222222)
        #     continue


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/api/stop_temp', methods=['GET', 'POST'])
def stop_temp():
    global ser

    stop_cmds = request.json
    # stop_cmds = dict(
    #     fix_cmd=fix_cmd,
    #
    # )
    log('stop_cmds', stop_cmds)

    stop_return = stop_temperature(ser, stop_cmds)
    log('stop_return', stop_return)

    return jsonify(stop_return)
    # 从浏览器获取到的数据是字符串的
    # stop_cmd = request.json.get('stop_cmd')
    # stop_cmd = stop_cmd.encode()
    # stop_cmd = b':010608000000f1\r\n'
    # 串口一直打开的方式

    # 串口每次打开关闭的方式
    # if serial_flag is True:
    #     serial_flag = False
    #     # ser.close()
    #     # time.sleep(0.1)
    #     # stop_temperature(ser)
    #     while True:
    #         status_code = stop_temperature(ser, stop_cmd)
    #         if status_code == '':
    #             time.sleep(0.1)
    #         else:
    #             break
    #     serial_flag = True
    # else:
    #     while True:
    #         status_code = stop_temperature(ser, stop_cmd)
    #         if status_code == '':
    #             time.sleep(0.1)
    #         else:
    #             break
    #     serial_flag = True
    # stop_temperature(ser)


@app.route('/api/pause_temp', methods=['GET', 'POST'])
def pause_temp():
    global ser

    pause_cmds = request.json
    # log('pause_cmds', pause_cmds)
    # pause_cmds = dict(
    #     fix_cmd=fix_cmd,
    #     read_cmd=read_cmd,
    # )

    pause_return = pause_temperature(ser, pause_cmds)
    log('pause_return', pause_return)

    return jsonify(pause_return)

    # 从浏览器获取到的数据是字符串的
    # stop_cmd = request.json.get('stop_cmd')


    # 串口一直打开的方式
    # cmd_status = stop_temperature(ser, stop_cmd)
    # log('cmd_status', cmd_status)


@app.route('/api/set_temp', methods=['GET', 'POST'])
def set_temp():
    global ser
    set_cmds = request.json
    # log('request.json', request.json)
    #
    # require_cmds = ['deact_cmd', 'sv_cmd', 'time_cmd', 'act_cmd']
    # set_cmds = {}
    # for require_cmd in require_cmds:
    #     set_cmds[require_cmd] = request.json.get(require_cmd)
    # sv_cmd = request.json.get('sv')
    # set_cmds['sv_cmd'] = sv_cmd
    # time_cmd = request.json.get('time')
    # set_cmds['time_cmd'] = time_cmd
    # act_cmd = request.json.get('act')
    # set_cmds['act_cmd'] = act_cmd
    log('set_cmds', set_cmds)

    # 串口一直打开的方式
    set_return = set_temperature(ser, set_cmds)
    log('set_return', set_return)

    return jsonify(set_return)
    # 串口每次打开关闭的方式
    # if set_temp_value != '' and set_ramp_value != '':
    #     # set_temp_value = int(set_temp_value)
    #     # set_ramp_value = int(set_ramp_value)
    #     # log(set_temp_value, set_ramp_value)
    #
    #     # set_temperature(ser, set_temp_value, set_ramp_value)
    #     # sv_cmd = b':0106000d138851\r\n'
    #     # time_cmd = b':0106000e012cbe\r\n'
    #     if serial_flag is True:
    #         serial_flag = False
    #         # ser.close()
    #         # time.sleep(0.1)
    #         # log('ser status', ser.isOpen())
    #         # log('flag1', serial_flag)
    #         while True:
    #             status_code = set_temperature(ser, sv_cmd, time_cmd, act_cmd)
    #             if status_code == '':
    #                 time.sleep(0.1)
    #             else:
    #                 break
    #         log(22222, serial_flag)
    #         serial_flag = True
    #     else:
    #         # ser.close()
    #         # time.sleep(0.1)
    #         # set_temperature(ser, set_temp_value, set_ramp_value)
    #         while True:
    #             status_code = set_temperature(ser, sv_cmd, time_cmd, act_cmd)
    #             if status_code == '':
    #                 time.sleep(0.1)
    #             else:
    #                 break
    #         serial_flag = True
    # elif set_temp_value != '' and set_ramp_value == '':
    #     set_ramp_value = '100.00'
    #     log(set_ramp_value)
    # else:
    #     log('oooo')


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
    socketio.run(app, host='0.0.0.0')
