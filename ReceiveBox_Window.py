# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReceiveBox_Window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ReceiveBox_Window(object):
    def setupUi(self, ReceiveBox_Window):
        ReceiveBox_Window.setObjectName("ReceiveBox_Window")
        ReceiveBox_Window.setEnabled(True)
        ReceiveBox_Window.resize(1344, 756)
        self.label = QtWidgets.QLabel(ReceiveBox_Window)
        self.label.setGeometry(QtCore.QRect(10, 90, 72, 15))
        self.label.setText("")
        self.label.setObjectName("label")
        self.view_information = QtWidgets.QTextBrowser(ReceiveBox_Window)
        self.view_information.setGeometry(QtCore.QRect(550, 148, 747, 373))
        self.view_information.setObjectName("view_information")
        self.view_list = QtWidgets.QListWidget(ReceiveBox_Window)
        self.view_list.setGeometry(QtCore.QRect(50, 158, 401, 352))
        self.view_list.setObjectName("view_list")
        self.btn_forwardthis = QtWidgets.QPushButton(ReceiveBox_Window)
        self.btn_forwardthis.setGeometry(QtCore.QRect(610, 530, 231, 30))
        self.btn_forwardthis.setObjectName("btn_forwardthis")
        self.btn_delete = QtWidgets.QPushButton(ReceiveBox_Window)
        self.btn_delete.setGeometry(QtCore.QRect(990, 530, 191, 30))
        self.btn_delete.setObjectName("btn_delete")
        self.label_3 = QtWidgets.QLabel(ReceiveBox_Window)
        self.label_3.setGeometry(QtCore.QRect(690, 660, 72, 15))
        self.label_3.setObjectName("label_3")
        self.btn_download = QtWidgets.QPushButton(ReceiveBox_Window)
        self.btn_download.setGeometry(QtCore.QRect(1110, 690, 100, 30))
        self.btn_download.setObjectName("btn_download")
        self.label_4 = QtWidgets.QLabel(ReceiveBox_Window)
        self.label_4.setGeometry(QtCore.QRect(690, 700, 131, 16))
        self.label_4.setObjectName("label_4")
        self.attadress = QtWidgets.QLineEdit(ReceiveBox_Window)
        self.attadress.setGeometry(QtCore.QRect(830, 690, 261, 31))
        self.attadress.setObjectName("attadress")
        self.view_attname = QtWidgets.QTextBrowser(ReceiveBox_Window)
        self.view_attname.setGeometry(QtCore.QRect(780, 650, 511, 31))
        self.view_attname.setObjectName("view_attname")
        self.label_5 = QtWidgets.QLabel(ReceiveBox_Window)
        self.label_5.setEnabled(True)
        self.label_5.setGeometry(QtCore.QRect(0, 0, 1351, 761))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("./Background4.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_5.raise_()
        self.label.raise_()
        self.view_information.raise_()
        self.view_list.raise_()
        self.btn_forwardthis.raise_()
        self.btn_delete.raise_()
        self.label_3.raise_()
        self.btn_download.raise_()
        self.label_4.raise_()
        self.attadress.raise_()
        self.view_attname.raise_()

        self.retranslateUi(ReceiveBox_Window)
        QtCore.QMetaObject.connectSlotsByName(ReceiveBox_Window)

    def retranslateUi(self, ReceiveBox_Window):
        _translate = QtCore.QCoreApplication.translate
        ReceiveBox_Window.setWindowTitle(_translate("ReceiveBox_Window", "收件箱"))
        self.btn_forwardthis.setText(_translate("ReceiveBox_Window", "转发该邮件"))
        self.btn_delete.setText(_translate("ReceiveBox_Window", "删除"))
        self.label_3.setText(_translate("ReceiveBox_Window", "附件名称："))
        self.btn_download.setText(_translate("ReceiveBox_Window", "下载附件"))
        self.label_4.setText(_translate("ReceiveBox_Window", "请输入下载地址："))