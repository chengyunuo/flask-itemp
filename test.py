from utils import temp_parse, log
import serial
import time
import os


class Command(object):
    def __init__(self, fun_code='0103', register_address='0100', set_data=0.01, enter_code='0D0A'):
        self.fun_code = fun_code
        self.register_address = register_address
        self.set_data = set_data
        self.enter_code = enter_code

    # 数据解析
    def data_parse(self):
        temp = int(self.set_data * 100)
        log('temp1', temp)
        # 温度值解析成16进制字符串'{:0>4}'.format('{:x}'.format(temp))
        temp = self.fun_code + self.register_address + '{:0>4}'.format('{:x}'.format(temp))
        log('temp2', temp)
        hex_str = calc_lrc(temp)
        # 根据控制器文档要求，把指令转换成byte类型并回车
        byte_data = hex_str.encode() + bytes.fromhex(self.enter_code)
        log(byte_data)

        return byte_data


# windows上串口操作


def serial_init():
    ser = serial.Serial()
    ser.port = 'com6'
    ser.baudrate = 19200
    ser.parity = 'N'
    ser.bytesize = 8
    ser.stopbits = 1
    ser.timeout = 0.2
    ser.open()
    time.sleep(0.1)

    return ser


# def set(ser, data_send1, data_send2):
#     # 打开串口
#     ser.open()
#     # 要发送的命令
#     data_send1 = data_send1.encode()
#
#     log('data_send1', data_send1)
#     data_send2 = bytes.fromhex(data_send2)
#     log('data_send2', data_send2)
#     data_send = data_send1 + data_send2
#     log('data_send', data_send)
#     # 写入串口发送缓冲区
#     temp_data = ser.write(data_send)
#     log('temp_data', temp_data)
#     # 延时
#     time.sleep(0.1)
#     # 读取串口接收缓冲区,并把数据转换为bytes
#     # data_recv = ser.readall().decode()
#     buffer_recv = ser.readall()
#     if data_send1 == buffer_recv[:-2]:
#         log(1)
#         data_recv = ser.readall().decode()
#     else:
#         log(0)
#     log('data_recv', data_recv)
#     # 清空串口接收缓冲区
#     ser.flushInput()
#     # data_recv = ser.readall().decode()
#     # print('data_recv2', data_recv)
#     time.sleep(0.01)
#     # 清空串口发送缓冲区
#     ser.flushOutput()
#     # 关闭串口
#     ser.close()
#
#     return data_recv


# 向下位机发送指令，并且得到下位机应答数据
def serial_send(ser, register_address='0100', fun_code='0103', set_data=0.01):
    cmd_object = Command(register_address=register_address, fun_code=fun_code, set_data=set_data)
    cmd = cmd_object.data_parse()
    # 写入串口发送缓冲区
    ser.write(cmd)
    time.sleep(0.1)
    # 读取串口接收缓冲区,并把数据转换为bytes
    data_recv = ser.readall().decode()

    return data_recv


# 向下位机发送指令，并且得到下位机应答数据
def serial_send1(ser, data_send1, data_send2):

    # 要发送的命令
    data_send1 = data_send1.encode()
    log('data_send1', data_send1)
    data_send2 = bytes.fromhex(data_send2)
    log('data_send2', data_send2)
    data_send = data_send1 + data_send2
    log('data_send', data_send)
    # 打开串口
    # ser.open()
    # time.sleep(0.1)
    # 写入串口发送缓冲区
    # ser.write(data_send1)
    # time.sleep(0.1)
    # ser.write(data_send2)
    ser.write(data_send)
    # 延时
    # time.sleep(0.01)
    # 读取串口接收缓冲区,并把数据转换为bytes
    data_recv = ser.readall().decode()
    log('data_recv', data_recv)
    # # 清空串口接收缓冲区
    # ser.flushInput()
    # # 清空串口发送缓冲区
    # ser.flushOutput()
    # 关闭串口
    # ser.close()
    time.sleep(0.1)

    return data_recv

# 把串口缓冲区接收到的字符串转换成数字型温度值
# def temp_parse(recv_data):
#     r = '0x' + recv_data[7:11]
#     temp = int(r, 16)
#     # 温度数据除以100即为实际温度值
#     real_temp = temp / 100.00
#
#     return real_temp


# 读取温度
# def read_temp1(ser):
#     data1 = ':010301000001FA'
#     data2 = '0D0A'
#     temp = '3A30313033303130303030303146410D0A'
#
#     recv = serial_send(ser, data1, data2)
#     try:
#         real_temp = temp_parse(recv)
#     except:
#         ser.close()
#     finally:
#         log(real_temp)


# 读取温度
def read_temp(ser):
    data_recv = serial_send(ser)
    temperature = temp_parse(data_recv)

    log('temperature', temperature)

    return temperature


# 设置温度
def set_temp1(ser):

    sv_object = Command(register_address='000d', fun_code='0106', set_data=80)
    sv_cmd = sv_object.data_parse()
    time_object = Command(register_address='000e', fun_code='0106', set_data=3)
    time_cmd = time_object.data_parse()
    act_object = Command(register_address='0800', fun_code='0106', set_data=0.01)
    act_cmd = act_object.data_parse()
    ser.write(sv_cmd)
    time.sleep(0.1)
    ser.write(time_cmd)
    time.sleep(0.1)
    ser.write(act_cmd)


# 数据解析
def data_parse(register_addr='0100', set_data=0.01, fun_code='0103', enter_code='0D0A'):
    temp = int(set_data * 100)
    log('temp1', temp)
    # 温度值解析成16进制字符串'{:0>4}'.format('{:x}'.format(temp))
    temp = fun_code + register_addr + '{:0>4}'.format('{:x}'.format(temp))
    log('temp2', temp)
    hex_str = calc_lrc(temp)
    # 根据控制器文档要求，把指令转换成byte类型并回车
    byte_data = hex_str.encode() + bytes.fromhex(enter_code)
    log(byte_data)

    return byte_data


# 得到发送数据
# def send_parse(data):
#     temp = int(data * 100)
#     log('temp1', temp)
#     # 温度值解析成16进制字符串'{:0>4}'.format('{:x}'.format(temp))
#     temp = '01060101' + '{:0>4}'.format('{:x}'.format(temp))
#     log('temp2', temp)
#     hex_str = calc_lrc(temp)
#
#     return hex_str


# lrc码计算，所有16进制数相加的值，取反，然后加1
def calc_lrc(hex_str):
    input_byte = bytes.fromhex(hex_str)
    log('input_byte', input_byte)
    lrc = 0
    # byte数组
    message = bytearray(input_byte)
    log(message)
    # 所有16进制数相加
    for b in message:
        lrc += b
    #   取反
    lrc ^= 0xff
    lrc += 1
    # lrc取低8位
    lrc_data = ':' + hex_str + '{:0>2}'.format('{:x}'.format(lrc))
    log('lrc_data', lrc_data)

    return lrc_data


if __name__ == "__main__":
    pass
    ser = serial_init()
    read_temp(ser)
    # set_temp1(ser)

    # serial_send(ser, ':0106000d138851', '0D0A')
    # serial_send(ser, ':0106000e012cbe', '0D0A')
    # 开启程序段模式
    # serial_send(ser, ':010608000001f0', '0D0A')
    # read_cmd = Command()
    # a = read_cmd.data_parse()


    # 关闭程序段模式，开启sv模式
    # serial_send(ser, ':010608000000f1', '0D0A')
    # deact_object = Command(register_address='0800', fun_code='0106', set_data=0)
    # deact_cmd = deact_object.data_parse()
    # ser.write(deact_cmd)
    # ser.close()



