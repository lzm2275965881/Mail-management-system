# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Address_Book_Window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Address_Book_Window(object):
    def setupUi(self, Address_Book_Window):
        Address_Book_Window.setObjectName("Address_Book_Window")
        Address_Book_Window.resize(960, 540)
        self.listWidget_Address = QtWidgets.QListWidget(Address_Book_Window)
        self.listWidget_Address.setGeometry(QtCore.QRect(32, 109, 314, 401))
        self.listWidget_Address.setObjectName("listWidget_Address")
        self.Edit_name_motify = QtWidgets.QLineEdit(Address_Book_Window)
        self.Edit_name_motify.setGeometry(QtCore.QRect(460, 120, 141, 21))
        self.Edit_name_motify.setObjectName("Edit_name_motify")
        self.Edit_email_motify = QtWidgets.QLineEdit(Address_Book_Window)
        self.Edit_email_motify.setGeometry(QtCore.QRect(460, 160, 141, 21))
        self.Edit_email_motify.setObjectName("Edit_email_motify")
        self.Edit_name_add = QtWidgets.QLineEdit(Address_Book_Window)
        self.Edit_name_add.setGeometry(QtCore.QRect(740, 120, 131, 21))
        self.Edit_name_add.setObjectName("Edit_name_add")
        self.Edit_email_add = QtWidgets.QLineEdit(Address_Book_Window)
        self.Edit_email_add.setGeometry(QtCore.QRect(740, 160, 131, 21))
        self.Edit_email_add.setObjectName("Edit_email_add")
        self.Btn_name_motify = QtWidgets.QPushButton(Address_Book_Window)
        self.Btn_name_motify.setGeometry(QtCore.QRect(390, 200, 111, 28))
        self.Btn_name_motify.setObjectName("Btn_name_motify")
        self.Btn_email_motify = QtWidgets.QPushButton(Address_Book_Window)
        self.Btn_email_motify.setGeometry(QtCore.QRect(520, 200, 111, 28))
        self.Btn_email_motify.setObjectName("Btn_email_motify")
        self.Btn_add = QtWidgets.QPushButton(Address_Book_Window)
        self.Btn_add.setGeometry(QtCore.QRect(730, 200, 141, 28))
        self.Btn_add.setObjectName("Btn_add")
        self.label_2 = QtWidgets.QLabel(Address_Book_Window)
        self.label_2.setGeometry(QtCore.QRect(410, 20, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(Address_Book_Window)
        self.label_4.setGeometry(QtCore.QRect(420, 120, 41, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Address_Book_Window)
        self.label_5.setGeometry(QtCore.QRect(420, 160, 41, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Address_Book_Window)
        self.label_6.setGeometry(QtCore.QRect(700, 120, 41, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Address_Book_Window)
        self.label_7.setGeometry(QtCore.QRect(700, 160, 41, 16))
        self.label_7.setObjectName("label_7")
        self.Btn_Delete = QtWidgets.QPushButton(Address_Book_Window)
        self.Btn_Delete.setGeometry(QtCore.QRect(680, 437, 231, 61))
        self.Btn_Delete.setText("")
        op = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(0.2)
        self.Btn_Delete.setGraphicsEffect(op)
        self.Btn_Delete.setObjectName("Btn_Delete")

        self.Btn_Send = QtWidgets.QPushButton(Address_Book_Window)
        self.Btn_Send.setGeometry(QtCore.QRect(400, 440, 231, 61))
        self.Btn_Send.setAutoFillBackground(False)
        self.Btn_Send.setText("")
        self.Btn_Send.setObjectName("Btn_Send")
        op2 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op2.setOpacity(0.2)
        self.Btn_Send.setGraphicsEffect(op2)
        self.Btn_Send.setGraphicsEffect(op2)
        self.label_8 = QtWidgets.QLabel(Address_Book_Window)
        self.label_8.setGeometry(QtCore.QRect(-7, -9, 971, 551))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("./Background5.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.label_8.raise_()
        self.Btn_Send.raise_()
        self.Btn_Delete.raise_()
        self.listWidget_Address.raise_()
        self.Edit_name_motify.raise_()
        self.Edit_email_motify.raise_()
        self.Edit_name_add.raise_()
        self.Edit_email_add.raise_()
        self.Btn_name_motify.raise_()
        self.Btn_email_motify.raise_()
        self.Btn_add.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()

        self.retranslateUi(Address_Book_Window)
        QtCore.QMetaObject.connectSlotsByName(Address_Book_Window)

    def retranslateUi(self, Address_Book_Window):
        _translate = QtCore.QCoreApplication.translate
        Address_Book_Window.setWindowTitle(_translate("Address_Book_Window", "Form"))
        self.Btn_name_motify.setText(_translate("Address_Book_Window", "修改姓名"))
        self.Btn_email_motify.setText(_translate("Address_Book_Window", "修改邮箱"))
        self.Btn_add.setText(_translate("Address_Book_Window", "增加联系人"))
        self.label_2.setText(_translate("Address_Book_Window", " "))
        self.label_4.setText(_translate("Address_Book_Window", "姓名"))
        self.label_5.setText(_translate("Address_Book_Window", "邮箱"))
        self.label_6.setText(_translate("Address_Book_Window", "姓名"))
        self.label_7.setText(_translate("Address_Book_Window", "邮箱"))
