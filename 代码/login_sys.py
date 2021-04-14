# coding=gbk
# -*- coding: utf-8 -*-
import sys,os
import login_face
import mw_sys
import msg
import id_amin
import face_admin
import ps_show
import ps_insert
import ad_insert
import ps_delete
import ad_delete
import ps_modify
import ad_psw_modify
import ad_msg_modify
import ps_query
import ad_query
import face_rec
import face_train
import face_recognition
import Fe_record
import Fe_train
import Fe_recognition
import Fe_login
import pymysql
import shutil
import logging
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg


class fe_recognition(qw.QWidget, face_recognition.Ui_Form):   #创建人脸识别系统嵌套窗口类
    def __init__(self):
        super().__init__()
        InitUi(self)
        # 初始化
        self.is_check = 0  # 0为未查询，1为已查询
        # 绑定信号与槽
        self.btn_recognition.clicked.connect(self.btn_recognition_cb)
        self.btn_show.clicked.connect(self.btn_show_cb)
        con_mysql(self)  # 连接数据库
    def btn_show_cb(self):
        print("you clicked btn_show.")
        cur = self.cur
        self.sql1 = "select * from pes_show"
        cur.execute(query=self.sql1)
        total1 = cur.fetchall()
        if (len(total1) == 0):  # or len(total2)==0
            qw.QMessageBox.information(self, '提示', '暂未录入员工信息！', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self, total1, self.tableWidget_pes)
        self.sql2 = "select * from ad_show"
        cur.execute(query=self.sql2)
        total2 = cur.fetchall()
        if (len(total2) == 0):
            qw.QMessageBox.information(self, '提示', '暂未录入管理信息！', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self, total2, self.tableWidget_ad)
    def btn_recognition_cb(self):
        print("you clicked btn_recognition.")
        if (self.is_check == 1):
            self.is_check = 0
            self.w_face_train = Fe_recognition.Fe_recognition()
            self.w_face_train.show()
        else:
            qw.QMessageBox.information(self, '提示', '请先点击查询确认该员工或账号是否存在！', qw.QMessageBox.Ok)


class fe_train(qw.QWidget, face_train.Ui_Form):   #创建人脸训练系统嵌套窗口类
    def __init__(self):
        super().__init__()
        InitUi(self)
        # 初始化
        self.is_check = 0 # 0为未查询，1为已查询
        # 绑定信号与槽
        self.btn_train.clicked.connect(self.btn_train_cb)
        self.btn_show.clicked.connect(self.btn_show_cb)
        con_mysql(self) #连接数据库
    def btn_show_cb(self):
        print("you clicked btn_show.")
        cur = self.cur
        self.sql1 = "select * from pes_show"
        cur.execute(query=self.sql1)
        total1 = cur.fetchall()
        if (len(total1) == 0 ):#or len(total2)==0
            qw.QMessageBox.information(self, '提示', '暂未录入员工信息！', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self,total1,self.tableWidget_pes)
        self.sql2 = "select * from ad_show"
        cur.execute(query=self.sql2)
        total2 = cur.fetchall()
        if (len(total2) == 0):
            qw.QMessageBox.information(self, '提示', '暂未录入管理信息！', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self, total2, self.tableWidget_ad)
    def btn_train_cb(self):
        print("you clicked btn_train.")
        if (self.is_check == 1):
            self.is_check = 0
            self.w_face_train = Fe_train.Fe_train()
            self.w_face_train.show()
            # self.w_face_train.re_table(self.sql)
        else:
            qw.QMessageBox.information(self, '提示', '请先点击查询确认该员工或账号是否存在！', qw.QMessageBox.Ok)

