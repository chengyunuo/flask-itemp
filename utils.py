import time


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


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


# 把串口缓冲区接收到的字符串转换成数字型温度值
def temp_parse(recv_data):
    log('recv_data', recv_data)
    # 字符串切片并拼接0x
    try:
        hex_str = '0x' + recv_data[7:11]
        # 把字符串转成16进制
        dec_num = int(hex_str, 16)
        # 根据协议生成实际温度值,温度数据除以100即为实际温度值
        real_temp = dec_num / 100.00
        return real_temp
    except:
        log('error format')


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

