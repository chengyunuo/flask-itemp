# import serial.tools.list_ports
#
# plist = list(serial.tools.list_ports.comports())
#
# if len(plist) <= 0:
#     print("没有发现端口!")
# else:
#     plist_0 = list(plist[0])
#     serialName = plist_0[0]
#     serialFd = serial.Serial(serialName, 9600, timeout=60)
#     print("可用端口名>>>", serialFd.name)

# import serial
#
# class Ser(object):
#     def __init__(self):
#         # 打开端口
#         self.port = serial.Serial(port='COM1', baudrate=115200, bytesize=8, parity='E', stopbits=1, timeout=2)
#
#     # 发送指令的完整流程
#     def send_cmd(self, cmd):
#         # send_data =
#         self.port.write(cmd)
#         response = self.port.readall()
#         response = self.convert_hex(response)
#         return response
#
#     # 转成16进制的函数
#     def convert_hex(self, string):
#         res = []
#         result = []
#         for item in string:
#             res.append(item)
#         for i in res:
#             result.append(hex(i))
#         return result

# import binascii,time
# a = 'AA BB 00 02 B1 01 B0 EF F0'
# a = bytes.fromhex(a)
# # a_list = []
# # for i in a.split():
# #     a_list.append(binascii.a2b_hex(i))
# # print(a_list[0])
# #
# print(a)
# ser = serial.Serial('com1', 115200)
# ser.parity = serial.PARITY_NONE
# ser.stopbits = 1
#
# ser.write(a)
# time.sleep(1)
# print(ser.read_all())
# ser.closed



import serial, binascii
import time

# 打开串口
# ser = serial.Serial("/dev/ttyUSB0",9600)
# 创建serial实例
ser = serial.Serial()
ser.port = 'com1'
ser.baudrate = 115200
ser.parity = 'N'
ser.bytesize = 8
ser.stopbits = 1
ser.timeout = 0.2


def main():
    # 打开串口
    while True:
        ser.open()
    # 发送
    # code = '01 03 40 00 00 02 D1 CB'
    # send_code = 'AA BB 00 02 B1 01 B0 EF F0'
    # code = bytes.fromhex(send_code)
    # # ser.write(bytes.fromhex(code))
    # # print(code)
    # ser.flushOutput()
    # time.sleep(0.01)
    # ser.write(code)
    # time.sleep(0.01)
        recv = ser.readall()
    # data = recv[14:18]
    # data_10 = int(data, 16)
    # current_temp = data_10 / 100
    # # data_16 = binascii.a2b_hex(data)
    # # print(data_16)
        print('recv', recv)
        ser.flushInput()
    # print(current_temp)
    # ser.flushInput()
        time.sleep(0.01)
        ser.close()
        time.sleep(5)


#     while True:
#
#         # 获得接收缓冲区字符
#         count = ser.inWaiting()
#         if count != 0:
#             # 读取内容并回显
#             recv = ser.read(count)
#             data= recv.hex()
#             print(data);
# #            ser.write(recv)
#         # 清空接收缓冲区
#         ser.flushInput()
#         # 必要的软件延时
#         time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()

            # import serial.tools.list_ports
            #
            # plist = list(serial.tools.list_ports.comports())
            #
            # if len(plist) <= 0:
            #     print("没有发现端口!")
            # else:
            #     plist_0 = list(plist[0])
            #     serialName = plist_0[0]
            #     serialFd = serial.Serial(serialName, 9600, timeout=60)
            #     print("可用端口名>>>", serialFd.name)
            #
            # # 所发十六进制字符串010591F50000F104
            # cmd = [0xAA, 0xBB, 0x00, 0x02, 0xB1, 0x01, 0xB0, 0xEF, 0xF0]
            #
            #
            # import serial
            #
            #
            # class Ser(object):
            #     def __init__(self):
            #         # 打开端口
            #         self.port = serial.Serial(port='com3', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0.2)
            #         # self.port = serial.Serial(port='COM1', baudrate=115200)
            #
            #     # 发送指令的完整流程
            #     def send_cmd(self, cmd):
            #         self.port.write(cmd)
            #         response = self.port.readall()
            #         response = self.convert_hex(response)
            #         return response
            #
            #     # 转成16进制的函数
            #     def convert_hex(self, string):
            #         res = []
            #         result = []
            #         for item in string:
            #             res.append(item)
            #         for i in res:
            #             result.append(hex(i))
            #         return result
            #
            # s = Ser()
            #
            # print(s.send_cmd(cmd))