class fe_record(qw.QWidget, face_rec.Ui_Form):   #创建人脸采集系统嵌套窗口类
    def __init__(self):
        super().__init__()
        InitUi(self)
        # 初始化界面
        self.radioButton_psid.setChecked(True)  # 初始选工号查询
        self.is_select = 0  # 0为工号查询，1为账号查询
        self.is_check = 0 # 0为未查询，1为已查询
        # 绑定信号与槽
        self.btn_record.clicked.connect(self.btn_record_cb)
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.radioButton_adid.toggled.connect(self.radioButton_adid_cb)
        self.radioButton_psid.toggled.connect(self.radioButton_psid_cb)
        con_mysql(self) #连接数据库
    def btn_check_cb(self):
        print("you clicked btn_check.")
        cur = self.cur
        id_name = self.lineEdit.text()
        if (self.is_select == 0):
            self.sql = "select * from pes_show where 工号 = '" + id_name + "'"
        else:
            self.sql = "select * from ad_show where  账号 = '" + id_name + "'"
        cur.execute(query=self.sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '提示', '该员工或账号不存在,请重新输入！', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self,total,self.tableWidget)
    def btn_record_cb(self):
        print("you clicked btn_record.")
        if(self.is_check == 1):
            self.is_check = 0
            self.w_face_rec = Fe_record.Fe_record()
            self.w_face_rec.show()
            self.w_face_rec.re_table(self.sql)
        else:
            qw.QMessageBox.information(self, '提示', '请先点击查询确认该员工或账号是否存在！', qw.QMessageBox.Ok)
    def radioButton_adid_cb(self):
        print("you select the id_check.")
        self.is_select=1
    def radioButton_psid_cb(self):
        print("you select the name_check.")
        self.is_select=0


class adm_query(qw.QWidget, ad_query.Ui_Form):   #创建管理员信息查询类
    def __init__(self):
        super().__init__()
        InitUi(self)
        # 绑定信号与槽
        self.btn_check.clicked.connect(self.btn_check_cb)
        con_mysql(self) #连接数据库
    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        sql = "select * from ad_show where 账号 = '" + id + "' "
        cur.execute(query=sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '提示', '该账号不存在,请重新输入！', qw.QMessageBox.Ok)
        else:
            table_build(self,total,self.tableWidget)


class pes_query(qw.QWidget, ps_query.Ui_Form):   #创建员工信息查询类
    def __init__(self):
        super().__init__()
        InitUi(self)
        # 初始化界面
        self.radioButton_id.setChecked(True)  # 初始选工号查询
        self.is_select = 0  #0为工号查询，1为姓名查询
        # 绑定信号与槽
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.radioButton_id.toggled.connect(self.radioButton_id_cb)
        self.radioButton_name.toggled.connect(self.radioButton_name_cb)
        con_mysql(self) #连接数据库
    def radioButton_id_cb(self):
        print("you select the id_check.")
        self.is_select=0
    def radioButton_name_cb(self):
        print("you select the name_check.")
        self.is_select=1
    def btn_check_cb(self):
        cur = self.cur
        id_name =self.lineEdit.text()
        if(self.is_select==0):
            sql = "select * from pes_show where 工号 = '" + id_name + "'"
        else:
            sql = "select * from pes_show where  姓名 = '" + id_name + "'"
        cur.execute(query=sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '提示', '该员工不存在,请重新输入！', qw.QMessageBox.Ok)
        else:
            table_build(self,total,self.tableWidget)

