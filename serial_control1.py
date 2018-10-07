from serial import Serial
import time


class SerialControl(Serial):
    def __init__(self, port='com4', baudrate=19200, timeout=0.2):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
    # def __init__(self):
    #     super().__init__()

    def serial_send(self, cmd_send, cmd_end):
        self.open()
        # 把字符串转成bytes
        cmd_send = cmd_send.encode()

        # 清空串口发送缓冲区
        self.flushOutput()
        # 延迟0.01秒
        time.sleep(0.01)
        # 写入串口发送缓冲区
        cmd_end = bytes.fromhex(cmd_end)
        self.write(cmd_end)

        time.sleep(0.01)
        # 关闭串口
        self.close()

    def serial_recv(self):
        self.open()
        # 把字符串转成bytes
        # data_recv = ser.read_all().hex()
        cmd_recv = self.readall()
        # cmd_recv = self.read_all()
        cmd_recv = cmd_recv.decode('utf-8')
        # if cmd_recv is b'':
        #     cmd_recv = ''
        # print('recv', cmd_recv)
        # 清空串口接收缓冲区
        # ser.flushInput()
        # 延迟0.01秒
        time.sleep(0.1)
        # 关闭串口
        self.close()
        print('recv', cmd_recv)
        return cmd_recv

    def serial_read(self, data_send):
        self.open()
        data = bytes.fromhex(data_send)
             # 写入串口发送缓冲区
        self.write(data)
        time.sleep(0.05)
        data_recv = self.readall()
        time.sleep(0.01)
        # 清空串口发送缓冲区
        self.flushOutput()
        # 关闭串口
        self.close()
        return str(data_recv)

    def serial_cmd(ser, data_send):
        # 打开串口
        ser.open()
        # 要发送的命令
        data_send = bytes.fromhex(data_send)
        # 写入串口发送缓冲区
        ser.write(data_send)
        # 延时
        time.sleep(0.05)
        # 读取串口接收缓冲区,并把数据转换为bytes
        data_recv = ser.readall().decode()
        time.sleep(0.01)
        # 清空串口发送缓冲区
        ser.flushOutput()
        # 关闭串口
        ser.close()
        return data_recv

# config = dict(
#     port='com1',
#     baudrate=115200,
#
# )

# ser = SerialControl()
# print(ser.stopbits)
# a = 'AA BB 00 02 B1 01 B0 EF F0'
# ser.serial_send(a)


# def test1():
#     print(ser.port)
#
# test1()
