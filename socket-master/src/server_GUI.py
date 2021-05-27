# -*- coding: UTF-8 -*-
'''
@Time : 2021/5/17 12:52
@Author : Silicon-He
@File : server.py
@Software: PyCharm
'''
import wx.adv
import wx
import threading
import time
import socket
from en_decoder import *
import re

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='服务端', size=(660, 741), name='frame', style=541072896)
        icon = wx.Icon(r'./ico.jpg')
        self.SetIcon(icon)
        self.start_windows = wx.Panel(self)
        self.Centre()
        self.title_set()
        self.edit_box_set()
        self.button_set()


    def thread_control(self, event):
        self.t = threading.Thread(target=self.start_server)
        self.t.start()

    def button_set(self):
        self.button1 = wx.Button(self.start_windows, size=(330, 80), pos=(250, 610), label='启动服务端', name='button')
        self.button1.Bind(wx.EVT_BUTTON, self.thread_control)

    def title_set(self):
        self.title = wx.StaticText(self.start_windows, size=(355, 33), pos=(160, 6), label='服务端', name='staticText',
                                   style=2321)
        title_font = wx.Font(22, 74, 90, 400, False, 'Microsoft YaHei UI', 28)
        self.title.SetFont(title_font)

    def edit_box_set(self):
        self.HOST_box = wx.TextCtrl(self.start_windows, size=(157, 28), pos=(63, 615), value='127.0.0.1', name='text',
                                    style=0)
        self.PORT_box = wx.TextCtrl(self.start_windows, size=(155, 29), pos=(65, 656), value='6666', name='text',
                                    style=0)
        self.message_box = wx.TextCtrl(self.start_windows, size=(540, 530), pos=(59, 68), value='欢迎打开服务端软件',
                                       name='text',
                                       style=wx.TE_READONLY|wx.TE_WORDWRAP|wx.TE_MULTILINE)
        self.message_box.SetFont(wx.Font(11, 74, 90, 400, False, 'Microsoft YaHei UI', 28))

    def start_server(self):
        self.HOST = self.HOST_box.GetValue()
        self.PORT = int(self.PORT_box.GetValue())
        if not self.check_ip(self.HOST):
            self.update_message("IP地址不合法，请重新输入")
            return


        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.HOST, self.PORT))
            self.server.listen(5)
        except socket.error as msg:
            self.update_message(msg)
            return

        self.update_message('({}:{})等待连接......'.format(self.HOST, self.PORT))
        self.wait_conn()

    def wait_conn(self):
        while True:
            conn, addr = self.server.accept()
            t = threading.Thread(target=self.deal_data, args=(conn, addr))
            t.start()

    def deal_data(self, conn, addr):
        # self.TCPIP_conn(conn,addr)
        self.update_message('有一个新连接： {}'.format(addr))
        conn.send(('你好，欢迎连接服务器').encode())
        self.update_message(('({}:{}) 服务器发送消息：你好，欢迎连接服务器'.format(self.HOST, self.PORT)))

        while True:
            try:
                data = conn.recv(1024)
            except ConnectionResetError:
                self.update_message("{}断开连接".format(addr))
                return

            data_recv = str(data.decode())
            msg_recv,check_code_recv = unpack_msg(data_recv)


            if msg_decode(msg_recv) == 'error':
                msg_recv = msg_recv[:-1]

            print('{:10}:{}'.format('源字符串',data_recv))
            print('{:9}:{}'.format('其中消息字符串',msg_recv))


            check_code_solve = CRC([int(i) for i in msg_recv]).get_check_code()

            print('{:10}:{}'.format('收到的CRC码',check_code_recv))
            print('{:10}:{}'.format('验算的的CRC码',check_code_solve))

            if check_code_recv == check_code_solve:
                print('{:10}:{}\n'.format('解码后', msg_decode(msg_recv)))
                self.update_message('{}\n{} 客户端发送消息： {}'.format(time.asctime(time.localtime(time.time())),
                                                            addr,msg_decode(msg_recv)))
                flag = True
            else:
                self.update_message("消息验证出错")
                flag = False


            time.sleep(1)
            if data.decode() == 'exit' or not data:
                conn.send('连接关闭!'.encode())
                self.update_message('{} 连接关闭!'.format(addr))
                break


            if flag:
                # goto: 添加字符串判定功能
                conn.send('消息验证成功, {}'.format(msg_decode(msg_recv)).encode())
            else:
                conn.send('消息验证出错'.format(msg_decode(msg_recv)).encode())

        conn.close()

    def update_message(self, new_msg):
        msg = self.message_box.GetValue()
        new_msg = str(new_msg)
        self.message_box.SetValue('\n\n'.join([msg, new_msg]))


    def check_ip(self, HOST):
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
            '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if compile_ip.match(HOST):
            return True
        else:
            return False

    def message_check(self, msg):
        pass


class myApp(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True


def main():
    app = myApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