class adm_msg_modify(qw.QWidget, ad_msg_modify.Ui_Form):   #创建管理员信息修改类
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.is_check = 0  # 默认0为未查询
        # 绑定信号与槽
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_modify.clicked.connect(self.btn_modify_cb)
        con_mysql(self) #连接数据库
    def btn_modify_cb(self):
        reply = qw.QMessageBox.question(self, '提示', '是否确认修改?', qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            if (self.is_check == 1):
                self.is_check = 0
                cur = self.cur
                id = self.tableWidget.item(0, 0).text()
                name = self.tableWidget.item(0, 1).text()
                number = self.tableWidget.item(0, 3).text()
                phone = self.tableWidget.item(0, 4).text()
                section = self.tableWidget.item(0, 5).text()
                position = self.tableWidget.item(0, 6).text()
                sql = "update ad_show set " \
                      "姓名 = '" + name + "',身份证='" + number + "',电话='" + phone + "',部门='" + section + "'," \
                                                                                                     "职务='" + position + "'WHERE 账号='" + id + "'"
                cur.execute(sql)
                self.connection.commit()
                qw.QMessageBox.information(self, '提示', '修改成功！', qw.QMessageBox.Ok)
            else:
                qw.QMessageBox.information(self, '提示', '请先点击查询确认该账号是否存在！', qw.QMessageBox.Ok)

    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        sql = "select * from ad_show where 账号 = '" + id + "'"
        cur.execute(query=sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '提示', '账号不存在，请重新输入！', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self,total,self.tableWidget)

class adm_psw_modify(qw.QWidget, ad_psw_modify.Ui_Form):   #创建管理员账号密码修改类
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.is_check = 0 #默认0为未查询
        # 绑定信号与槽
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_modify.clicked.connect(self.btn_modify_cb)
        con_mysql(self) #连接数据库
    def btn_modify_cb(self):
        reply = qw.QMessageBox.question(self, '提示', '是否确认修改?', qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            if (self.is_check == 1):
                self.is_check = 0
                cur = self.cur
                id = self.tableWidget.item(0, 0).text()
                password = self.tableWidget.item(0, 1).text()
                cur.execute("update admin set 密码= '" + password + "'WHERE 账号 = '" + id + "'")
                self.connection.commit()
                qw.QMessageBox.information(self, '提示', '修改成功！', qw.QMessageBox.Ok)
            else:
                qw.QMessageBox.information(self, '提示', '请先点击查询确认改账号是否存在！', qw.QMessageBox.Ok)

    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        password = self.lineEdit_psw.text()
        sql =" select * from admin where 账号='" + id + "'and 密码='" + password + "'"
        cur.execute(query=sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '提示', '账号不存在或密码错误！', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self,total,self.tableWidget)

class pes_modify(qw.QWidget, ps_modify.Ui_Form):   #创建员工信息修改类
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.is_check = 0 #默认0为未查询
        # 绑定信号与槽
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_modify.clicked.connect(self.btn_modify_cb)
        con_mysql(self)
    def btn_modify_cb(self):
        reply = qw.QMessageBox.question(self, '提示', '是否确认修改?', qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            if(self.is_check==1):
                self.is_check=0
                cur = self.cur
                id = self.tableWidget.item(0,0).text()
                name = self.tableWidget.item(0,1).text()
                sex = self.tableWidget.item(0,3).text()
                phone = self.tableWidget.item(0,4).text()
                number = self.tableWidget.item(0,5).text()
                section = self.tableWidget.item(0,6).text()
                position = self.tableWidget.item(0,7).text()
                place = self.tableWidget.item(0,8).text()
                edu = self.tableWidget.item(0,9).text()
                note = self.tableWidget.item(0,10).text()
                sql = "update pes_show set" \
                      " 姓名='" + name + "',性别='" + sex + "',电话='" + phone + "',身份证='" + number + "',部门='" + section \
                      + "',职务='" + position + "',籍贯='" + place + "',学历='" + edu + "',备注='" + note + "'WHERE 工号='" + id + "'"
                cur.execute(sql)
                self.connection.commit()
                qw.QMessageBox.information(self, '提示', '修改成功！', qw.QMessageBox.Ok)
            else:
                qw.QMessageBox.information(self, '提示', '请先点击查询确认改员工是否存在！', qw.QMessageBox.Ok)
    def btn_check_cb(self):
        try:
            cur = self.cur
            id = self.lineEdit_id.text()
            name = self.lineEdit_name.text()
            sql = "select * from pes_show where 工号 = '" + id + "' and 姓名 = '" + name + "'"  # ,姓名 = '" + name + "'
            cur.execute(query=sql)
            total = cur.fetchall()
            if (len(total) == 0):
                qw.QMessageBox.information(self, '提示', '该员工不存在,请确认工号是否与姓名相对应！', qw.QMessageBox.Ok)
            else:
                self.is_check = 1
                table_build(self,total,self.tableWidget)
        except:
            qw.QMessageBox.information(self, '提示', '请确认工号是否与姓名相对应！', qw.QMessageBox.Ok)


class adm_delete(qw.QWidget, ad_delete.Ui_Form):   #创建管理员信息删除类
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.datasets = './datasets'    #当前存放人脸数据的位置
        self.isCheck = 0  # 默认0为未查询及删除，1为已查询
        # 绑定信号与槽
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_delete.clicked.connect(self.btn_delete_cb)
        con_mysql(self) #连接数据库
    def btn_delete_cb(self):
        text = '从数据库中删除该用户，同时删除相应人脸数据，<font color=red>该操作不可逆！</font>'
        informativeText = '<b>是否继续？</b>'
        reply = qw.QMessageBox.warning(self, "提示", text + informativeText, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                       qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            if (self.isCheck == 1):
                self.isCheck = 0
                cur = self.cur
                id = self.lineEdit_id.text()
                password = self.lineEdit_psw.text()
                cur.execute("DELETE FROM ad_show WHERE 账号 = '" + id + "'")
                cur.execute("DELETE FROM admin WHERE 账号 = '" + id + "'and 密码 = '" + password + "'")
                self.connection.commit()
                if os.path.exists('{}/stu_{}'.format(self.datasets, id)):
                    try:
                        shutil.rmtree('{}/stu_{}'.format(self.datasets, id))
                    except Exception as e:
                        logging.error('Error：系统删除人脸数据失败，请手动删除{}/stu_{}目录'.format(self.datasets, id))

                text = '你已成功删除账号为 <font color=blue>{}</font> 的用户记录。'.format(id)
                informativeText = '<b>请在人脸库重新训练人脸数据。</b>'
                qw.QMessageBox.information(self, "提示", text + informativeText, qw.QMessageBox.Ok)
                # 刷新前重置tableWidget
                self.lineEdit_id.clear()
                self.lineEdit_psw.clear()
                while self.tableWidget.rowCount() > 0: # 重置tableWidget
                    self.tableWidget.removeRow(0)
            else:
                qw.QMessageBox.information(self, '提示', '请先点击查询确认账号是否存在！', qw.QMessageBox.Ok)

    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        password = self.lineEdit_psw.text()
        sql = "select * from admin where 账号 = '" + id + "'and 密码 = '" + password + "'"
        cur.execute(query=sql)
        judge = cur.fetchall()
        if (len(judge) == 0):
            qw.QMessageBox.information(self, '提示', '该账号不存在或密码错误,请重新输入！', qw.QMessageBox.Ok)
        else:
            sql1 = "select * from ad_show where 账号 = '" + id + "'"
            cur.execute(sql1)
            total = cur.fetchall()
            if(len(total)==0):
                qw.QMessageBox.information(self, '提示', '账号不存在,请重新输入！', qw.QMessageBox.Ok)
            else:
                self.isCheck = 1
                table_build(self,total,self.tableWidget)

class pes_delete(qw.QWidget, ps_delete.Ui_Form):   #创建员工信息删除类
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.datasets = './datasets'    #当前存放人脸数据的位置
        #初始化变量
        self.isCheck = 0    #默认0为未查询及删除，1为已查询
        # 绑定信号与槽
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_delete.clicked.connect(self.btn_delete_cb)
        con_mysql(self) #连接数据库
    def btn_delete_cb(self):
        text = '从数据库中删除该用户，同时删除相应人脸数据，<font color=red>该操作不可逆！</font>'
        informativeText = '<b>是否继续？</b>'
        reply = qw.QMessageBox.warning(self, "提示",text+informativeText, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            if(self.isCheck==1):
                self.isCheck=0
                cur = self.cur
                id = self.lineEdit_id.text()
                name = self.lineEdit_name.text()
                cur.execute("DELETE FROM pes_show WHERE 工号 = '" + id + "'and 姓名 = '" + name + "'")
                self.connection.commit()
                # print('{}/stu_{}'.format(self.datasets, id))
                if os.path.exists('{}/stu_{}'.format(self.datasets, id)):
                    try:
                        shutil.rmtree('{}/stu_{}'.format(self.datasets, id))
                    except Exception as e:
                        logging.error('Error：系统删除人脸数据失败，请手动删除{}/stu_{}目录'.format(self.datasets, id))

                text = '你已成功删除工号为 <font color=blue>{}</font> 的用户记录。'.format(id)
                informativeText = '<b>请在人脸库重新训练人脸数据。</b>'
                qw.QMessageBox.information(self, "提示", text + informativeText,qw.QMessageBox.Ok)
                self.lineEdit_id.clear()
                self.lineEdit_name.clear()
                while self.tableWidget.rowCount() > 0: # 重置tableWidget
                    self.tableWidget.removeRow(0)
            else:
                qw.QMessageBox.information(self, '提示', '请先点击查询确认员工是否存在！', qw.QMessageBox.Ok)

    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        name = self.lineEdit_name.text()
        sql = "select * from pes_show where 工号 = '" + id + "' and 姓名 = '" + name + "'"#,姓名 = '" + name + "'
        cur.execute(query=sql)
        total = cur.fetchall()
        if(len(total)==0):
            qw.QMessageBox.information(self, '提示', '该员工不存在,请重新输入！', qw.QMessageBox.Ok)
        else:
            self.isCheck = 1
            table_build(self,total,self.tableWidget)

class pes_insert(qw.QWidget, ps_insert.Ui_Form):   #创建员工信息增添类
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #绑定信号与槽
        self.btn_add.clicked.connect(self.My_Sql)
        con_mysql(self)  # 连接数据库
    #实现槽函数
    def My_Sql(self):
        reply = qw.QMessageBox.question(self, '提示', '是否确认添加?', qw.QMessageBox.Yes | qw.QMessageBox.No,
                                     qw.QMessageBox.No)
        if(reply == qw.QMessageBox.Yes):
            try:
                cur = self.cur
                # 读取输入的信息
                id = self.lineEdit_id.text()
                name = self.lineEdit_name.text()
                face_id = -1
                sex = self.lineEdit_sex.text()
                phone = self.lineEdit_phone.text()
                number = self.lineEdit_number.text()
                section = self.lineEdit_section.text()
                position = self.lineEdit_position.text()
                place = self.lineEdit_place.text()
                edu =self.lineEdit_edu.text()
                note = self.lineEdit_note.text()
                # 插入sql语句
                sql1 = "select * from pes_show where 工号 = '" + id + "'"
                cur.execute(sql1)
                judge = cur.fetchall()
                if(len(judge)==0):
                    sql="INSERT INTO pes_show(工号,姓名,face_id,性别,电话,身份证,部门,职务,籍贯,学历,备注)" \
                         " VALUES ('"+id+"','"+name+"','"+str(face_id)+"','"+sex+"','"+phone+"','"+number+"','"+section+"','"+position+"','"+place+"','"+edu+"','"+note+"')"
                    cur.execute(sql)
                    self.connection.commit() #事务的提交
                    cur.close()
                    self.connection.close()
                    qw.QMessageBox.information(self, '提示', '增添成功', qw.QMessageBox.Ok)
                    self.lineEdit_id.clear()#清空单行框内容
                    self.lineEdit_name.clear()
                    self.lineEdit_sex.clear()
                    self.lineEdit_phone.clear()
                    self.lineEdit_number.clear()
                    self.lineEdit_section.clear()
                    self.lineEdit_position.clear()
                    self.lineEdit_place.clear()
                    self.lineEdit_edu.clear()
                    self.lineEdit_note.clear()
                else:
                    qw.QMessageBox.information(self, '提示', '员工已存在！', qw.QMessageBox.Ok)
            except:
                qw.QMessageBox.information(self, '提示', '增添失败', qw.QMessageBox.Close)

class adm_insert(qw.QWidget, ad_insert.Ui_Form):   #创建管理员信息增添类
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 绑定信号与槽
        self.btn_add.clicked.connect(self.My_Sql)
        con_mysql(self)  # 连接数据库
    # 实现槽函数
    def My_Sql(self):
        reply = qw.QMessageBox.question(self, '提示', '是否确认添加?', qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            try:
                cur = self.cur
                # 读取输入的信息
                id = self.lineEdit_id.text()
                password = self.lineEdit_psw.text()
                face_id = -1
                name = self.lineEdit_name.text()
                number = self.lineEdit_number.text()
                phone = self.lineEdit_phone.text()
                section = self.lineEdit_section.text()
                position = self.lineEdit_position.text()
                # print(str(face_id))
                # print(int(str(face_id)))
                # 插入sql语句
                sql = "select * from ad_show where 账号 = '" + id + "'"
                cur.execute(sql)
                judge = cur.fetchall()
                if (len(judge) == 0):
                    sql1 = "INSERT INTO ad_show(账号,姓名,face_id,身份证,电话,部门,职务)" \
                          " VALUES ('" + id + "','" + name + "'," + str(face_id) +" ,'" + number + "','" + phone + "','" + section + "','" + position + "')"
                    sql2 ="INSERT INTO admin(账号,密码) VALUES ('"+id+"','" + password + "')"
                    cur.execute(sql1)
                    cur.execute(sql2)
                    self.connection.commit()  # 事务的提交
                    cur.close()
                    self.connection.close()
                    qw.QMessageBox.information(self, '提示', '增添成功', qw.QMessageBox.Ok)
                    self.lineEdit_id.clear()    #清空单行框内容
                    self.lineEdit_psw.clear()
                    self.lineEdit_name.clear()
                    self.lineEdit_number.clear()
                    self.lineEdit_phone.clear()
                    self.lineEdit_section.clear()
                    self.lineEdit_position.clear()
                else:
                    qw.QMessageBox.information(self, '提示', '账号已存在！', qw.QMessageBox.Ok)
            except:
                qw.QMessageBox.information(self, '提示', '增添失败', qw.QMessageBox.Close)

class pes_show(qw.QWidget, ps_show.Ui_Form):   #创建员工信息展示类
    def __init__(self):
        super().__init__()
        InitUi(self)
        con_mysql(self)  # 连接数据库
        self.My_Sql()
    def My_Sql(self):    #连接mysql数据库
        try:
            cur = self.cur
            cur.execute('select * from pes_show')  # 将数据从数据库中拿出来
            total = cur.fetchall()
            table_build(self,total,self.tableWidget)
        except:
            qw.QMessageBox.information(self, '提示', '尚未添加管理员信息！', qw.QMessageBox.Ok)

class adm_show(qw.QWidget, ps_show.Ui_Form):   #创建管理员信息展示类
    def __init__(self):
        super().__init__()
        InitUi(self)
        con_mysql(self)  # 连接数据库
        self.My_Sql()

    def My_Sql(self):  # 取mysql数据库表内容
        try:
            cur = self.cur
            cur.execute('select * from ad_show')  # 将数据从数据库中拿出来
            total = cur.fetchall()
            table_build(self, total,self.tableWidget)
        except:
            qw.QMessageBox.information(self, '提示', '尚未添加管理员信息！', qw.QMessageBox.Ok)

class adminmsg(qw.QWidget, msg.Ui_Form):   #创建员工信息管理类
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化窗口
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # 绑定信号与槽
        self.btn_show.clicked.connect(self.btn_show_cb)
        self.btn_insert.clicked.connect(self.btn_insert_cb)
        self.btn_delete.clicked.connect(self.btn_delete_cb)
        self.btn_modify.clicked.connect(self.btn_modify_cb)
        self.btn_query.clicked.connect(self.btn_query_cb)

    # 实现槽函数
    def btn_show_cb(self):
        print("you clicked the btn_show.")
        self.w_show_1 = pes_show()
        self.splitter.addWidget(self.w_show_1)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_show_1)

    def btn_insert_cb(self):
        print("you clicked the btn_insert.")
        self.w_insert_1 = pes_insert()
        self.splitter.addWidget(self.w_insert_1)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_insert_1)

    def btn_delete_cb(self):
        print("you clicked the btn_delete.")
        self.w_delete_1 = pes_delete()
        self.splitter.addWidget(self.w_delete_1)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_delete_1)

    def btn_modify_cb(self):
        print("you clicked the btn_modify.")
        self.w_modify_1 = pes_modify()
        self.splitter.addWidget(self.w_modify_1)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_modify_1)
        # if(ps_modify.Ui_Form.modify())

    def btn_query_cb(self):
        print("you clicked the btn_query.")
        self.w_query_1 = pes_query()
        self.splitter.addWidget(self.w_query_1)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_query_1)


class adminID(qw.QWidget, id_amin.Ui_Form):   #创建管理员信息类
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化窗口
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # 绑定信号与槽
        self.btn_show.clicked.connect(self.btn_show_cb)
        self.btn_insert.clicked.connect(self.btn_insert_cb)
        self.btn_delete.clicked.connect(self.btn_delete_cb)
        self.btn_msg_modify.clicked.connect(self.btn_msg_modify_cb)
        self.btn_psw_modify.clicked.connect(self.btn_psw_modify_cb)
        self.btn_query.clicked.connect(self.btn_query_cb)

    # 实现槽函数
    def btn_show_cb(self):
        print("you clicked the btn_show.")
        self.w_show_2 = adm_show()
        self.splitter.addWidget(self.w_show_2)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_show_2)

    def btn_insert_cb(self):
        print("you clicked the btn_insert.")
        self.w_insert_2 = adm_insert()
        self.splitter.addWidget(self.w_insert_2)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_insert_2)

    def btn_delete_cb(self):
        print("you clicked the btn_delete.")
        self.w_delete_2 = adm_delete()
        self.splitter.addWidget(self.w_delete_2)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_delete_2)

    def btn_psw_modify_cb(self):
        print("you clicked the btn_modify.")
        self.w_modify_2 = adm_psw_modify()
        self.splitter.addWidget(self.w_modify_2)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_modify_2)

    def btn_msg_modify_cb(self):
        print("you clicked the btn_modify.")
        self.w_modify_3 = adm_msg_modify()
        self.splitter.addWidget(self.w_modify_3)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_modify_3)

    def btn_query_cb(self):
        print("you clicked the btn_query.")
        self.w_query = adm_query()
        self.splitter.addWidget(self.w_query)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_query)

