# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'msg.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(681, 581)
        Form.setMinimumSize(QtCore.QSize(681, 581))
        Form.setMaximumSize(QtCore.QSize(681, 581))
        Form.setStyleSheet("QFrame  {\n"
"    background-image: url();\n"
"}\n"
"QWidget  {\n"
"border-image:url();\n"
"}\n"
"QLabel {\n"
"border-image:url();\n"
"}\n"
"QPushButton {\n"
"border-image:url();\n"
"}\n"
"QLineEdit {\n"
"border-image:url();\n"
"}\n"
"")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 661, 571))
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setGeometry(QtCore.QRect(10, 20, 641, 541))
        self.splitter.setStyleSheet("")
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setMinimumSize(QtCore.QSize(111, 541))
        self.frame.setMaximumSize(QtCore.QSize(111, 541))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 70, 95, 341))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_show = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_show.setStyleSheet("background-color: rgb(194, 170, 255,200);\n"
"")
        self.btn_show.setObjectName("btn_show")
        self.verticalLayout.addWidget(self.btn_show)
        self.btn_insert = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_insert.setStyleSheet("background-color: rgb(194, 170, 255,200);\n"
"")
        self.btn_insert.setObjectName("btn_insert")
        self.verticalLayout.addWidget(self.btn_insert)
        self.btn_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_delete.setStyleSheet("background-color: rgb(194, 170, 255,200);\n"
"")
        self.btn_delete.setObjectName("btn_delete")
        self.verticalLayout.addWidget(self.btn_delete)
        self.btn_modify = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_modify.setStyleSheet("background-color: rgb(194, 170, 255,200);\n"
"")
        self.btn_modify.setObjectName("btn_modify")
        self.verticalLayout.addWidget(self.btn_modify)
        self.btn_query = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_query.setStyleSheet("background-color: rgb(194, 170, 255,200);\n"
"")
        self.btn_query.setObjectName("btn_query")
        self.verticalLayout.addWidget(self.btn_query)
        self.frame_2 = QtWidgets.QFrame(self.splitter)
        self.frame_2.setStyleSheet("QFrame  {\n"
"    background-image: url();\n"
"}\n"
"QWidget  {\n"
"border-image:url();\n"
"}\n"
"QLabel {\n"
"border-image:url();\n"
"}\n"
"QPushButton {\n"
"border-image:url();\n"
"}\n"
"QLineEdit {\n"
"border-image:url();\n"
"}\n"
"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "??????????????????"))
        self.btn_show.setText(_translate("Form", "????????????"))
        self.btn_insert.setText(_translate("Form", "????????????"))
        self.btn_delete.setText(_translate("Form", "????????????"))
        self.btn_modify.setText(_translate("Form", "????????????"))
        self.btn_query.setText(_translate("Form", "????????????"))
