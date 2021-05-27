# -*- coding: UTF-8 -*-
''' 
@Time : 2021/5/18 17:52 
@Author : Silicon-He
@File : en_decoder.py 
@Software: PyCharm
'''

class CRC:
    def __init__(self, info, crc_n=32):
        self.info = info
        # 初始化生成多项式p
        loc = [32, 26, 23, 22, 16, 12, 11, 10, 8, 7, 5, 2, 1, 0]
        if crc_n == 8:
            loc = [8, 2, 1, 0]
        elif crc_n == 16:
            loc = [16, 15, 2, 0]
        p = [0 for i in range(crc_n + 1)]
        for i in loc:
            p[i] = 1

        info = self.info.copy()
        times = len(info)
        n = crc_n + 1

        # 左移补零
        for i in range(crc_n):
            info.append(0)
        # 除
        q = []
        for i in range(times):
            if info[i] == 1:
                q.append(1)
                for j in range(n):
                    info[j + i] = info[j + i] ^ p[j]
            else:
                q.append(0)

        # 余数
        check_code = info[-crc_n::]

        # 生成编码
        code = self.info.copy()
        for i in check_code:
            code.append(i)

        self.crc_n = crc_n
        self.p = p
        self.q = q
        self.check_code = check_code
        self.code = code

    def print_format(self):
        """格式化输出结果"""

        print('{:10}\t{}'.format('信息：', self.info))
        print('{:10}\t{}'.format('生成多项式：', self.p))
        print('{:11}\t{}'.format('商：', self.q))
        print('{:10}\t{}'.format('余数：', self.check_code))
        print('{:10}\t{}'.format('编码：', self.code))

    def get_code(self):
        return ''.join([str(i) for i in self.code])


    def get_check_code(self):
        return ''.join([str(i) for i in self.check_code])

'''
对字符转成2进制
'''
def msg_encode(msg: str) -> str:
    # 字符串转ascii/unicode码
    msg_list = [ord(i) for i in msg]
    # print("unicode码:",msg_list)

    # unicode转二进制
    msg_byte = [bin(i) for i in msg_list]
    # print("二进制unicode码:",msg_byte)

    # 将不足两字节的unicode码补齐两字节（16bytes）
    for i in range(len(msg_byte)):
        length_minus = 18 - len(msg_byte[i])
        msg_byte[i] = '0' * length_minus + msg_byte[i][2:]
    # print("补零后二进制unicode码:",msg_byte)
    return ''.join(msg_byte)

'''
将二进制转成字符
'''
def msg_decode(msg):
    msg_byte = [msg[i:i + 16] for i in range(0, len(msg), 16)]
    # print('补零后二进制unicode码:',msg_byte)
    # 将二进制转十进制
    msg_byte_deocde = [int(i, 2) for i in msg_byte]
    # print("十进制unicode码：",msg_byte_deocde)

    # 十进制unicode转字符串
    msg_decode = [chr(i) for i in msg_byte_deocde]
    # print("字符串：",msg_decode)

    # 将字符串列表连接成字符串
    # print('译码后：',''.join(msg_decode))
    msg_out = ''.join(msg_decode).replace('TRATRA','TRA')
    msg_out = msg_out.replace('TRAART','ART')
    msg_out = msg_out.replace('TRAFRE','FRE')

    return msg_out


def crc_encode(msg_byte: str) -> str:
    msg_byte_spilt = [int(i) for i in msg_byte]
    msg_crc = CRC(msg_byte_spilt, 32)
    msg_crc_code = msg_crc.get_code()
    return ''.join(map(str,msg_crc_code))


'''
ART起始 TRA转义 FRE结束
'''
def package_msg(msg: str) -> str:
    return msg_encode('ART') + msg + msg_encode('FRE')


def check_msg(msg: str) -> str:
    msg = msg.replace('TRA', 'TRATRA')
    msg = msg.replace('ART', 'TRAART')
    msg_after = msg.replace('FRE', 'TRAFRE')
    return msg_after

def unpack_msg(msg:str):
    ART_code = msg_encode('ART')
    FRE_code = msg_encode('FRE')

    if msg.startswith(ART_code) and msg.endswith(FRE_code):
        msg = msg[len(ART_code):-len(FRE_code)]
        # msg_pure = msg_decode(msg[:-32])
        msg_pure = msg[:-32]
        check_code = msg[-32:]
        return msg_pure,check_code
    else:
        raise ValueError('没有找到起始码/结束码')


if __name__ == '__main__':
    # a = '你好！hello!@#$#$'
    # b = msg_encode(a)
    # c = check_msg(b)
    # d = crc_encode(c)
    # e = package_msg(d)
    # #conn.send(e)
    # msg,check_code = unpack_msg(e)
    '''
    a == msg
    '''

    j,k = unpack_msg('0000000001000001000000000101001000000000010101000000000000110001000000000011000101101111110001100000100011010110000000000100011000000000010100100000000001000101')
    print(j)