class ad_face(qw.QWidget, face_admin.Ui_Form):   #创建人脸库管理类
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 绑定信号与槽
        self.btn_face_rec.clicked.connect(self.btn_face_rec_cb)
        self.btn_face_pre.clicked.connect(self.btn_face_pre_cb)
        self.btn_face_check.clicked.connect(self.btn_face_check_cb)

    def btn_face_rec_cb(self):
        print("you clicked btn_face_rec.")
        self.w_re = fe_record()  #实例化嵌套窗口
        self.splitter.addWidget(self.w_re)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_re)
    def btn_face_pre_cb(self):
        print("you clicked btn_face_pre.")
        self.w_train = fe_train()   #实例化嵌套窗口
        self.splitter.addWidget(self.w_train)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_train)
    def btn_face_check_cb(self):
        print("you clicked btn_face_pre.")
        self.w_recognition = fe_recognition()   #实例化嵌套窗口
        self.splitter.addWidget(self.w_recognition)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_recognition)

class adminWidget(qw.QWidget, mw_sys.Ui_Form):   #创建主界面类
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化窗口
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # 绑定信号与槽
        self.btn_msge.clicked.connect(self.btn_msge_cb)
        self.btn_id.clicked.connect(self.btn_id_cb)
        self.btn_face.clicked.connect(self.btn_face_cb)
        self.btn_close.clicked.connect(self.btn_close_cb)

    # 实现槽函数
    def btn_msge_cb(self):
        print("you clicked btn_msge.")
        self.w_msg = adminmsg() #实例化嵌套窗口
        self.splitter.addWidget(self.w_msg)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_msg)

    def btn_id_cb(self):
        print("you clicked btn_id.")
        self.w_id = adminID()   #实例化嵌套窗口
        self.splitter.addWidget(self.w_id)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_id)

    def btn_face_cb(self):
        print("you clicked btn_face.")
        self.w_face = ad_face() #实例化嵌套窗口
        self.splitter.addWidget(self.w_face)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_face)

    def btn_close_cb(self): #退出系统
        print("you clicked btn_msge.")
        adminWidget.close(self)


