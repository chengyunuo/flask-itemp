__author__ = 'anigon'

from flask import Flask, render_template
from flask_sockets import Sockets
import datetime
import time
import serial
import random
import psutil
import time

from threading import Lock


# windows上串口操作
def serial_init():
    ser = serial.Serial()
    ser.port = 'com1'
    ser.baudrate = 115200
    ser.parity = 'N'
    ser.bytesize = 8
    ser.stopbits = 1
    ser.timeout = 0.2

    return ser


def serial_send(ser, data_send):
    ser.open()
    # 把字符串转成bytes
    data = bytes.fromhex(data_send)
    # 清空串口发送缓冲区
    ser.flushOutput()
    # 延迟0.01秒
    time.sleep(0.01)
    # 写入串口发送缓冲区
    ser.write(data)
    time.sleep(0.01)
    # 关闭串口
    ser.close()


def serial_recv(ser):
    ser.open()
    # 把字符串转成bytes
    # data_recv = ser.read_all().hex()
    data_recv = ser.readall()
    if data_recv is b'':
        data_recv = ''
    print('recv', data_recv)
    # 清空串口接收缓冲区
    # ser.flushInput()
    # 延迟0.01秒
    time.sleep(0.1)
    # 关闭串口
    ser.close()
    return str(data_recv)

app = Flask(__name__)

ser = serial_init()
sockets = Sockets(app)


@sockets.route('/temp')
def temp_socket(ws):
    while not ws.closed:
        temp_data = serial_recv(ser)
        last_data = temp_data[:]
        if temp_data is None:
            temp_data = last_data
        print('temp', temp_data)
        ws.send(temp_data)
        time.sleep(0.1)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        now = datetime.datetime.now().isoformat() + 'Z'
        ws.send(now)  # 发送数据
        time.sleep(0.01)


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()
