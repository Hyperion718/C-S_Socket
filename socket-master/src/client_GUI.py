# -*- coding: UTF-8 -*-
'''
@Time : 2021/5/17 13:20
@Author : Silicon-He
@File : client.py
@Software: PyCharm
'''
import random
import wx
import socket
import threading
import time
from en_decoder import *
import datetime
import re
from concurrent.futures import ThreadPoolExecutor, wait


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='客户端', size=(630, 820), name='frame', style=541072896)
        try:
            icon = wx.Icon(r'./ico.jpg')
            self.SetIcon(icon)
        except:
            print("没找到图标图像 ./ico.jpg")
        self.start_windows = wx.Panel(self)
        self.start_windows.SetOwnBackgroundColour((240, 240, 240, 255))
        self.Centre()
        self.label_set()
        self.edit_box_set()
        self.button_set()
        self.spinctrl_set()
        self.open_port = []
        self.is_conn = False
        self.is_scan = False

    def spinctrl_set(self):
        self.tar_PORT_box = wx.SpinCtrl(self.start_windows, size=(114, 27), pos=(90, 557), name='wxSpinCtrl', min=0,
                                        max=65535, initial=6666, style=0)
        self.tar_PORT_box.SetBase(10)

        self.PORT_box = wx.SpinCtrl(self.start_windows, size=(114, 27), pos=(90, 645), name='wxSpinCtrl', min=0,
                                    max=65535, initial=random.randint(0, 65535), style=0)
        self.PORT_box.SetBase(10)

        self.scan_down_box = wx.SpinCtrl(self.start_windows, size=(60, 27), pos=(220, 557), name='wxSpinCtrl', min=0,
                                        max=65535, initial=4000, style=0)
        self.scan_down_box.SetBase(10)

        self.scan_up_box = wx.SpinCtrl(self.start_windows, size=(60, 27), pos=(290, 557), name='wxSpinCtrl', min=0,
                                    max=65535, initial=8000, style=0)
        self.scan_up_box.SetBase(10)

    def button_set(self):
        self.button_conn = wx.Button(self.start_windows, size=(150, 77), pos=(210, 600), label='连接', name='button')
        self.button_conn.SetFont(wx.Font(12, 74, 90, 400, False, 'Microsoft YaHei UI', 28))
        self.button_conn.Bind(wx.EVT_BUTTON, self.client_conn)

        self.button_disconn = wx.Button(self.start_windows, size=(150, 77), pos=(380, 600), label='断开连接', name='button')
        self.button_disconn.SetFont(wx.Font(12, 74, 90, 400, False, 'Microsoft YaHei UI', 28))
        self.button_disconn.Bind(wx.EVT_BUTTON, self.client_disconn)

        self.button_send_message = wx.Button(self.start_windows, size=(120, 75), pos=(410, 687), label='发送消息',
                                             name='button')
        self.button_send_message.SetFont(wx.Font(12, 74, 90, 400, False, 'Microsoft YaHei UI', 28))
        self.button_send_message.Bind(wx.EVT_BUTTON, self.send_message)

        self.button_port_scan = wx.Button(self.start_windows, size=(150, 77), pos=(380, 510), label='端口扫描',
                                          name='button')
        self.button_port_scan.SetFont(wx.Font(12, 74, 90, 400, False, 'Microsoft YaHei UI', 28))
        self.button_port_scan.Bind(wx.EVT_BUTTON, self.start_port_scan)

    def label_set(self):
        self.label_title = wx.StaticText(self.start_windows, size=(362, 38), pos=(125, 14), label='客户端',
                                         name='staticText', style=2321)
        self.label_title.SetFont(wx.Font(15, 74, 90, 400, False, 'Microsoft YaHei UI', 28))

        self.tar_HOST_label = wx.StaticText(self.start_windows, size=(70, 25), pos=(10, 520), label='目标HOST',
                                            name='staticText', style=2321)
        self.tar_HOST_label.SetFont(wx.Font(9, 74, 90, 400, False, 'Microsoft YaHei UI', 28))

        self.tar_PORT_label = wx.StaticText(self.start_windows, size=(70, 25), pos=(10, 565), label='目标PORT',
                                            name='staticText', style=2321)
        self.tar_PORT_label.SetFont(wx.Font(9, 74, 90, 400, False, 'Microsoft YaHei UI', 28))

        self.HOST_label = wx.StaticText(self.start_windows, size=(70, 25), pos=(10, 610), label='自身HOST',
                                        name='staticText', style=2321)
        self.HOST_label.SetFont(wx.Font(9, 74, 90, 400, False, 'Microsoft YaHei UI', 28))

        self.PORT_label = wx.StaticText(self.start_windows, size=(70, 25), pos=(10, 650), label='自身PORT',
                                        name='staticText', style=2321)
        self.PORT_label.SetFont(wx.Font(9, 74, 90, 400, False, 'Microsoft YaHei UI', 28))

        self.PORT_label = wx.StaticText(self.start_windows, size=(150, 40), pos=(210, 515), label='端口扫描范围：',
                                        name='staticText', style=2321)
        self.PORT_label.SetFont(wx.Font(11, 74, 90, 400, False, 'Microsoft YaHei UI', 28))

    def edit_box_set(self):
        self.message_box = wx.TextCtrl(self.start_windows, size=(493, 440), pos=(51, 56), value='欢迎打开客户端软件',
                                       name='text', style=wx.TE_READONLY|wx.TE_WORDWRAP|wx.TE_MULTILINE)
        self.message_box.ShowPosition(self.message_box.GetLastPosition())


        self.message_box.SetFont(wx.Font(11, 74, 90, 400, False, 'Microsoft YaHei UI', 28))

        self.tar_HOST_box = wx.TextCtrl(self.start_windows, size=(112, 26), pos=(90, 514), value='127.0.0.1',
                                        name='text',style=0)

        self.send_box = wx.TextCtrl(self.start_windows, size=(350, 77), pos=(42, 685), value='', name='text',
                                    style=1073741856)

        self.HOST_box = wx.TextCtrl(self.start_windows, size=(112, 26), pos=(90, 605), value='127.0.0.1', name='text',
                                    style=0)


    def client_conn(self, event):
        self.HOST = self.HOST_box.GetValue()
        self.PORT = self.PORT_box.GetValue()
        self.tar_HOST = self.tar_HOST_box.GetValue()
        self.tar_PORT = self.tar_PORT_box.GetValue()
        if self.is_conn:
            self.update_message('已处于连接状态，请勿重复连接')
            return
        elif self.is_scan:
            self.update_message("扫描端口状态中，请勿连接")
            return
        elif not self.check_ip(self.tar_HOST):
            self.update_message("目标IP不合法，请重新输入")
            return
        elif not  self.check_ip(self.HOST):
            self.update_message("自身IP不合法，请重新输入")
            return

        else:
            self.is_conn = True

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.bind((self.HOST, int(self.PORT)))
            self.client.connect((self.tar_HOST, int(self.tar_PORT)))

        except socket.error as msg:
            self.update_message(msg)
            self.is_conn = False

        t1 = threading.Thread(target=self.recv_msg)
        t1.start()

    def recv_msg(self):
        while 1:
            try:
                msg = self.client.recv(1024)
                self.update_message('{}\n({}:{})从服务器收到消息：{}'.format(time.asctime(time.localtime(time.time())),
                                                                self.tar_HOST,
                                                                self.tar_PORT,
                                                                str(msg.decode())))
            except:
                break


    def client_disconn(self, event):
        if self.is_conn:
            self.client.close()
            self.update_message("已断开连接")
            self.is_conn = False
        else:
            self.update_message("客户端并未处于连接状态")

    def send_message(self, event):
        if not self.is_conn:
            self.update_message("没有连接主机，无法发送消息")
            return
        send_msg = self.send_box.GetValue()
        if send_msg == '':
            return

        print('原消息：           ', send_msg)
        send_msg = check_msg(send_msg)
        print('转义后消息：        ', send_msg)
        send_msg = msg_encode(send_msg)

        if len(send_msg) > 948:  # 消息长度限制可以修改 默认1024-12-64
            self.update_message('消息过长无法发送！0.0')
            return

        print('Unicode消息：      ', send_msg)
        send_msg = crc_encode(send_msg)
        print('crc校验后消息：     ', send_msg)
        send_msg = package_msg(send_msg)
        print('发送头尾校验码后消息：', send_msg, '\n')
        if send_msg != '':
            self.client.send(send_msg.encode())
            self.send_box.Clear()


    def start_port_scan(self, event):
        self.tar_HOST = self.tar_HOST_box.GetValue()
        self.scan_up = self.scan_up_box.GetValue()
        self.scan_down = self.scan_down_box.GetValue()
        self.HOST = self.HOST_box.GetValue()

        if self.is_conn:
            self.update_message("连接状态下不能进行端口扫描")
            return
        elif not self.check_ip(self.tar_HOST):
            self.update_message("目标IP不合法，请重新输入")
            return
        elif not  self.check_ip(self.HOST):
            self.update_message("自身IP不合法，请重新输入")
            return
        elif self.scan_up <= self.scan_down:
            self.update_message("请让左边数字小于右边")
            return
        else:
            self.is_scan = True

        try:
            while True:
                if self.check_ip(self.tar_HOST):
                    start_time = datetime.datetime.now()
                    executor = ThreadPoolExecutor(max_workers=600)  #启动600个子线程同时进行扫描
                    t = [executor.submit(self.port_scan, self.tar_HOST, n) for n in range(self.scan_down, self.scan_up)]
                    if wait(t, return_when='ALL_COMPLETED'):
                        end_time = datetime.datetime.now()
                        break
            self.update_message('以下端口处于打开状态：\n'+','.join(self.open_port))
            self.update_message("扫描完成,用时:{}s".format(str((end_time - start_time).seconds)))
            self.open_port = []

        except Exception as e:
            self.update_message(str(e)+'端口扫描失败')

        finally:
            self.is_scan = False



    def port_scan(self, HOST, PORT):
        s = socket.socket()
        try:
            s.settimeout(0.2)
            s.connect((HOST, PORT))
            print('{:5}端口打开'.format(PORT))
            self.open_port.append(str(PORT))
        except Exception as e:
            pass
        finally:
            s.close()


    def check_ip(self, HOST):
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
            '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if compile_ip.match(HOST):
            return True
        else:
            return False


    def update_message(self, new_msg):
        msg = self.message_box.GetValue()
        new_msg = str(new_msg)
        self.message_box.SetValue('\n\n'.join([msg, new_msg]))


class myApp(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True


if __name__ == '__main__':
    app = myApp()
    app.MainLoop()
