from utils import temp_parse
from utils import log
import serial
import time
import os


# 串口初始化
def serial_init():
    ser = serial.Serial()
    ser.port = 'com6'
    ser.baudrate = 19200
    ser.parity = 'N'
    ser.bytesize = 8
    ser.stopbits = 1
    ser.timeout = 0.1
    # ser.writeTimeout = 0.2
    # ser.open()
    # time.sleep(0.1)

    return ser


class Command(object):
    def __init__(self, fun_code='0103', register_address='0100', set_data=0.01, enter_code='0D0A'):
        self.fun_code = fun_code
        self.register_address = register_address
        self.set_data = set_data
        self.enter_code = enter_code

    # 数据解析
    def data_parse(self):
        temp = int(self.set_data * 100)
        log('temp', temp)
        # 温度值解析成16进制字符串'{:0>4}'.format('{:x}'.format(temp))
        data_format = '{:0>4}'.format('{:x}'.format(temp))
        log('data_format', data_format)
        temp = self.fun_code + self.register_address + data_format
        hex_str = calc_lrc(temp)
        log('hex_str', hex_str)
        # 根据控制器文档要求，把指令转换成byte类型并回车
        byte_data = hex_str.encode() + bytes.fromhex(self.enter_code)

        return byte_data


# 向下位机发送指令，并且得到下位机应答数据
def serial_send(ser, send_cmd):
    # ser.close()
    # time.sleep(0.1)
    # cmd_object = Command(register_address=register_address, fun_code=fun_code, set_data=set_data)
    # cmd = cmd_object.data_parse()
    # log('cmd', cmd)
    ser.open()
    time.sleep(0.1)
    # 写入串口发送缓冲区
    ser.write(send_cmd)
    time.sleep(0.1)
    # 读取串口接收缓冲区,并把数据转换为bytes
    data_recv = ser.readall().decode()
    ser.close()
    # time.sleep(0.1)

    return data_recv


def serial_send1(ser, register_address='0100', fun_code='0103', set_data=0.01):
    ser.close()
    time.sleep(0.1)
    cmd_object = Command(register_address=register_address, fun_code=fun_code, set_data=set_data)
    cmd = cmd_object.data_parse()
    log('cmd', cmd)
    ser.open()
    time.sleep(0.1)
    # 写入串口发送缓冲区
    ser.write(cmd)
    time.sleep(0.2)
    # 读取串口接收缓冲区,并把数据转换为bytes
    data_recv = ser.readall().decode()
    ser.close()
    time.sleep(0.1)

    return data_recv


# 读取温度
def read_temperature(ser):
    send_cmd = b':010301000001FA\r\n'
    data_recv = serial_send(ser, send_cmd)
    temperature = temp_parse(data_recv)

    return temperature


# 按照程序段模式设定温度
def set_temperature(ser, set_temp_value, set_ramp_value):
    # 发送sv命令
    sv = serial_send(
        ser,
        register_address='000d',
        fun_code='0106',
        set_data=set_temp_value,
    )
    log('sv', sv)

    # 发送time命令
    time = serial_send(
        ser,
        register_address='000e',
        fun_code='0106',
        set_data=set_ramp_value,
    )
    log('time', time)
    # 发送程序段启动命令
    act = serial_send(
        ser,
        register_address='0800',
        fun_code='0106',
        set_data=0.01,
    )
    log('act', act)

    return True


def stop_temperature(ser):
    # 发送程序段停止命令
    serial_send(
        ser,
        register_address='0800',
        fun_code='0106',
        set_data=0,
    )


# 根据操作系统类型，得出串口名
def serial_name():
    win32_serial = 'com6'
    unix_serial = '/dev/ttyUSB0'
    sys_name = os.name
    if sys_name == 'nt':
        name = win32_serial
    else:
        name = unix_serial

    return name


# lrc数据验证码计算，所有16进制数相加的值，取反，然后加1
def calc_lrc(hex_str):
    input_byte = bytes.fromhex(hex_str)
    # print('hex_str', hex_str)
    lrc = 0
    # byte数组
    message = bytearray(input_byte)
    log('message', message)
    # 所有16进制数相加
    for b in message:
        lrc += b
    #   取反
    lrc ^= 0xff
    lrc += 1
    # 取低8位
    lrc &= 0xff
    log('lrc {:x}', lrc)
    # lrc取低8位
    data = '{:0>2}'.format('{:x}'.format(lrc))
    log('data', data)
    lrc_data = ':' + hex_str + data
    log('lrc_data', lrc_data)

    return lrc_data