class mainWidget(qw.QWidget,login_face.Ui_Form):  # 将object改为QWidget，才能弹出消息对话框
    def __init__(self):
        super().__init__()  # 用户添加代码
        self.setupUi(self)

        # 初始化窗口
        self.setWindowTitle("员工管理系统")
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)
        self.w_admin = adminWidget()    #实例化主页面

        # 绑定信号与槽
        self.btn_login.clicked.connect(self.btn_login_cb)
        self.btn_facelogin.clicked.connect(self.btn_facelogin_cb)
        self.checkBox.toggled.connect(self.checkBox_cb)

    # 实现槽函数
    def btn_login_cb(self):
        print("you clicked the btn_login.")
        id = self.lineEdit_id.text()
        psw = self.lineEdit_pw.text()
        if(id == "" or psw == ""):
            qw.QMessageBox.information(self, '提示', '账号或密码不可为空！', qw.QMessageBox.Close)
        else:
            # --------判断用户是否存在--------------
            con_mysql(self)  # 连接数据库
            cur =self.cur
            sql = "select 账号,密码 from admin where 账号 = '" + id + "' "
            cur.execute(sql)
            password = cur.fetchall()
            # print(password)
            if (id == "admin" and psw == "123456"):
                self.w_admin.show()  # 显示管理窗口
                w.close()
            elif(len(password)==0):
                qw.QMessageBox.information(self, '提示', '用户不存在，请重新输入！', qw.QMessageBox.Close)
            elif(str(password[0][1])==psw): #判断密码是否一致
                self.w_admin.show()  # 显示管理窗口
                w.close()
            else:
                qw.QMessageBox.information(self, '提示', '密码错误', qw.QMessageBox.Close)

    def btn_facelogin_cb(self):
        print("you clicked the btn_facelogin.")
        self.w_faceLogin = Fe_login.run()
        # print(len(self.w_faceLogin))
        # print(self.w_faceLogin)
        if self.w_faceLogin == "True":
            qw.QMessageBox.information(self, self.w_faceLogin, '管理员,您好，欢迎进入员工管理系统！', qw.QMessageBox.Open)
            self.w_admin.show()  # 显示管理窗口
            w.close()
        elif self.w_faceLogin == "False":
            qw.QMessageBox.information(self, '提示', '抱歉,您不是管理员，无法进入系统！', qw.QMessageBox.Ok)
        else:
            qw.QMessageBox.information(self, '提示', '抱歉,识别身份失败，无法进入系统！', qw.QMessageBox.Ok)
    def checkBox_cb(self):
        print("you clicked the checkBox.")


