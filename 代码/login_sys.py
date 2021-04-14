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


class fe_recognition(qw.QWidget, face_recognition.Ui_Form):   #��������ʶ��ϵͳǶ�״�����
    def __init__(self):
        super().__init__()
        InitUi(self)
        # ��ʼ��
        self.is_check = 0  # 0Ϊδ��ѯ��1Ϊ�Ѳ�ѯ
        # ���ź����
        self.btn_recognition.clicked.connect(self.btn_recognition_cb)
        self.btn_show.clicked.connect(self.btn_show_cb)
        con_mysql(self)  # �������ݿ�
    def btn_show_cb(self):
        print("you clicked btn_show.")
        cur = self.cur
        self.sql1 = "select * from pes_show"
        cur.execute(query=self.sql1)
        total1 = cur.fetchall()
        if (len(total1) == 0):  # or len(total2)==0
            qw.QMessageBox.information(self, '��ʾ', '��δ¼��Ա����Ϣ��', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self, total1, self.tableWidget_pes)
        self.sql2 = "select * from ad_show"
        cur.execute(query=self.sql2)
        total2 = cur.fetchall()
        if (len(total2) == 0):
            qw.QMessageBox.information(self, '��ʾ', '��δ¼�������Ϣ��', qw.QMessageBox.Ok)
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
            qw.QMessageBox.information(self, '��ʾ', '���ȵ����ѯȷ�ϸ�Ա�����˺��Ƿ���ڣ�', qw.QMessageBox.Ok)


class fe_train(qw.QWidget, face_train.Ui_Form):   #��������ѵ��ϵͳǶ�״�����
    def __init__(self):
        super().__init__()
        InitUi(self)
        # ��ʼ��
        self.is_check = 0 # 0Ϊδ��ѯ��1Ϊ�Ѳ�ѯ
        # ���ź����
        self.btn_train.clicked.connect(self.btn_train_cb)
        self.btn_show.clicked.connect(self.btn_show_cb)
        con_mysql(self) #�������ݿ�
    def btn_show_cb(self):
        print("you clicked btn_show.")
        cur = self.cur
        self.sql1 = "select * from pes_show"
        cur.execute(query=self.sql1)
        total1 = cur.fetchall()
        if (len(total1) == 0 ):#or len(total2)==0
            qw.QMessageBox.information(self, '��ʾ', '��δ¼��Ա����Ϣ��', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self,total1,self.tableWidget_pes)
        self.sql2 = "select * from ad_show"
        cur.execute(query=self.sql2)
        total2 = cur.fetchall()
        if (len(total2) == 0):
            qw.QMessageBox.information(self, '��ʾ', '��δ¼�������Ϣ��', qw.QMessageBox.Ok)
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
            qw.QMessageBox.information(self, '��ʾ', '���ȵ����ѯȷ�ϸ�Ա�����˺��Ƿ���ڣ�', qw.QMessageBox.Ok)

class fe_record(qw.QWidget, face_rec.Ui_Form):   #���������ɼ�ϵͳǶ�״�����
    def __init__(self):
        super().__init__()
        InitUi(self)
        # ��ʼ������
        self.radioButton_psid.setChecked(True)  # ��ʼѡ���Ų�ѯ
        self.is_select = 0  # 0Ϊ���Ų�ѯ��1Ϊ�˺Ų�ѯ
        self.is_check = 0 # 0Ϊδ��ѯ��1Ϊ�Ѳ�ѯ
        # ���ź����
        self.btn_record.clicked.connect(self.btn_record_cb)
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.radioButton_adid.toggled.connect(self.radioButton_adid_cb)
        self.radioButton_psid.toggled.connect(self.radioButton_psid_cb)
        con_mysql(self) #�������ݿ�
    def btn_check_cb(self):
        print("you clicked btn_check.")
        cur = self.cur
        id_name = self.lineEdit.text()
        if (self.is_select == 0):
            self.sql = "select * from pes_show where ���� = '" + id_name + "'"
        else:
            self.sql = "select * from ad_show where  �˺� = '" + id_name + "'"
        cur.execute(query=self.sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '��ʾ', '��Ա�����˺Ų�����,���������룡', qw.QMessageBox.Ok)
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
            qw.QMessageBox.information(self, '��ʾ', '���ȵ����ѯȷ�ϸ�Ա�����˺��Ƿ���ڣ�', qw.QMessageBox.Ok)
    def radioButton_adid_cb(self):
        print("you select the id_check.")
        self.is_select=1
    def radioButton_psid_cb(self):
        print("you select the name_check.")
        self.is_select=0