# # 向下位机控制器发送指令，并且得到下位机应答数据
# def serial_send1(ser, data_send1, data_send2):
#     # 组装要发送的命令
#     data_send1 = data_send1.encode()
#     data_send2 = bytes.fromhex(data_send2)
#     data_send = data_send1 + data_send2
#     # 打开串口
#     ser.open()
#     # 很重要的延时，判断是串口打开需要一些时间
#     time.sleep(0.1)
#     # 写入串口发送缓冲区
#     # ser.write(data_send1)
#     # ser.write(data_send2)
#     ser.write(data_send)
#     # 延时
#     time.sleep(0.1)
#     # 读取串口接收缓冲区,并把数据转换为bytes
#     data_recv = ser.readall().decode()
#     # log('data_recv', data_recv)
#     # 清空串口接收缓冲区
#     ser.flushInput()
#     # 清空串口发送缓冲区
#     ser.flushOutput()
#     # 关闭串口
#     ser.close()
#
#     return data_recv
#
#
# # 读取温度
# def read_temperature1(ser, data_send1, data_send2):
#     recv = serial_send(ser, data_send1, data_send2)
#     try:
#         real_temp = temp_parse(recv)
#     except:
#         real_temp = 25.0
#         ser.close()
#     # finally:
#     #     print(real_temp)
#
#     return real_temp
#
#
# # 得到发送数据
# def send_parse(data):
#     temp = int(data * 100)
#     print('temp1', temp)
#     # 温度值解析成16进制字符串'{:0>4}'.format('{:x}'.format(temp))
#     temp = '01060101' + '{:0>4}'.format('{:x}'.format(temp))
#     print('temp2', temp)
#     hex_str = calc_lrc(temp)
#
#     return hex_str


# 把串口缓冲区接收到的字符串转换成数字型温度值
# def temp_parse(recv_data):
#     # 字符串切片并拼接0x
#     hex_str = '0x' + recv_data[7:11]
#     # 把字符串转成16进制
#     dec_num = int(hex_str, 16)
#     # 根据协议生成实际温度值,温度数据除以100即为实际温度值
#     real_temp = dec_num / 100.00
#     return real_temp


# # 数据解析
# def data_parse(register_addr='0100', set_data=0.01, fun_code='0103', enter_code='0D0A'):
#     temp = int(set_data * 100)
#     # print('temp1', temp)
#     # 温度值解析成16进制字符串'{:0>4}'.format('{:x}'.format(temp))
#     temp = fun_code + register_addr + '{:0>4}'.format('{:x}'.format(temp))
#     # print('temp2', temp)
#     hex_str = calc_lrc(temp)
#     # 根据控制器文档要求，把指令转换成byte类型并回车
#     byte_data = hex_str.encode() + bytes.fromhex(enter_code)
#     # log(byte_data)
#
#     return byte_data
#
#
# # 程序段方式设定温度，取程序段1，设置sv为50C，1388
# def set_temperature1(ser, sv, ramp):
#     # temp = int(sv * 100)
#     # print('temp1', temp)
#     # temp = '01060101' + '{:0>4}'.format('{:x}'.format(temp))
#     # print('temp2', temp)
#     # data1 = calc_lrc(temp)
#     data1 = send_parse(sv)
#     log(data1)
#     # data1 = ':010601010bb8'
#     data2 = '0D0A'
#     recv = serial_send(ser, data1, data2)
#     return recv
#
#
# # 设定温度，设置sv为50C，1388
# def set_temperature1(ser, sv):
#     # temp = int(sv * 100)
#     # print('temp1', temp)
#     # temp = '01060101' + '{:0>4}'.format('{:x}'.format(temp))
#     # print('temp2', temp)
#     # data1 = calc_lrc(temp)
#     data1 = send_parse(sv)
#     # data1 = ':010601010bb8'
#     data2 = '0D0A'
#     recv = serial_send(ser, data1, data2)
#     return recv





if __name__ == "__main__":
    pass
    # ser = serial_init()
#
#     # 一次设置有可能不会成功
#     # set_temp(40.00)
#     # 多次设置
#     # for i in range(6):
#     #     set_temp(30.00)
#     multi_set(30.00)
#     prog_parse('000d', 50)
#     data_parse()
    # data_parse(register_addr='000d', set_data=50, fun_code='0106')


