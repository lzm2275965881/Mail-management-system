import os.path
import sys
import threading

from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog, QDialog, QTextEdit, QWidget

from Address_Book_Window import Ui_Address_Book_Window
from Forwarding_Window import Ui_Forwarding_Window
from SendEmail import mailSocket
from Lib.share import SharedInfo
from Login_Window import Ui_Login_Window
from Main_Window import Ui_Main_Window
from SendEmail_Window import Ui_SendEmail_Window
from ConfirmDeletion_Window import Ui_ConfirmDeletion_Window
from ReceiveBox_Window import *
from ReceiveEmail import *
from imbox import Imbox
import base64
import smtplib
import socket
import ssl
import re
import string


class Win_Login(QDialog): #初始化登陆窗口

    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Login_Window()
        self.ui.setupUi(self)

    def MailSocket(self): #这里判断登陆是否成功
        Username = SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip()
        Password = SharedInfo.Login_Window.ui.edt_Authorization.text().strip()
        print(Password)
        if '@qq.com' in Username or '@sina.com' in Username or '@163.com' in Username or '@126.com' in Username:
            mailserver = ('smtp.' + Username[Username.index('@') + 1:], 465)  # 根据用户名判断端口
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sslclientSocket = ssl.wrap_socket(clientSocket, cert_reqs=ssl.CERT_NONE,
                                              ssl_version=ssl.PROTOCOL_SSLv23)
            print('连接中.........')
            sslclientSocket.connect(mailserver)
            recv = sslclientSocket.recv(1024).decode('utf-8')
            if recv[:3] != '220':
                print('连接失败， 重新连接')
                mailSocket()
            print(recv)  # 220 smtp.qq.com Esmtp QQ Mail Server
            print('连接成功..........')

            # 服务器响应
            sslclientSocket.send(b'HELO qq.com\r\n')
            recv = sslclientSocket.recv(1024).decode()
            print(recv)  # 250 smtp.qq.com
            # 发送登录请求
            sslclientSocket.send(b'AUTH login\r\n')
            recv2 = sslclientSocket.recv(1024).decode('utf-8')
            print(recv2)  # 334 VXNlcm5hbWU6
            # 开始登陆

            username = b'%s\r\n' % base64.b64encode(Username.encode('utf-8'))
            password = b'%s\r\n' % base64.b64encode(Password.encode('utf-8'))
            sslclientSocket.send(username)
            recv = sslclientSocket.recv(1024).decode('utf-8')
            print('username = ', recv)  # 334 UGFzc3dvcmQ6
            sslclientSocket.send(password)
            recv = sslclientSocket.recv(1024).decode()
            print('password = ', recv)  # 235 Authentication successful
        else:
            recv = []
            recv[:3] = '0'
        if Username == '123' and Password == '123':
            Win_Login.ChangeToMain(self)  # 超级用户
        else:
            if recv[:3] == '235':
                Win_Login.ChangeToMain(self)  # 如果登陆成功，则执行窗口转换
            else:
                SharedInfo.Login_Window.ui.Welcome.setText('账号或授权码有误，请重新登录！') #如果登陆失败则给出提示

    def ChangeToMain(self): #转换窗口到主窗口
        SharedInfo.Main_Window.ui.label_username.setText(SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip())
        SharedInfo.Main_Window.show()
        SharedInfo.Login_Window.close() #关闭登陆窗口

class Win_Main(QMainWindow): #初始化主窗口
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Main_Window()
        self.ui.setupUi(self)

    def ChangeToSend(self):
        SharedInfo.SendEmail_Window.show() #打开发送邮件窗口

    def ChangToReceive(self):
        SharedInfo.ReceiveBox_Window = Win_Receive()
        SharedInfo.ReceiveBox_Window.show()
        t1 = threading.Thread(target=SharedInfo.ReceiveBox_Window.Receive) #线程
        t1.start() #线程开始
        SharedInfo.ReceiveBox_Window.ui.btn_forwardthis.clicked.connect(Win_Receive.ChangeToForward)

    def ChangeToAddress(self):
        SharedInfo.Address_Book_Window = Win_Address_Book()
        SharedInfo.Address_Book_Window.show() #打开通讯录窗口