class adm_query(qw.QWidget, ad_query.Ui_Form):   #��������Ա��Ϣ��ѯ��
    def __init__(self):
        super().__init__()
        InitUi(self)
        # ���ź����
        self.btn_check.clicked.connect(self.btn_check_cb)
        con_mysql(self) #�������ݿ�
    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        sql = "select * from ad_show where �˺� = '" + id + "' "
        cur.execute(query=sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '��ʾ', '���˺Ų�����,���������룡', qw.QMessageBox.Ok)
        else:
            table_build(self,total,self.tableWidget)


class pes_query(qw.QWidget, ps_query.Ui_Form):   #����Ա����Ϣ��ѯ��
    def __init__(self):
        super().__init__()
        InitUi(self)
        # ��ʼ������
        self.radioButton_id.setChecked(True)  # ��ʼѡ���Ų�ѯ
        self.is_select = 0  #0Ϊ���Ų�ѯ��1Ϊ������ѯ
        # ���ź����
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.radioButton_id.toggled.connect(self.radioButton_id_cb)
        self.radioButton_name.toggled.connect(self.radioButton_name_cb)
        con_mysql(self) #�������ݿ�
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
            sql = "select * from pes_show where ���� = '" + id_name + "'"
        else:
            sql = "select * from pes_show where  ���� = '" + id_name + "'"
        cur.execute(query=sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '��ʾ', '��Ա��������,���������룡', qw.QMessageBox.Ok)
        else:
            table_build(self,total,self.tableWidget)

