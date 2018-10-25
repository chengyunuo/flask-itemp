from utils import data_parse32
from utils import log
from utils import calc_lrc
import serial
import time
import os

# # 停止指令，也就是切换到fix模式下
# fix_cmd = ':010608000000f1\r\n'
# # 读取当前温度指令
# read_cmd = ':010301000001FA\r\n'
last_read = 0


# 串口初始化
def serial_init():
    try:
        ser = serial.Serial()

        ser.port = 'com6'
        ser.baudrate = 19200
        ser.parity = 'N'
        ser.bytesize = 8
        ser.stopbits = 1
        ser.timeout = 0.1

        # 打开串口
        ser.open()
        time.sleep(0.1)
    except:
        print(123456)

    return ser


# 向下位机发送指令，并且得到下位机应答数据
def serial_send(ser, send_cmd, is_read=True):
    # cmd_object = Command(register_address=register_address, fun_code=fun_code, set_data=set_data)
    # cmd = cmd_object.data_parse()
    # log('cmd', cmd)
    # ser.open()
    # time.sleep(0.1)
    global last_read
    # 返回的数据
    return_data = {}
    # 写入串口发送缓冲区,写入的数据是bytes型
    send_cmd = send_cmd.encode()
    ser.write(send_cmd)
    # 延时小于0.2会出现读取到空
    time.sleep(0.3)
    # 读取串口接收缓冲区,并把数据转换为bytes
    serial_recv = ser.read_until().decode()
    # log('serial_recv', serial_recv)
    # 判断是否是读取温度的指令，如果是，则把当前温度保存在last_read
    if is_read:
        return_data['read_cmd'] = serial_recv
        return_data['other_cmd'] = serial_recv
        last_read = serial_recv
    else:
        return_data['read_cmd'] = last_read
        return_data['other_cmd'] = serial_recv
    # log('serial_recv', serial_recv)
    # serial_recv = ser.readall().decode()
    # data_recv = ser.readall()
    # log('data_recv', type(data_recv))
    # ser.close()
    # time.sleep(0.1)

    # 返回bytes字符串
    return return_data


# def serial_send1(ser, register_address='0100', fun_code='0103', set_data=0.01):
#     ser.close()
#     time.sleep(0.1)
#     cmd_object = Command(register_address=register_address, fun_code=fun_code, set_data=set_data)
#     cmd = cmd_object.data_parse()
#     log('cmd', cmd)
#     ser.open()
#     time.sleep(0.1)
#     # 写入串口发送缓冲区
#     ser.write(cmd)
#     time.sleep(0.2)
#     # 读取串口接收缓冲区,并把数据转换为bytes
#     data_recv = ser.readall().decode()
#     ser.close()
#     time.sleep(0.1)
#
#     return data_recv


# 读取温度
def read_temperature(ser, read_cmds):
    # read_datas是读取到的返回值 和 解析成int型的温度值
    # {
    #     'read_recv': read_recv,
    #     'temperature': temperature,
    # }
    # # 读取当前温度指令
    # read_cmd = ':010301000001FA\r\n'
    # read_cmds = kwargs

    return_data = {
        'serial_status': False,
    }
    read_recv = serial_send(ser, read_cmds['read_cmd'])
    # 判断是否指令是否发送成功，不成功直接返回False
    if len(read_recv['read_cmd']) == 0:
        return return_data
    # 把接收到的字符串解析成温度值（整型）
    temperature = data_parse32(read_recv['read_cmd'])
    # 生成返回值
    return_data['serial_status'] = True
    return_data['read_recv'] = read_recv
    return_data['temperature'] = temperature

    return return_data


# 设置温度，在程序模式下，程序段1中设置
# def set_temperature(ser, set_cmds):
def set_temperature(ser, set_cmds):

    return_data = {
        'serial_status': False,
    }
    # # 切换到fix模式指令
    # fix_cmd = ':010608000000f1\r\n'
    # # 发送程序段停止命令
    # fix_recv = serial_send(ser, fix_cmd)
    # # 判断指令是否发送成功，不成功直接返回False
    # if len(fix_recv) == 0:
    #     return return_data
    # set_cmds = kwargs
    count = 0
    for k, v in set_cmds.items():
        log('v', count, v)
        count += 1
        return_data[k] = serial_send(ser, v, is_read=False)['other_cmd']
        if len(return_data[k]) == 0:
            return return_data
    return_data['serial_status'] = True
    # log('return_data', return_data)

    return return_data


# 停止加热，温度回复到默认sv
def stop_temperature(ser, stop_cmds):
    return_data = {
        'serial_status': False,
    }
    # # 停止指令，也就是切换到fix模式下
    # fix_cmd = ':010608000000f1\r\n'
    # 发送程序段停止命令
    fix_recv = serial_send(ser, stop_cmds['fix_cmd'], is_read=False)
    # 判断是否指令是否发送成功，不成功直接返回False
    if len(fix_recv['other_cmd']) == 0:
        return return_data
    return_data['serial_status'] = True

    return return_data


# 暂停加热，切换到模式，并且把当前温度设置为sv
def pause_temperature(ser, pause_cmds):
    return_data = {
        'serial_status': False,
    }
    # # 切换到fix模式指令
    # fix_cmd = ':010608000000f1\r\n'
    # # 读取当前温度指令
    # read_cmd = ':010301000001FA\r\n'

    read_cmds = pause_cmds.copy()
    read_cmds.pop('fix_cmd')

    read_datas = read_temperature(ser, read_cmds)
    if read_datas['serial_status'] is False:
        return return_data
    # 1、先把系统从程序模式切换到fix模式，然后再把读取的温度进行解析
    fix_recv = serial_send(ser, pause_cmds['fix_cmd'], is_read=False)
    log('fix_recv', fix_recv)
    if len(fix_recv['other_cmd']) == 0:
        return return_data
    # 解析读取的温度为fix模式sv指令
    parse_temperature = read_datas.get('read_recv')

    temp = '01060101' + parse_temperature['read_cmd'][7:11]

    sv_cmd = calc_lrc(temp)
    # 2、设置sv为当前温度
    sv_recv = serial_send(ser, sv_cmd, is_read=False)
    if len(sv_recv['other_cmd']) == 0:
        return return_data
    return_data['serial_status'] = True

    return return_data


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


if __name__ == "__main__":
    pass