class Win_Send(QMainWindow): #初始化发送窗口
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SendEmail_Window()
        self.ui.setupUi(self)

    def Send(self): #调用发送功能
        mailSocket(SharedInfo.SendEmail_Window.ui.edt_Receiver.text().strip(), #接收者
                      SharedInfo.SendEmail_Window.ui.edt_HeadLine.text().strip(), #主题
                      SharedInfo.SendEmail_Window.ui.edt_MainText.toPlainText().strip(), #大文本框获取内容的方式不同
                      SharedInfo.SendEmail_Window.ui.edt_Receiver_2.text().strip(),  # 附件地址
                      SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip(), #用户名
                      SharedInfo.Login_Window.ui.edt_Authorization.text().strip()) #授权码
        # SharedInfo.SendEmail_Window.ui.edt_Receiver.clear()
        # SharedInfo.SendEmail_Window.ui.edt_HeadLine.clear()
        # SharedInfo.SendEmail_Window.ui.edt_MainText.clear()
        # SharedInfo.SendEmail_Window.ui.edt_Receiver_2.clear()
class Win_Receive(QDialog):
    def __init__(self): #点击了收件箱之后就开始获取邮件信息
        QDialog.__init__(self)
        self.ui = Ui_ReceiveBox_Window()
        self.ui.setupUi(self) #初始化收件箱窗口

    def Receive(self):
        #self.ui.btn_delete.clicked.connect(Win_Receive.ChangeToConfirm)
        global delete_signal
        delete_signal = 0
        with Imbox('imap.' + SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip()[
                             SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip().index('@') + 1:],
                   SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip(),
                   SharedInfo.Login_Window.ui.edt_Authorization.text().strip(), ssl=True) as imbox:

            # imap服务器地址，邮箱，密码，是否支持s
            self.all_email = imbox.messages() #获取所有邮件
            self.title = {}#标题
            self.text = {}#正文
            self.sent_from = {}#发件人
            self.date = {}#日期
            self.attachments = {}  # 附件
            i = 0
            for uid, message in self.all_email:
                try:#过滤掉不合理的邮件
                    j = 1
                    temp = message.subject
                    while True: #用来判断是否有重复的标题，并进行区分
                        if temp in self.title.keys():
                            temp = message.subject + '_' + str(j)#重复的标题会有编号
                            j += 1
                        else:
                            message.subject = temp
                            break
                    self.title[message.subject] = i #标题_i作为key，i作为值
                    self.text[str(i)] = message.body #i作为key，文本作为值
                    self.sent_from[str(i)] = message.sent_from #发件人
                    self.date[str(i)] = message.date #日期
                    self.attachments[str(i)] = message.attachments  # 附件
                    print('正在获取邮件中，请稍后 ' + str(i+1) + '/' + str(len(self.all_email)))
                    self.ui.view_list.insertItem(0, message.subject)
                    i += 1
                except AttributeError as e:
                    self.date[str(i)] = 'None'
                    self.attachments[str(i)] = []
                    print('正在获取邮件中，请稍后 ' + str(i + 1) + '/' + str(len(self.all_email)))
                    self.ui.view_list.insertItem(0, message.subject)
                    i += 1
            self.qList = list(self.title.keys())
            self.qList.reverse()
        self.ui.view_list.itemSelectionChanged.connect(self.Show) #改变鼠标点击可显示对应的邮件信息
        self.ui.btn_delete.clicked.connect(self.ChangeToConfirm)#点击删除调用确认删除函数
        self.ui.btn_download.clicked.connect(self.Download)#点击下载附件调用下载函数
        subject, text, sent_from, date, attachments, emailcount = Receive_Email(
            SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip(),
            SharedInfo.Login_Window.ui.edt_Authorization.text().strip()
        )
        count = emailcount #记录当前邮件的数量
        while True: #一直循环
            try:
                subject, text, sent_from, date, attachments, emailcount = Receive_Email(
                    SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip(),
                    SharedInfo.Login_Window.ui.edt_Authorization.text().strip()
                )
            except UnboundLocalError as e:
                attachments = []
            if count >= emailcount: #如果邮件数量未增加则进行下一轮循环
                count = emailcount
                continue
            count = emailcount #记录新的邮件数
            j = 1
            while True:
                if subject in self.title.keys():
                    subject = subject + '_' + str(j)
                    j += 1
                else:
                    break
            self.qList.insert(0, subject) #将新的邮件标题存入列表首端
            self.title[subject] = emailcount-1 #将标题存入字典
            self.text[str(emailcount-1)] = text #将正文存入字典
            self.sent_from[str(emailcount-1)] = sent_from #将发件人存入字典
            self.date[str(emailcount-1)] = date  #将日期存入字典
            #if self.attachments.get(str(emailcount-1):
            self.attachments[str(emailcount-1)] = attachments # 将附件存入字典
            #else:
                #pass
            self.ui.view_list.insertItem(0, self.qList[0]) #将新邮件的标题显示在文本框内
    def Show(self): #用来显示选中的邮件信息
        self.current = self.ui.view_list.selectedItems()
        self.i = self.title.get(self.current[0].text())
        global delete_row
        delete_row = self.ui.view_list.currentRow()#记录需要删除的邮件在文本框中的行数
        global delete_index
        delete_index = self.current[0].text()#记录需要删除的邮件的题目
        global selected #全局变量取到之后需要用到的转发邮件信息
        plain = self.text.get(str(self.i))['plain']
        html = self.text.get(str(self.i))['html']
        if self.text.get(str(self.i))['plain']:  # plain不为空
            result1 = re.findall('<' + '(.*?)' + '>', plain[0])  # 下面这几行用来解析邮件，去掉非文本内容
            for i in range(len(result1)):
                if '<a' in '<' + result1[i] + '>' or 'a>' in '<' + result1[i] + '>':
                    plain[0] = plain[0].replace('<' + result1[i] + '>', ' ')  # 去掉<...>（换行）的内容
                else:
                    plain[0] = plain[0].replace('<' + result1[i] + '>', '\n')
            result2 = re.findall('&' + '(.*?)' + ';', plain[0])
            for i in range(len(result2)):
                plain[0] = plain[0].replace('&' + result2[i] + ';', ' ')  # 去掉$...;（空格）的内容
            selected = '标题：' + self.current[0].text() + '\n发件人昵称：' + str(self.sent_from.get(str(self.i))[0]['name']) + \
                       '\n' + '发件人邮箱：' + str(self.sent_from.get(str(self.i))[0]['email']) + \
                       '\n日期：' + self.date.get(str(self.i)) + \
                       '\n正文：\n' + plain[0]  # f"{str(self.text.get(str(self.i))['plain'][0])}" + '\n'
            # + 'html： ' + f"{str(self.text.get(str(self.i))['html'])}"
        else:  # plain为空
            result1 = re.findall('<' + '(.*?)' + '>', html[0])
            for i in range(len(result1)):
                if '<a' in '<' + result1[i] + '>' or 'a>' in '<' + result1[i] + '>':
                    html[0] = html[0].replace('<' + result1[i] + '>', ' ')
                else:
                    html[0] = html[0].replace('<' + result1[i] + '>', '\n')
            result2 = re.findall('&' + '(.*?)' + ';', html[0])
            for i in range(len(result2)):
                html[0] = html[0].replace('&' + result2[i] + ';', ' ')
            selected = '标题：' + self.current[0].text() + '\n发件人昵称：' + str(self.sent_from.get(str(self.i))[0]['name']) + \
                       '\n' + '发件人邮箱：' + str(self.sent_from.get(str(self.i))[0]['email']) + \
                       '\n日期：' + self.date.get(str(self.i)) + \
                       '\n正文：\n' + html[0]  # f"{str(self.text.get(str(self.i))['html'][0])}"
        if self.attachments.get(str(self.i)):  # 此处单纯在文本框内展示是否有附件
            # path1 = os.path.abspath('.')  # 表示当前所处的文件夹的绝对路径
            # print('绝对路径path1= ', path1)
            att = []
            for attachment in self.attachments.get(str(self.i)):
                att.append(attachment['filename'])  # 显示多个附件的名称
                a = ' '.join(att)
            self.ui.view_attname.setText(a)  # 显示附件名称
        else:
            self.ui.view_attname.setText('没有附件')
        if self.text.get(str(self.i))['plain']:  # plain不为空
            result1 = re.findall('<' + '(.*?)' + '>', plain[0])
            for i in range(len(result1)):
                if '<a' in '<' + result1[i] + '>' or 'a>' in '<' + result1[i] + '>':
                    plain[0] = plain[0].replace('<' + result1[i] + '>', ' ')
                else:
                    plain[0] = plain[0].replace('<' + result1[i] + '>', '\n')
            result2 = re.findall('&' + '(.*?)' + ';', plain[0])
            for i in range(len(result2)):
                plain[0] = plain[0].replace('&' + result2[i] + ';', ' ')
            self.ui.view_information.setText(
                '标题：' + self.current[0].text() + '\n发件人昵称：' + str(self.sent_from.get(str(self.i))[0]['name']) +
                '\n' + '发件人邮箱：' + str(self.sent_from.get(str(self.i))[0]['email']) +
                '\n日期：' + self.date.get(str(self.i)) +
                '\n正文：\n' + plain[0])  # f"{str(self.text.get(str(self.i))['plain'][0])}" + '\n')
            # + 'html： ' + f"{str(self.text.get(str(self.i))['html'])}") #将选中邮件的信息显示出来
        else:  # plain为空
            result1 = re.findall('<' + '(.*?)' + '>', html[0])
            for i in range(len(result1)):
                if '<a' in '<' + result1[i] + '>' or 'a>' in '<' + result1[i] + '>':
                    html[0] = html[0].replace('<' + result1[i] + '>', ' ')
                else:
                    html[0] = html[0].replace('<' + result1[i] + '>', '\n')
            result2 = re.findall('&' + '(.*?)' + ';', html[0])
            for i in range(len(result2)):
                html[0] = html[0].replace('&' + result2[i] + ';', ' ')
            self.ui.view_information.setText(
                '标题：' + self.current[0].text() + '\n发件人昵称：' + str(self.sent_from.get(str(self.i))[0]['name']) +
                '\n' + '发件人邮箱：' + str(self.sent_from.get(str(self.i))[0]['email']) +
                '\n日期：' + self.date.get(str(self.i)) +
                '\n正文：\n'  # + f"{str(self.text.get(str(self.i))['plain'][0])}" + '\n')
                + html[0])  #f"{str(self.text.get(str(self.i))['html'])}") #将选中邮件的信息显示出来
    def Download(self):#下载附件函数
        if self.attachments.get(str(self.i)):
            path1 = os.path.abspath('.')  # 表示当前所处的文件夹的绝对路径
            #print('绝对路径path1= ', path1)
            for attachment in self.attachments.get(str(self.i)):
                with open(attachment['filename'].replace('?', ''), 'wb') as f: #此处去掉可能存在的乱码问号
                    path = self.ui.attadress.text().strip()
                    f.write(attachment['content'].getvalue())
                    f.close()
                    if path != path1 :
                     shutil.move(os.path.realpath(attachment['filename'].replace('?', '')), path)
        else:
            pass
    def ChangeToForward(self):
            SharedInfo.Forwarding_Window = Win_Forwarding()  # 实例化转发窗口
            SharedInfo.Forwarding_Window.show()
            global forward_message  # 全局变量，转发邮件信息
            forward_message = '--------转发邮件信息--------\n' + str(selected)  # 编辑一下转发的邮件信息
            SharedInfo.Forwarding_Window.ui.edt_forwarding.setText(forward_message)  # 将需要转发的邮件信息显示在文本框内
            SharedInfo.Forwarding_Window.ui.btn_forward.clicked.connect(Win_Forwarding.ForwardSend)  # 点击转发按键触发事件

    def ChangeToConfirm(self):
            SharedInfo.ConfirmDeletion_Window = Win_ConfirmDeletion()  # 实例化确认删除的窗口
            SharedInfo.ConfirmDeletion_Window.show()
            SharedInfo.ConfirmDeletion_Window.ui.btn_no.clicked.connect(
                SharedInfo.ConfirmDeletion_Window.close)  # 点击否会直接关闭窗口
            SharedInfo.ConfirmDeletion_Window.ui.btn_yes.clicked.connect(self.Delete)  # 点击'是'会调用Delete

    def Delete(self):
        try:
            i = self.title.get(delete_index)  # 根据标题得到邮件的索引
            self.qList.remove(delete_index)  # 更新qList列表
            self.title.pop(delete_index)  # 更新title字典
            self.text.pop(str(i))  # 更新text字典
            self.sent_from.pop(str(i))  # 更新sent_from字典
            self.date.pop(str(i))  # 更新date字典
            if self.attachments.get(str(self.i)):
              self.attachments.pop(str(i))  # 更新attachments字典
            else:
                pass
            with Imbox('imap.' + SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip()[
                                 SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip().index('@') + 1:],
                       SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip(),
                       SharedInfo.Login_Window.ui.edt_Authorization.text().strip(), ssl=True) as imbox2:

                all_email = imbox2.messages()
                imbox2.delete(all_email[i][0])  # 删掉选中的邮件，服务器中的邮件也删除了
            self.ui.view_list.removeItemWidget(self.ui.view_list.takeItem(delete_row))  # 在文本框中去掉对应的邮件
            SharedInfo.ConfirmDeletion_Window.close()  # 关闭窗口
        except TypeError as e:
            pass

