import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


# 把串口缓冲区接收到的字符串转换成数字型温度值
def temp_parse(recv_data):
    # log('recv_data', recv_data)
    # 字符串切片并拼接0x
    try:
        hex_str = '0x' + recv_data[7:11]
        # 把字符串转成16进制
        dec_num = int(hex_str, 16)
        # 根据协议生成实际温度值,温度数据除以100即为实际温度值
        real_temp = dec_num / 100.00
        return real_temp
    except:
        log('error')

