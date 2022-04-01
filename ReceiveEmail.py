import imaplib
import email
# 此函数通过使用imaplib实现接收邮件
from PyQt5.QtCore import QStringListModel
from numpy.compat import unicode
from imbox import Imbox
import keyring
from imbox import Imbox
import os
import shutil
import yagmail



def Receive_Email(email_address, email_password):
    # 要进行邮件接收的邮箱。改成自己的邮箱
    #email_address = "2275965881@qq.com"
    # 要进行邮件接收的邮箱的密码。改成自己的邮箱的密码
    #email_password = "vcsfrkvrgvrfebcf"
    # 邮箱对应的imap服务器，也可以直接是IP地址
    # 改成自己邮箱的imap服务器；qq邮箱不需要修改此值
    #imap_server_host = "imap.qq.com"
    # 邮箱对应的pop服务器的监听端口。改成自己邮箱的pop服务器的端口；qq邮箱不需要修改此值
    imap_server_port = 993
    with Imbox('imap.' + email_address[email_address.index('@') + 1:], email_address, email_password,
               ssl=True) as imbox:
        # imap服务器地址，邮箱，密码，是否支持s
        try:
            all_email = imbox.messages()
            email_count = len(all_email)
            subject = str(all_email[email_count - 1][1].subject)
            text = all_email[email_count - 1][1].body
            sent_from = all_email[email_count - 1][1].sent_from
            date = str(all_email[email_count - 1][1].date)
            attachment = all_email[email_count - 1][1].attachments
        except AttributeError as e:
            date = 'None'
            attachment = []
        # except UnboundLocalError as u:
        # attachment = ['']
    return subject, text, sent_from, date, attachment, email_count

# def parseBody(message):
#     """ 解析邮件/信体 """
#     # 循环信件中的每一个mime的数据块
#     for part in message.walk():
#         # 这里要判断是否是multipart，是的话，里面的数据是一个message 列表
#         if not part.is_multipart():
#             charset = part.get_charset()
#             # print 'charset: ', charset
#             contenttype = part.get_content_type()
#             # print 'content-type', contenttype
#             name = part.get_param("name")  # 如果是附件，这里就会取出附件的文件名
#             if name:
#                 # 有附件
#                 # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
#                 fh = email.Header.Header(name)
#                 fdh = email.Header.decode_header(fh)
#                 fname = fdh[0][0]
#                 #print('附件名:', fname)
#                 #attach_data = part.get_payload(decode=True) #　解码出附件数据，然后存储到文件中
#
#                 #try:
#                      #f = open(fname, 'wb') #注意一定要用wb来打开文件，因为附件一般都是二进制文件
#                 #except:
#                      #print ('附件名有非法字符，自动换一个')
#                      #f = open('aaaa', 'wb')
#                 #f.write(attach_data)
#                 #f.close()
#             else:
#                 # 不是附件，是文本内容
#                 return part.get_payload(decode=True).decode('gbk')
#                 # pass
#             # print '+'*60 # 用来区别各个部分的输出
#
#
# def parseHeader(message):
#     """ 解析邮件首部 """
#     subject = message.get('subject')
#     h = email.header.Header(subject)
#     dh = email.header.decode_header(h)
#     subject = unicode(dh[0][0], dh[0][1]).encode('gb2312')
#
#     return subject, email.utils.parseaddr(message.get('from'))[1]
#
# def GetList(email_address,email_password):
#     print('ok2')
#     with Imbox('imap.qq.com', email_address, email_password, ssl=True) as imbox:
#         # imap服务器地址，邮箱，密码，是否支持s
#         all_mails = imbox.messages()
#         email_count = len(all_mails)
#         # imbox.delete(all_mails[160][0]) #删除QQ邮箱中收到的第161封邮件
#         # 读取收件箱所有信息
#         # List = {}
#         # i = 0
#         # for uid, messages in all_mails:
#         #     if i != 0:
#         #         List[email_count-i-1] = messages.subject
#         #         i += 1
#     print('ok3')
#     return all_mails
#             #print(messages.date)
#               #输出邮件主题
#              #print(messages.body['plain'])
#             #输出邮件内容以文本格式