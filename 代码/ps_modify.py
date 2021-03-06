# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ps_modify.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(524, 541)
        Form.setMinimumSize(QtCore.QSize(524, 541))
        Form.setMaximumSize(QtCore.QSize(524, 541))
        Form.setStyleSheet("")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 521, 541))
        self.groupBox.setStyleSheet("QGroupBox {\n"
"border:1px solid rgb(217, 217, 217);\n"
"}")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(80, 30, 381, 41))
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btn_check = QtWidgets.QPushButton(self.groupBox)
        self.btn_check.setGeometry(QtCore.QRect(130, 470, 93, 28))
        self.btn_check.setStyleSheet("background-color: rgb(194, 170, 255,200);\n"
"")
        self.btn_check.setObjectName("btn_check")
        self.btn_modify = QtWidgets.QPushButton(self.groupBox)
        self.btn_modify.setGeometry(QtCore.QRect(300, 470, 93, 28))
        self.btn_modify.setStyleSheet("background-color: rgb(194, 170, 255,200);\n"
"")
        self.btn_modify.setObjectName("btn_modify")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 70, 451, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_id = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_id.setStyleSheet("background-color: rgb(255, 255, 255,120);")
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.gridLayout.addWidget(self.lineEdit_id, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_name.setStyleSheet("background-color: rgb(248, 250, 255,120);")
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 1, 1, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(QtCore.QRect(40, 170, 451, 281))
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255,60);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label_2.setBuddy(self.lineEdit_id)
        self.label_3.setBuddy(self.lineEdit_name)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_id, self.lineEdit_name)
        Form.setTabOrder(self.lineEdit_name, self.tableWidget)
        Form.setTabOrder(self.tableWidget, self.btn_check)
        Form.setTabOrder(self.btn_check, self.btn_modify)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "修改信息"))
        self.label.setText(_translate("Form", "请输入您想要修改员工信息的工号以及姓名"))
        self.btn_check.setText(_translate("Form", "查询"))
        self.btn_modify.setText(_translate("Form", "修改"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"right\">工 号：</p></body></html>"))
        self.lineEdit_id.setPlaceholderText(_translate("Form", "请输入10位数字的员工工号"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"right\">姓 名：</p></body></html>"))
        self.lineEdit_name.setPlaceholderText(_translate("Form", "请输入员工的姓名"))