class adm_msg_modify(qw.QWidget, ad_msg_modify.Ui_Form):   #��������Ա��Ϣ�޸���
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.is_check = 0  # Ĭ��0Ϊδ��ѯ
        # ���ź����
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_modify.clicked.connect(self.btn_modify_cb)
        con_mysql(self) #�������ݿ�
    def btn_modify_cb(self):
        reply = qw.QMessageBox.question(self, '��ʾ', '�Ƿ�ȷ���޸�?', qw.QMessageBox.Yes | qw.QMessageBox.No,
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
                      "���� = '" + name + "',���֤='" + number + "',�绰='" + phone + "',����='" + section + "'," \
                                                                                                     "ְ��='" + position + "'WHERE �˺�='" + id + "'"
                cur.execute(sql)
                self.connection.commit()
                qw.QMessageBox.information(self, '��ʾ', '�޸ĳɹ���', qw.QMessageBox.Ok)
            else:
                qw.QMessageBox.information(self, '��ʾ', '���ȵ����ѯȷ�ϸ��˺��Ƿ���ڣ�', qw.QMessageBox.Ok)

    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        sql = "select * from ad_show where �˺� = '" + id + "'"
        cur.execute(query=sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '��ʾ', '�˺Ų����ڣ����������룡', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self,total,self.tableWidget)

class adm_psw_modify(qw.QWidget, ad_psw_modify.Ui_Form):   #��������Ա�˺������޸���
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.is_check = 0 #Ĭ��0Ϊδ��ѯ
        # ���ź����
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_modify.clicked.connect(self.btn_modify_cb)
        con_mysql(self) #�������ݿ�
    def btn_modify_cb(self):
        reply = qw.QMessageBox.question(self, '��ʾ', '�Ƿ�ȷ���޸�?', qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            if (self.is_check == 1):
                self.is_check = 0
                cur = self.cur
                id = self.tableWidget.item(0, 0).text()
                password = self.tableWidget.item(0, 1).text()
                cur.execute("update admin set ����= '" + password + "'WHERE �˺� = '" + id + "'")
                self.connection.commit()
                qw.QMessageBox.information(self, '��ʾ', '�޸ĳɹ���', qw.QMessageBox.Ok)
            else:
                qw.QMessageBox.information(self, '��ʾ', '���ȵ����ѯȷ�ϸ��˺��Ƿ���ڣ�', qw.QMessageBox.Ok)

    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        password = self.lineEdit_psw.text()
        sql =" select * from admin where �˺�='" + id + "'and ����='" + password + "'"
        cur.execute(query=sql)
        total = cur.fetchall()
        if (len(total) == 0):
            qw.QMessageBox.information(self, '��ʾ', '�˺Ų����ڻ��������', qw.QMessageBox.Ok)
        else:
            self.is_check = 1
            table_build(self,total,self.tableWidget)

class pes_modify(qw.QWidget, ps_modify.Ui_Form):   #����Ա����Ϣ�޸���
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.is_check = 0 #Ĭ��0Ϊδ��ѯ
        # ���ź����
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_modify.clicked.connect(self.btn_modify_cb)
        con_mysql(self)
    def btn_modify_cb(self):
        reply = qw.QMessageBox.question(self, '��ʾ', '�Ƿ�ȷ���޸�?', qw.QMessageBox.Yes | qw.QMessageBox.No,
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
                      " ����='" + name + "',�Ա�='" + sex + "',�绰='" + phone + "',���֤='" + number + "',����='" + section \
                      + "',ְ��='" + position + "',����='" + place + "',ѧ��='" + edu + "',��ע='" + note + "'WHERE ����='" + id + "'"
                cur.execute(sql)
                self.connection.commit()
                qw.QMessageBox.information(self, '��ʾ', '�޸ĳɹ���', qw.QMessageBox.Ok)
            else:
                qw.QMessageBox.information(self, '��ʾ', '���ȵ����ѯȷ�ϸ�Ա���Ƿ���ڣ�', qw.QMessageBox.Ok)
    def btn_check_cb(self):
        try:
            cur = self.cur
            id = self.lineEdit_id.text()
            name = self.lineEdit_name.text()
            sql = "select * from pes_show where ���� = '" + id + "' and ���� = '" + name + "'"  # ,���� = '" + name + "'
            cur.execute(query=sql)
            total = cur.fetchall()
            if (len(total) == 0):
                qw.QMessageBox.information(self, '��ʾ', '��Ա��������,��ȷ�Ϲ����Ƿ����������Ӧ��', qw.QMessageBox.Ok)
            else:
                self.is_check = 1
                table_build(self,total,self.tableWidget)
        except:
            qw.QMessageBox.information(self, '��ʾ', '��ȷ�Ϲ����Ƿ����������Ӧ��', qw.QMessageBox.Ok)


class adm_delete(qw.QWidget, ad_delete.Ui_Form):   #��������Ա��Ϣɾ����
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.datasets = './datasets'    #��ǰ����������ݵ�λ��
        self.isCheck = 0  # Ĭ��0Ϊδ��ѯ��ɾ����1Ϊ�Ѳ�ѯ
        # ���ź����
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_delete.clicked.connect(self.btn_delete_cb)
        con_mysql(self) #�������ݿ�
    def btn_delete_cb(self):
        text = '�����ݿ���ɾ�����û���ͬʱɾ����Ӧ�������ݣ�<font color=red>�ò��������棡</font>'
        informativeText = '<b>�Ƿ������</b>'
        reply = qw.QMessageBox.warning(self, "��ʾ", text + informativeText, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                       qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            if (self.isCheck == 1):
                self.isCheck = 0
                cur = self.cur
                id = self.lineEdit_id.text()
                password = self.lineEdit_psw.text()
                cur.execute("DELETE FROM ad_show WHERE �˺� = '" + id + "'")
                cur.execute("DELETE FROM admin WHERE �˺� = '" + id + "'and ���� = '" + password + "'")
                self.connection.commit()
                if os.path.exists('{}/stu_{}'.format(self.datasets, id)):
                    try:
                        shutil.rmtree('{}/stu_{}'.format(self.datasets, id))
                    except Exception as e:
                        logging.error('Error��ϵͳɾ����������ʧ�ܣ����ֶ�ɾ��{}/stu_{}Ŀ¼'.format(self.datasets, id))

                text = '���ѳɹ�ɾ���˺�Ϊ <font color=blue>{}</font> ���û���¼��'.format(id)
                informativeText = '<b>��������������ѵ���������ݡ�</b>'
                qw.QMessageBox.information(self, "��ʾ", text + informativeText, qw.QMessageBox.Ok)
                # ˢ��ǰ����tableWidget
                self.lineEdit_id.clear()
                self.lineEdit_psw.clear()
                while self.tableWidget.rowCount() > 0: # ����tableWidget
                    self.tableWidget.removeRow(0)
            else:
                qw.QMessageBox.information(self, '��ʾ', '���ȵ����ѯȷ���˺��Ƿ���ڣ�', qw.QMessageBox.Ok)

    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        password = self.lineEdit_psw.text()
        sql = "select * from admin where �˺� = '" + id + "'and ���� = '" + password + "'"
        cur.execute(query=sql)
        judge = cur.fetchall()
        if (len(judge) == 0):
            qw.QMessageBox.information(self, '��ʾ', '���˺Ų����ڻ��������,���������룡', qw.QMessageBox.Ok)
        else:
            sql1 = "select * from ad_show where �˺� = '" + id + "'"
            cur.execute(sql1)
            total = cur.fetchall()
            if(len(total)==0):
                qw.QMessageBox.information(self, '��ʾ', '�˺Ų�����,���������룡', qw.QMessageBox.Ok)
            else:
                self.isCheck = 1
                table_build(self,total,self.tableWidget)

class pes_delete(qw.QWidget, ps_delete.Ui_Form):   #����Ա����Ϣɾ����
    def __init__(self):
        super().__init__()
        InitUi(self)
        self.datasets = './datasets'    #��ǰ����������ݵ�λ��
        #��ʼ������
        self.isCheck = 0    #Ĭ��0Ϊδ��ѯ��ɾ����1Ϊ�Ѳ�ѯ
        # ���ź����
        self.btn_check.clicked.connect(self.btn_check_cb)
        self.btn_delete.clicked.connect(self.btn_delete_cb)
        con_mysql(self) #�������ݿ�
    def btn_delete_cb(self):
        text = '�����ݿ���ɾ�����û���ͬʱɾ����Ӧ�������ݣ�<font color=red>�ò��������棡</font>'
        informativeText = '<b>�Ƿ������</b>'
        reply = qw.QMessageBox.warning(self, "��ʾ",text+informativeText, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            if(self.isCheck==1):
                self.isCheck=0
                cur = self.cur
                id = self.lineEdit_id.text()
                name = self.lineEdit_name.text()
                cur.execute("DELETE FROM pes_show WHERE ���� = '" + id + "'and ���� = '" + name + "'")
                self.connection.commit()
                # print('{}/stu_{}'.format(self.datasets, id))
                if os.path.exists('{}/stu_{}'.format(self.datasets, id)):
                    try:
                        shutil.rmtree('{}/stu_{}'.format(self.datasets, id))
                    except Exception as e:
                        logging.error('Error��ϵͳɾ����������ʧ�ܣ����ֶ�ɾ��{}/stu_{}Ŀ¼'.format(self.datasets, id))

                text = '���ѳɹ�ɾ������Ϊ <font color=blue>{}</font> ���û���¼��'.format(id)
                informativeText = '<b>��������������ѵ���������ݡ�</b>'
                qw.QMessageBox.information(self, "��ʾ", text + informativeText,qw.QMessageBox.Ok)
                self.lineEdit_id.clear()
                self.lineEdit_name.clear()
                while self.tableWidget.rowCount() > 0: # ����tableWidget
                    self.tableWidget.removeRow(0)
            else:
                qw.QMessageBox.information(self, '��ʾ', '���ȵ����ѯȷ��Ա���Ƿ���ڣ�', qw.QMessageBox.Ok)

    def btn_check_cb(self):
        cur = self.cur
        id = self.lineEdit_id.text()
        name = self.lineEdit_name.text()
        sql = "select * from pes_show where ���� = '" + id + "' and ���� = '" + name + "'"#,���� = '" + name + "'
        cur.execute(query=sql)
        total = cur.fetchall()
        if(len(total)==0):
            qw.QMessageBox.information(self, '��ʾ', '��Ա��������,���������룡', qw.QMessageBox.Ok)
        else:
            self.isCheck = 1
            table_build(self,total,self.tableWidget)

class pes_insert(qw.QWidget, ps_insert.Ui_Form):   #����Ա����Ϣ������
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #���ź����
        self.btn_add.clicked.connect(self.My_Sql)
        con_mysql(self)  # �������ݿ�
    #ʵ�ֲۺ���
    def My_Sql(self):
        reply = qw.QMessageBox.question(self, '��ʾ', '�Ƿ�ȷ�����?', qw.QMessageBox.Yes | qw.QMessageBox.No,
                                     qw.QMessageBox.No)
        if(reply == qw.QMessageBox.Yes):
            try:
                cur = self.cur
                # ��ȡ�������Ϣ
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
                # ����sql���
                sql1 = "select * from pes_show where ���� = '" + id + "'"
                cur.execute(sql1)
                judge = cur.fetchall()
                if(len(judge)==0):
                    sql="INSERT INTO pes_show(����,����,face_id,�Ա�,�绰,���֤,����,ְ��,����,ѧ��,��ע)" \
                         " VALUES ('"+id+"','"+name+"','"+str(face_id)+"','"+sex+"','"+phone+"','"+number+"','"+section+"','"+position+"','"+place+"','"+edu+"','"+note+"')"
                    cur.execute(sql)
                    self.connection.commit() #������ύ
                    cur.close()
                    self.connection.close()
                    qw.QMessageBox.information(self, '��ʾ', '����ɹ�', qw.QMessageBox.Ok)
                    self.lineEdit_id.clear()#��յ��п�����
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
                    qw.QMessageBox.information(self, '��ʾ', 'Ա���Ѵ��ڣ�', qw.QMessageBox.Ok)
            except:
                qw.QMessageBox.information(self, '��ʾ', '����ʧ��', qw.QMessageBox.Close)

class adm_insert(qw.QWidget, ad_insert.Ui_Form):   #��������Ա��Ϣ������
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ���ź����
        self.btn_add.clicked.connect(self.My_Sql)
        con_mysql(self)  # �������ݿ�
    # ʵ�ֲۺ���
    def My_Sql(self):
        reply = qw.QMessageBox.question(self, '��ʾ', '�Ƿ�ȷ�����?', qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
        if (reply == qw.QMessageBox.Yes):
            try:
                cur = self.cur
                # ��ȡ�������Ϣ
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
                # ����sql���
                sql = "select * from ad_show where �˺� = '" + id + "'"
                cur.execute(sql)
                judge = cur.fetchall()
                if (len(judge) == 0):
                    sql1 = "INSERT INTO ad_show(�˺�,����,face_id,���֤,�绰,����,ְ��)" \
                          " VALUES ('" + id + "','" + name + "'," + str(face_id) +" ,'" + number + "','" + phone + "','" + section + "','" + position + "')"
                    sql2 ="INSERT INTO admin(�˺�,����) VALUES ('"+id+"','" + password + "')"
                    cur.execute(sql1)
                    cur.execute(sql2)
                    self.connection.commit()  # ������ύ
                    cur.close()
                    self.connection.close()
                    qw.QMessageBox.information(self, '��ʾ', '����ɹ�', qw.QMessageBox.Ok)
                    self.lineEdit_id.clear()    #��յ��п�����
                    self.lineEdit_psw.clear()
                    self.lineEdit_name.clear()
                    self.lineEdit_number.clear()
                    self.lineEdit_phone.clear()
                    self.lineEdit_section.clear()
                    self.lineEdit_position.clear()
                else:
                    qw.QMessageBox.information(self, '��ʾ', '�˺��Ѵ��ڣ�', qw.QMessageBox.Ok)
            except:
                qw.QMessageBox.information(self, '��ʾ', '����ʧ��', qw.QMessageBox.Close)

class pes_show(qw.QWidget, ps_show.Ui_Form):   #����Ա����Ϣչʾ��
    def __init__(self):
        super().__init__()
        InitUi(self)
        con_mysql(self)  # �������ݿ�
        self.My_Sql()
    def My_Sql(self):    #����mysql���ݿ�
        try:
            cur = self.cur
            cur.execute('select * from pes_show')  # �����ݴ����ݿ����ó���
            total = cur.fetchall()
            table_build(self,total,self.tableWidget)
        except:
            qw.QMessageBox.information(self, '��ʾ', '��δ��ӹ���Ա��Ϣ��', qw.QMessageBox.Ok)

class adm_show(qw.QWidget, ps_show.Ui_Form):   #��������Ա��Ϣչʾ��
    def __init__(self):
        super().__init__()
        InitUi(self)
        con_mysql(self)  # �������ݿ�
        self.My_Sql()

    def My_Sql(self):  # ȡmysql���ݿ������
        try:
            cur = self.cur
            cur.execute('select * from ad_show')  # �����ݴ����ݿ����ó���
            total = cur.fetchall()
            table_build(self, total,self.tableWidget)
        except:
            qw.QMessageBox.information(self, '��ʾ', '��δ��ӹ���Ա��Ϣ��', qw.QMessageBox.Ok)

class adminmsg(qw.QWidget, msg.Ui_Form):   #����Ա����Ϣ������
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ��ʼ������
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # ���ź����
        self.btn_show.clicked.connect(self.btn_show_cb)
        self.btn_insert.clicked.connect(self.btn_insert_cb)
        self.btn_delete.clicked.connect(self.btn_delete_cb)
        self.btn_modify.clicked.connect(self.btn_modify_cb)
        self.btn_query.clicked.connect(self.btn_query_cb)

    # ʵ�ֲۺ���
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


class adminID(qw.QWidget, id_amin.Ui_Form):   #��������Ա��Ϣ��
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ��ʼ������
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # ���ź����
        self.btn_show.clicked.connect(self.btn_show_cb)
        self.btn_insert.clicked.connect(self.btn_insert_cb)
        self.btn_delete.clicked.connect(self.btn_delete_cb)
        self.btn_msg_modify.clicked.connect(self.btn_msg_modify_cb)
        self.btn_psw_modify.clicked.connect(self.btn_psw_modify_cb)
        self.btn_query.clicked.connect(self.btn_query_cb)

    # ʵ�ֲۺ���
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

class ad_face(qw.QWidget, face_admin.Ui_Form):   #���������������
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ���ź����
        self.btn_face_rec.clicked.connect(self.btn_face_rec_cb)
        self.btn_face_pre.clicked.connect(self.btn_face_pre_cb)
        self.btn_face_check.clicked.connect(self.btn_face_check_cb)

    def btn_face_rec_cb(self):
        print("you clicked btn_face_rec.")
        self.w_re = fe_record()  #ʵ����Ƕ�״���
        self.splitter.addWidget(self.w_re)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_re)
    def btn_face_pre_cb(self):
        print("you clicked btn_face_pre.")
        self.w_train = fe_train()   #ʵ����Ƕ�״���
        self.splitter.addWidget(self.w_train)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_train)
    def btn_face_check_cb(self):
        print("you clicked btn_face_pre.")
        self.w_recognition = fe_recognition()   #ʵ����Ƕ�״���
        self.splitter.addWidget(self.w_recognition)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_recognition)

class adminWidget(qw.QWidget, mw_sys.Ui_Form):   #������������
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # ��ʼ������
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # ���ź����
        self.btn_msge.clicked.connect(self.btn_msge_cb)
        self.btn_id.clicked.connect(self.btn_id_cb)
        self.btn_face.clicked.connect(self.btn_face_cb)
        self.btn_close.clicked.connect(self.btn_close_cb)

    # ʵ�ֲۺ���
    def btn_msge_cb(self):
        print("you clicked btn_msge.")
        self.w_msg = adminmsg() #ʵ����Ƕ�״���
        self.splitter.addWidget(self.w_msg)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_msg)

    def btn_id_cb(self):
        print("you clicked btn_id.")
        self.w_id = adminID()   #ʵ����Ƕ�״���
        self.splitter.addWidget(self.w_id)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_id)

    def btn_face_cb(self):
        print("you clicked btn_face.")
        self.w_face = ad_face() #ʵ����Ƕ�״���
        self.splitter.addWidget(self.w_face)
        self.splitter.widget(1).setParent(None)
        self.splitter.insertWidget(1, self.w_face)

    def btn_close_cb(self): #�˳�ϵͳ
        print("you clicked btn_msge.")
        adminWidget.close(self)


class mainWidget(qw.QWidget,login_face.Ui_Form):  # ��object��ΪQWidget�����ܵ�����Ϣ�Ի���
    def __init__(self):
        super().__init__()  # �û���Ӵ���
        self.setupUi(self)

        # ��ʼ������
        self.setWindowTitle("Ա������ϵͳ")
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)
        self.w_admin = adminWidget()    #ʵ������ҳ��

        # ���ź����
        self.btn_login.clicked.connect(self.btn_login_cb)
        self.btn_facelogin.clicked.connect(self.btn_facelogin_cb)
        self.checkBox.toggled.connect(self.checkBox_cb)

    # ʵ�ֲۺ���
    def btn_login_cb(self):
        print("you clicked the btn_login.")
        id = self.lineEdit_id.text()
        psw = self.lineEdit_pw.text()
        if(id == "" or psw == ""):
            qw.QMessageBox.information(self, '��ʾ', '�˺Ż����벻��Ϊ�գ�', qw.QMessageBox.Close)
        else:
            # --------�ж��û��Ƿ����--------------
            con_mysql(self)  # �������ݿ�
            cur =self.cur
            sql = "select �˺�,���� from admin where �˺� = '" + id + "' "
            cur.execute(sql)
            password = cur.fetchall()
            # print(password)
            if (id == "admin" and psw == "123456"):
                self.w_admin.show()  # ��ʾ������
                w.close()
            elif(len(password)==0):
                qw.QMessageBox.information(self, '��ʾ', '�û������ڣ����������룡', qw.QMessageBox.Close)
            elif(str(password[0][1])==psw): #�ж������Ƿ�һ��
                self.w_admin.show()  # ��ʾ������
                w.close()
            else:
                qw.QMessageBox.information(self, '��ʾ', '�������', qw.QMessageBox.Close)

    def btn_facelogin_cb(self):
        print("you clicked the btn_facelogin.")
        self.w_faceLogin = Fe_login.run()
        # print(len(self.w_faceLogin))
        # print(self.w_faceLogin)
        if self.w_faceLogin == "True":
            qw.QMessageBox.information(self, self.w_faceLogin, '����Ա,���ã���ӭ����Ա������ϵͳ��', qw.QMessageBox.Open)
            self.w_admin.show()  # ��ʾ������
            w.close()
        elif self.w_faceLogin == "False":
            qw.QMessageBox.information(self, '��ʾ', '��Ǹ,�����ǹ���Ա���޷�����ϵͳ��', qw.QMessageBox.Ok)
        else:
            qw.QMessageBox.information(self, '��ʾ', '��Ǹ,ʶ�����ʧ�ܣ��޷�����ϵͳ��', qw.QMessageBox.Ok)
    def checkBox_cb(self):
        print("you clicked the checkBox.")


