import base64
import smtplib
import socket
import ssl
from email.mime.text import MIMEText
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from Lib.share import SharedInfo
from SendEmail_Window import Ui_SendEmail_Window


def mailSocket(receiver, subject, text, attachments, _username, _password):
    mailserver = ('smtp.qq.com', 465)
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

    username = b'%s\r\n' % base64.b64encode(_username.encode('utf-8'))
    password = b'%s\r\n' % base64.b64encode(_password.encode('utf-8'))
    sslclientSocket.send(username)
    recv = sslclientSocket.recv(1024).decode('utf-8')
    print('username = ', recv)  # 334 UGFzc3dvcmQ6
    sslclientSocket.send(password)
    recv = sslclientSocket.recv(1024).decode()
    print('password = ', recv)  # 235 Authentication successful
    if recv[:3] == '235':
        print('sslclientSocket = ', sslclientSocket)
        print('receiver = ', receiver)
        print('subject = ', subject)
        print('text = ', text)
        print('_username = ', _username)
        send(sslclientSocket, receiver, subject, text, _username,_password,attachments)


def send(sslclientSocket, receiver,subject, text, username,password,attachments):
    multiPart = MIMEMultipart()

    multiPart['From'] = username
    multiPart['To'] = ','.join(receiver)

    _subject = subject
    multiPart['Subject'] = Header(_subject, "utf-8")
    multiPart.attach(MIMEText(text, 'plain', 'utf-8'))
    if attachments != '':
      if os.path.exists(attachments):
        att1 = MIMEApplication(open(attachments, 'rb').read())
        print('att1 = ', att1)
        att1.add_header('Content-Disposition', 'attachment', filename=attachments)
        multiPart.attach(att1)
        SharedInfo.SendEmail_Window.ui.label_5.setText('附件地址正确，已发送')
        result = 1
      else:
        SharedInfo.SendEmail_Window.ui.label_5.setText('附件地址错误，请重试')
        result = 0




    smtp = smtplib.SMTP_SSL(host='smtp.qq.com', port=465)
    try:
        smtp.login(username, password)
        smtp.sendmail(username, receiver.split(','), multiPart.as_string())
    except smtplib.SMTPException as e:
        print("发送失败", e)
        SharedInfo.SendEmail_Window.ui.label_5.setText('发送失败，请检查收件人邮箱')
        result = 0
    else:
        print("发送成功")
        SharedInfo.SendEmail_Window.ui.label_5.setText('发送成功')
        result = 1


    # msgtype = b"Content-Type: multipart/mixed;boundary='BOUNDARY'\r\n\r\n"
    # msgboundary = b'--BOUNDARY\r\n'

    # sslclientSocket.send(b"Content-Type: multipart/mixed;boundary='BOUNDARY'\r\n\r\n")
    # sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
    # sslclientSocket.send(b'\r\n\r\n' + b'--BOUNDARY\r\n')
    #
    # sslclientSocket.send(b'Content-Type: text/html;charset=utf-8\r\n')
    # sslclientSocket.send(b'Content-Transfer-Encoding:7bit\r\n\r\n')
    # text = 'Hello, World, <h1 style="color:#c00">World</h1>'
    # _text = b'%s\r\n' % text.encode('utf-8')
    # sslclientSocket.send(_text)

    print('发送结束...')
    sslclientSocket.send(b'\r\n.\r\n')

    sslclientSocket.send(b'QUIT\r\n')
    if result == 1:
        SharedInfo.SendEmail_Window.ui.edt_Receiver.clear()
        SharedInfo.SendEmail_Window.ui.edt_HeadLine.clear()
        SharedInfo.SendEmail_Window.ui.edt_MainText.clear()
        SharedInfo.SendEmail_Window.ui.edt_Receiver_2.clear()
    else:
        pass

if __name__ == '__main__':
     mailSocket()


# def sendMailBySMTPlib(msg_from, password, msg_to, subject, content):
#     # msg_from = SharedInfo.Login_Window.ui.edt_AccountNumber.text().strip()  # 发送方邮箱地址。
#     # password = SharedInfo.Login_Window.ui.edt_Authorization.text().strip()  # 发送方QQ邮箱授权码，不是QQ邮箱密码。
#     # msg_to = SharedInfo.SendEmail_Window.ui.edt_Receiver.text().strip()  # 收件人邮箱地址。
#     #
#     # subject = SharedInfo.SendEmail_Window.ui.edt_HeadLine.text().strip()  # 主题。
#     # content = SharedInfo.SendEmail_Window.ui.edt_MainText.text().strip()  # 邮件正文内容。
#     msg = MIMEText(content, 'plain', 'utf-8')
#
#     msg['Subject'] = subject
#     msg['From'] = msg_from
#     msg['To'] = msg_to
#
#     try:
#         client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
#         print("连接到邮件服务器成功")
#
#         client.login(msg_from, password)
#         print("登录成功")
#
#         client.sendmail(msg_from, msg_to, msg.as_string())
#         print("发送成功")
#     except smtplib.SMTPException as e:
#         print("发送邮件异常")
#     finally:
#         client.quit()