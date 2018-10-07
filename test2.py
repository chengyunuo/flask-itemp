import serial
import time


# windows上串口操作
def serial_init():
    ser = serial.Serial()
    ser.port = 'com6'
    ser.baudrate = 19200
    ser.parity = 'N'
    ser.bytesize = 8
    ser.stopbits = 1
    ser.timeout = 0.2
    # ser.writeTimeout = 0.6
    # ser.open()

    return ser


def serial_cmd(ser, data_send):
    # 打开串口
    ser.open()
    time.sleep(0.1)
    # 要发送的命令
    data_send = bytes.fromhex(data_send)
    print('data_send:', data_send)
    # 写入串口发送缓冲区
    ser.write(data_send)
    # 延时
    time.sleep(0.1)
    # 读取串口接收缓冲区,并把数据转换为bytes
    data_recv = ser.readall().decode()
    print('data_recv:', data_recv)

    # 清空串口发送缓冲区
    # ser.flushOutput()
    time.sleep(0.1)
    # 关闭串口
    ser.close()


ser = serial_init()
data_send = '3A30313033303130303030303146410D0A'

# 0D0A
data = '010301000001FA'