if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    w = mainWidget()
    w.show()
    def InitUi(self):   #ʵ�������ں���
        self.setupUi(self)
        self._translate = qc.QCoreApplication.translate
    def con_mysql(self):    #�������ݿ�
        self.connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                          database='students',
                                          charset='utf8')
        # print('successfully connect')
        self.cur = self.connection.cursor()
    def table_build(self,total,tableWidget):   #��ȡ���ݿ���������ñ���С
        cur = self.cur
        col_result = cur.description
        self.tableWidget = tableWidget
        # print(col_result)
        # print(total)
        self.row = cur.rowcount  # ȡ�ü�¼�������������ñ�������
        self.vol = len(total[0])  # ȡ���ֶ������������ñ�������
        col_result = list(col_result)
        a = 0
        self.tableWidget.setColumnCount(self.vol)
        self.tableWidget.setRowCount(self.row)
        for i in col_result:  # ���ñ�ͷ��Ϣ����mysql���ݱ��еı�ͷ��Ϣ�ó������Ž�TableWidget��
            item = qw.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(a, item)  # ���ñ��ı�������
            item = self.tableWidget.horizontalHeaderItem(a)
            item.setBackground(qg.QColor(85, 170, 255, 60))
            item.setText(self._translate("Form", i[0]))
            a = a + 1
        total = list(total)  # �����ݸ�ʽ��Ϊ�б���ʽ�����ǽ����ݿ���ȡ�������������Ϊ�б���ʽ
        for i in range(len(total)):  # ����ص�����
            total[i] = list(total[i])  # ����ȡ������תΪ�б���ʽ
        for i in range(self.row):
            for j in range(self.vol):
                Table_Data(self,i, j, total[i][j])
    def Table_Data(self, i, j, data):    #������ʾ���ݿ���Ϣ�����
        item = qw.QTableWidgetItem()
        self.tableWidget.setItem(i, j, item)
        item = self.tableWidget.item(i, j)
        item.setTextAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)  # ���þ�����ʾ
        item.setText(self._translate("Form", str(data)))
        self.tableWidget.verticalHeader().setStyleSheet("background-color: rgb(147, 147, 220);")

    sys.exit(app.exec_())