class Win_Forwarding(QWidget):
        def __init__(self):
            QWidget.__init__(self)
            self.ui = Ui_Forwarding_Window()
            self.ui.setupUi(self)

        def ForwardSend(self):  # 真正的将邮件转发出去
            mailSocket(
                SharedInfo.Forwarding_Window.ui.edt_receiver.text().strip(),  # 接收者
                SharedInfo.Forwarding_Window.ui.edt_theme.text().strip(),  # 主题
                SharedInfo.Forwarding_Window.ui.edt_text.toPlainText().strip() + '\n\n\n\n' + forward_message,
                # 邮件信息与编辑的正文合并
                ' ', #转发邮件不含附件
                SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip(),  # 用户名
                SharedInfo.Login_Window.ui.edt_Authorization.text().strip())  # 授权码

class Win_Address_Book(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_Address_Book_Window()
        self.ui.setupUi(self)
        #功能键分别对应五个调用程序
        self.ui.Btn_Delete.clicked.connect(self.Delete)  # 点击删除调用确认删除函数
        self.ui.Btn_add.clicked.connect(self.Add)  # 点击添加联系人调用添加联系人函数
        self.ui.Btn_name_motify.clicked.connect(self.Name_Motify)  # 点击修改名字调用修改名字函数
        self.ui.Btn_email_motify.clicked.connect(self.Email_Motify)  # 点击修改邮箱调用修改邮箱函数
        self.ui.Btn_Send.clicked.connect(self.ChangeToSend)  # 点击发送调用确认发送函数

        #以下初始化窗口，显示读取的通讯录
        Path='.\\Address_Book\\Address_Book.txt'
        f = open(Path,'r',encoding='utf-8')#只是读取显示
        lines = f.readlines()
        for line in lines:
            #line = line.decode('gbk').encode('utf-8')
            line = line.strip('\n')
            self.ui.listWidget_Address.insertItem(0,line)
        f.close()

    def Add(self):#增加部分已完成，文件窗口中都可以
        Path = '.\\Address_Book\\Address_Book.txt'
        f = open(Path, 'a+', encoding='utf-8')  # a叫做追加写入模式，只可以在末尾追加内容，不可以读取
        f.write(self.ui.Edit_name_add.text()+' '+self.ui.Edit_email_add.text()+'\n')#直接写入名字和邮箱
        f.close()
        self.ui.listWidget_Address.insertItem(0, self.ui.Edit_name_add.text()+' '+self.ui.Edit_email_add.text())

        #f.write(self.textEdit.toPlainText() + '\n')
        #f.write(self.lineEdit.text() + '\n')
    def Name_Motify(self):
        name=[]
        email=[]
        Path = '.\\Address_Book\\Address_Book.txt'
        current_row = self.ui.listWidget_Address.currentRow()  # 记录选中的联系人在文本框中的行数
        count_row = self.ui.listWidget_Address.count()
        f = open(Path, 'r',encoding='utf-8')#读通讯录，只是显示
        lines = f.readlines()#读取所有的联系人，以列表形式显示
        line= lines.pop(count_row - current_row - 1)#相当于先删除掉这一行，这里是被删除掉的行
        current_line=line.strip().split(" ")#进行空格取数据串
        name.append(current_line[0])
        email.append(current_line[1])#分别读取要修改的名字和邮箱，形成数组
        self.ui.listWidget_Address.removeItemWidget(self.ui.listWidget_Address.takeItem(current_row))  # 在文本框中去掉对应的联系人
        f.close()
        print('修改前',name)
        print('邮箱',email)
        print('邮箱str', email[0])
        f = open(Path, 'w+',encoding='utf-8')#允许写入，覆盖
        f.writelines(lines)#第一步，完成删除改选定行
        f.close()
        print('donedeletename')
        f = open(Path, 'a+', encoding='utf-8')  # a叫做追加写入模式，只可以在末尾追加内容，不可以读取
        f.write(self.ui.Edit_name_motify.text() + ' ' +email[0]+ '\n')  # 直接写入名字和邮箱
        self.ui.listWidget_Address.insertItem(0, self.ui.Edit_name_motify.text() + ' ' + email[0])  # 直接补充在最上面
        f.close()
        print('doneaddname')
    def Email_Motify(self):
        name = []
        email = []
        Path = '.\\Address_Book\\Address_Book.txt'
        current_row = self.ui.listWidget_Address.currentRow()  # 记录选中的联系人在文本框中的行数

        count_row = self.ui.listWidget_Address.count()
        f = open(Path, 'r', encoding='utf-8')  # 读通讯录，只是显示
        lines = f.readlines()  # 读取所有的联系人，以列表形式显示
        line = lines.pop(count_row - current_row - 1)  # 相当于先删除掉这一行，这里是被删除掉的行
        current_line = line.strip().split(" ")  # 进行空格取数据串
        name.append(current_line[0])
        email.append(current_line[1])  # 分别读取要修改的名字和邮箱，形成数组
        f.close()
        print('修改前', name)
        print('邮箱str', email[0])
        f = open(Path, 'w+', encoding='utf-8')  # 允许写入，覆盖
        f.writelines(lines)  # 第一步，完成删除改选定行
        self.ui.listWidget_Address.removeItemWidget(self.ui.listWidget_Address.takeItem(current_row))  # 在文本框中去掉对应的联系人
        f.close()
        print('donedeleteemail')
        f = open(Path, 'a+', encoding='utf-8')  # a叫做追加写入模式，只可以在末尾追加内容，不可以读取
        f.write(name[0] + ' ' + self.ui.Edit_email_motify.text() + '\n')  # 直接写入名字和邮箱
        self.ui.listWidget_Address.insertItem(0, name[0] + ' ' + self.ui.Edit_email_motify.text())  # 直接补充在最上面
        f.close()
        print('doneaddemail')
        print(name[0] + ' ' + self.ui.Edit_email_motify.text() + '\n')
    def ChangeToSend(self):
        #SharedInfo.SendEmail_Window = Win_Send()  # 实例化发送窗口
        SharedInfo.SendEmail_Window.show()
        global address_message  # 全局变量，选定的联系人的邮箱
            #对于读取用户选定的信息，单纯的pop出而不写入并不会影响本地文件
        name = []
        email = []
        Path = '.\\Address_Book\\Address_Book.txt'
        current_row = self.ui.listWidget_Address.currentRow()  # 记录选中的联系人在文本框中的行数
        count_row = self.ui.listWidget_Address.count()
        f = open(Path, 'r', encoding='utf-8')  # 读通讯录，只是显示
        lines = f.readlines()  # 读取所有的联系人，以列表形式显示
        line = lines.pop(count_row - current_row - 1)  # 读取选定的联系人行
        current_line = line.strip().split(" ")  # 进行空格取数据串
        name.append(current_line[0])
        email.append(current_line[1])  # 分别读取要修改的名字和邮箱，形成数组
        f.close()
        address_message =email[0] # 读取需要发送的邮箱，str
        SharedInfo.SendEmail_Window.ui.edt_Receiver.setText(address_message)  # 将需要转发的邮件信息显示在文本框内

            #完成发送邮件


    # def Address_Send(self):
    #         current_row = self.ui.listWidget_Address.currentRow()  # 记录需要发送的联系人在文本框中的行数
    #         count_row = self.ui.listWidget_Address.count()
    #         Path = '.\\Address_Book\\Address_Book.txt'
    #         f = open(Path, 'r', encoding='utf-8')  # 只是读取显示
    #         lines = f.readlines()
    #         line_Send= lines.pop(count_row - current_row - 1)#用pop出具体选择的row,send
    #         Send=line_Send.strip().split(" ")#用空格键分出列表
    #         print(Send)#已经正确打印出列表中的名字和邮箱
    #         Send_Email=[]
    #         Send_Email.append(Send[1])
    #         print(Send_Email)#输出的是字符串
    #         SharedInfo.Main_Window.ui.Btn_Send.clicked.connect(Win_Main.ChangeToSend)
    #         #SharedInfo.SendEmail_Window.ui.edt_Receiver.text().strip()=lines_Send[1]#选择对应row的email
    #         mailSocket(SharedInfo.SendEmail_Window.ui.edt_Receiver.text().strip()==Send_Email,  # 接收者
    #                    SharedInfo.SendEmail_Window.ui.edt_HeadLine.text().strip(),  # 主题
    #                    SharedInfo.SendEmail_Window.ui.edt_MainText.toPlainText().strip(),  # 大文本框获取内容的方式不同
    #                    SharedInfo.SendEmail_Window.ui.edt_Receiver_2.text().strip(),  # 附件地址
    #                    SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip(),  # 用户名
    #                    SharedInfo.Login_Window.ui.edt_Authorization.text().strip())  # 授权码

    def Delete(self):#可以正常删除，文本框中和本地文件中都可以
        delete_row = self.ui.listWidget_Address.currentRow()  # 记录需要删除的联系人在文本框中的行数
        count_row=self.ui.listWidget_Address.count()
        print(count_row)
        print(delete_row)
        self.ui.listWidget_Address.removeItemWidget(self.ui.listWidget_Address.takeItem(delete_row))  # 在文本框中去掉对应的联系人
        Path = '.\\Address_Book\\Address_Book.txt'
        f = open(Path, 'r', encoding='utf-8')  # 只是读取显示
        lines = f.readlines()
        lines_new=lines.pop(count_row-delete_row-1)
        print(count_row-delete_row-1)
        print(lines)
        print(lines_new)
        f.close()
        f = open(Path, 'w+',encoding='utf-8')#允许写入，覆盖
        f.writelines(lines)
        f.close()

class Win_ConfirmDeletion(QWidget):
        def __init__(self):
            QWidget.__init__(self)
            self.ui = Ui_ConfirmDeletion_Window()
            self.ui.setupUi(self)

if __name__ == '__main__':
        app = QApplication(sys.argv)
        SharedInfo.Login_Window = Win_Login()  # 实例化登陆窗口
        SharedInfo.Main_Window = Win_Main()  # 实例化主窗口
        SharedInfo.SendEmail_Window = Win_Send()  # 实例化发送邮件窗口
        SharedInfo.Login_Window.ui.btn_Login.clicked.connect(Win_Login.MailSocket)  # 登陆窗口点击登陆之后，调出主窗口，并关闭登陆窗口
        SharedInfo.Main_Window.ui.btn_sendemail.clicked.connect(Win_Main.ChangeToSend)  # 主窗口点击发送邮件后，跳出发送邮件的窗口
        #SharedInfo.Address_Book_Window.ui.Btn_Send.clicked.connect(Win_Main.ChangeToSend)  # 通讯录点击发送邮件后，跳出发送邮件的窗口
        SharedInfo.Main_Window.ui.btn_receivebox.clicked.connect(Win_Main.ChangToReceive)  # 主窗口点击收件箱后，弹出收件箱窗口
        SharedInfo.Main_Window.ui.btn_adressbook.clicked.connect(Win_Main.ChangeToAddress)  # 主窗口点击通讯录后，跳出通讯录的窗口
        SharedInfo.SendEmail_Window.ui.btn_Send.clicked.connect(Win_Send.Send)  # 在发送邮件窗口编辑好文本之后，点击发送将文本发送出去
        SharedInfo.Login_Window.show()  # 显示登陆界面
        sys.exit(app.exec_())