if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    w = mainWidget()
    w.show()
    def InitUi(self):   #实例化窗口函数
        self.setupUi(self)
        self._translate = qc.QCoreApplication.translate
    def con_mysql(self):    #连接数据库
        self.connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                          database='students',
                                          charset='utf8')
        # print('successfully connect')
        self.cur = self.connection.cursor()
    def table_build(self,total,tableWidget):   #读取数据库的内容设置表格大小
        cur = self.cur
        col_result = cur.description
        self.tableWidget = tableWidget
        # print(col_result)
        # print(total)
        self.row = cur.rowcount  # 取得记录个数，用于设置表格的行数
        self.vol = len(total[0])  # 取得字段数，用于设置表格的列数
        col_result = list(col_result)
        a = 0
        self.tableWidget.setColumnCount(self.vol)
        self.tableWidget.setRowCount(self.row)
        for i in col_result:  # 设置表头信息，将mysql数据表中的表头信息拿出来，放进TableWidget中
            item = qw.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(a, item)  # 设置表格的标题名称
            item = self.tableWidget.horizontalHeaderItem(a)
            item.setBackground(qg.QColor(85, 170, 255, 60))
            item.setText(self._translate("Form", i[0]))
            a = a + 1
        total = list(total)  # 将数据格式改为列表形式，其是将数据库中取出的数据整体改为列表形式
        for i in range(len(total)):  # 将相关的数据
            total[i] = list(total[i])  # 将获取的数据转为列表形式
        for i in range(self.row):
            for j in range(self.vol):
                Table_Data(self,i, j, total[i][j])
    def Table_Data(self, i, j, data):    #创建显示数据库信息表格函数
        item = qw.QTableWidgetItem()
        self.tableWidget.setItem(i, j, item)
        item = self.tableWidget.item(i, j)
        item.setTextAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)  # 设置居中显示
        item.setText(self._translate("Form", str(data)))
        self.tableWidget.verticalHeader().setStyleSheet("background-color: rgb(147, 147, 220);")

    sys.exit(app.exec_())