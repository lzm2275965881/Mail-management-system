# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login_Window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette,QBrush,QPixmap


class Ui_Login_Window(object):
    def setupUi(self, Login_Window):

        Login_Window.setObjectName("Login_Window")
        Login_Window.resize(768, 432)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(".\Background.jpg")))
        Login_Window.setPalette(palette)
        #Login_Window.setStyleSheet("background-image:url(Background.jpg)")


        self.label = QtWidgets.QLabel(Login_Window)
        self.label.setGeometry(QtCore.QRect(450, 100, 61, 31))
        self.label.setObjectName("label")


        self.edt_AccountNumber = QtWidgets.QLineEdit(Login_Window)
        self.edt_AccountNumber.setGeometry(QtCore.QRect(540, 100, 121, 31))
        self.edt_AccountNumber.setObjectName("edt_AccountNumber")

        self.Welcome = QtWidgets.QLabel(Login_Window)
        self.Welcome.setGeometry(QtCore.QRect(440, 220, 240, 31))

        #font = QtGui.QFont()
        #font.setPointSize(15)
        #font.setBold(True)
        #font.setWeight(75)

        #self.Welcome.setFont(font)
        self.Welcome.setObjectName("Welcome")
        self.Welcome.setStyleSheet("""
        color:white;
        padding-left: 10px;
        padding-right: 10px;
        padding-top: 1px;
        padding-bottom: 1px;
        border:1px solid #0073df;
        border-radius:5px;
       
    """)

        # self.label_2 = QtWidgets.QLabel(Login_Window)
        # self.label_2.setGeometry(QtCore.QRect(450, 160, 61, 31))
        # self.label_2.setObjectName("label_2")

        self.btn_Login = QtWidgets.QPushButton(Login_Window)
        self.btn_Login.setGeometry(QtCore.QRect(480, 280, 131, 31))
        self.btn_Login.setObjectName("btn_Login")
        self.btn_Login.setStyleSheet("""
                padding-left: 10px;
                padding-right: 10px;
                padding-top: 1px;
                padding-bottom: 1px;
                border:1px solid #0073df;
                border-radius:5px;
                background:  # 6633FF;
            """)


        # self.edt_Password = QtWidgets.QLineEdit(Login_Window)
        # self.edt_Password.setGeometry(QtCore.QRect(540, 160, 121, 31))
        # self.edt_Password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.edt_Password.setObjectName("edt_Password")

        self.label_3 = QtWidgets.QLabel(Login_Window)
        self.label_3.setGeometry(QtCore.QRect(450, 160, 61, 31))
        self.label_3.setObjectName("label_3")

        self.edt_Authorization = QtWidgets.QLineEdit(Login_Window)
        self.edt_Authorization.setGeometry(QtCore.QRect(540, 160, 121, 31))
        self.edt_Authorization.setObjectName("edt_Authorization")

        self.retranslateUi(Login_Window)
        QtCore.QMetaObject.connectSlotsByName(Login_Window)

    def retranslateUi(self, Login_Window):
        _translate = QtCore.QCoreApplication.translate
        Login_Window.setWindowTitle(_translate("Login_Window", "登陆"))
        self.label.setText(_translate("Login_Window", "账号："))
        self.edt_AccountNumber.setPlaceholderText(_translate("Login_Window", "用户名"))
        self.Welcome.setText(_translate("Login_Window", "请输入您的账号和授权码"))
        #self.label_2.setText(_translate("Login_Window", "密码："))
        self.btn_Login.setText(_translate("Login_Window", "登陆"))
        #self.edt_Password.setPlaceholderText(_translate("Login_Window", "密码"))
        self.label_3.setText(_translate("Login_Window", "授权码："))
        self.edt_Authorization.setPlaceholderText(_translate("Login_Window", "授权码"))
