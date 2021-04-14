# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_face.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(543, 348)
        Form.setMinimumSize(QtCore.QSize(543, 348))
        Form.setMaximumSize(QtCore.QSize(543, 348))
        Form.setStyleSheet("")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 551, 351))
        self.frame.setStyleSheet("QFrame {\n"
"border-image:url(:/lay/image/login1.png);\n"
"}\n"
"QLineEdit {\n"
"border-image:url();\n"
"}\n"
"QLabel {\n"
"border-image:url();\n"
"}\n"
"QPushButton {\n"
"border-image:url();\n"
"}\n"
"QCheckBox {\n"
"border-image:url();\n"
"}\n"
"QGridLayout {\n"
"border-image:url();\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.btn_facelogin = QtWidgets.QPushButton(self.frame)
        self.btn_facelogin.setGeometry(QtCore.QRect(300, 240, 99, 28))
        self.btn_facelogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_facelogin.setStyleSheet("QPushButton\n"
"{\n"
"    border-radius: 5px;\n"
"    background-color: rgb(85, 170, 255,200);\n"
"}")
        self.btn_facelogin.setObjectName("btn_facelogin")
        self.btn_login = QtWidgets.QPushButton(self.frame)
        self.btn_login.setGeometry(QtCore.QRect(150, 240, 99, 28))
        self.btn_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_login.setStyleSheet("QPushButton\n"
"{    \n"
"    border-radius: 5px;\n"
"    background-color: rgb(85, 170, 255,200);\n"
"}")
        self.btn_login.setObjectName("btn_login")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(151, 142, 60, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(150, 210, 147, 19))
        self.checkBox.setStyleSheet("")
        self.checkBox.setObjectName("checkBox")
        self.lineEdit_id = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_id.setGeometry(QtCore.QRect(219, 142, 181, 21))
        self.lineEdit_id.setStyleSheet("background-color: rgb(255, 255, 255, 100);")
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.lineEdit_pw = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_pw.setGeometry(QtCore.QRect(219, 173, 181, 21))
        self.lineEdit_pw.setStyleSheet("background-color: rgb(255, 255, 255, 100);")
        self.lineEdit_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_pw.setObjectName("lineEdit_pw")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(151, 173, 61, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(100, 50, 381, 51))
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_id, self.lineEdit_pw)
        Form.setTabOrder(self.lineEdit_pw, self.btn_login)
        Form.setTabOrder(self.btn_login, self.btn_facelogin)
        Form.setTabOrder(self.btn_facelogin, self.checkBox)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_facelogin.setText(_translate("Form", "人脸识别登录"))
        self.btn_login.setText(_translate("Form", "登 录"))
        self.label.setText(_translate("Form", "用户名："))
        self.checkBox.setText(_translate("Form", "记住用户名和密码"))
        self.lineEdit_id.setToolTip(_translate("Form", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.lineEdit_id.setPlaceholderText(_translate("Form", "请输入用户名"))
        self.lineEdit_pw.setPlaceholderText(_translate("Form", "请输入密码"))
        self.label_2.setText(_translate("Form", "密  码："))
        self.label_3.setText(_translate("Form", "欢迎来到员工管理系统"))
import aaa_rc
