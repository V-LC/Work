# -*- coding: utf-8 -*-
import FaceTrain
import pymysql
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import cv2
import os
import logging
import logging.config
import multiprocessing
import numpy as np
import threading
import datetime

# 自定义数据库记录不存在异常
class RecordNotFound(Exception):
    pass

class Fe_train(qw.QWidget, FaceTrain.Ui_Form):   #创建管理员信息查询类
    logQueue = multiprocessing.Queue()  # 日志队列
    receiveLogSignal = qc.pyqtSignal(str)  # 日志信号
    def __init__(self):
        super().__init__()
        InitUi(self)
        # 初始化窗口
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # 数据库
        con_mysql(self)  # 连接数据库
        self.datasets = './datasets'
        self.isDbReady = False
        self.btn_init_mysql.clicked.connect(self.btn_init_mysql_cb)

        # 训练人脸数据
        self.btn_train.clicked.connect(self.btn_train_cb)

        # 系统日志
        self.receiveLogSignal.connect(lambda log: self.logOutput(log))
        self.logOutputThread = threading.Thread(target=self.receiveLog, daemon=True)  #创建守护线程
        self.logOutputThread.start()

    def btn_init_mysql_cb(self):    #初始化数据库
        # 刷新前重置tableWidget
        while self.tableWidget_ad.rowCount() > 0 :
            self.tableWidget_ad.removeRow(0)
        while self.tableWidget_pes.rowCount() > 0:
            self.tableWidget_pes.removeRow(0)
        try:
            con_mysql(self)
            cursor = self.cur
            conn = self.connection
            self.sql1 = "select * from pes_show"
            cursor.execute(query=self.sql1)
            total1 = cursor.fetchall()
            if len(total1) != 0:
                table_build(self, total1, self.tableWidget_pes)
            self.sql2 = "select * from ad_show"
            cursor.execute(query=self.sql2)
            total2 = cursor.fetchall()
            if len(total2) != 0:
                table_build(self, total2, self.tableWidget_ad)
            cursor.execute('SELECT Count(*) FROM pes_show')
            result1 = cursor.fetchone()
            cursor.execute('SELECT Count(*) FROM ad_show')
            result2 = cursor.fetchone()
            dbUserCount = result1[0] + result2[0]
        except Exception:
            logging.error('读取数据库异常，无法完成数据库初始化')
            self.isDbReady = False
            self.logQueue.put('Error：读取数据库异常，初始化/刷新数据库失败')
        else:
            cursor.close()
            conn.close()
            self.lcd_save.display(dbUserCount)
            if not self.isDbReady:
                self.isDbReady = True
                self.logQueue.put('Success：数据库初始化完成，发现用户数：{}'.format(dbUserCount))
                self.btn_init_mysql.setText('刷新数据库')
                self.btn_train.setToolTip('')
                self.btn_train.setEnabled(True)
            else:
                self.logQueue.put('Success：刷新数据库成功，发现用户数：{}'.format(dbUserCount))

    # 检测人脸
    def detectFace(self, img):
        # 灰度化，提高检测率
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 加载haarcascade文件来预测图像中的人脸
        face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
        # 检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸
        # 其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为构成检测目标的相邻矩形的最小个数，minSize限制目标区域范围
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(90, 90))
        # 如果未检测到面部，则返回原始图像
        if (len(faces) == 0):
            return None, None
        # 目前假设只有一张脸，xy为左上角坐标，wh为矩形的宽高
        (x, y, w, h) = faces[0]
        # 返回图像的正面部分
        return gray[y:y + w, x:x + h], faces[0]

    # 准备图片数据
    # 该函数将读取所有的训练图像，从每个图像检测人脸并将返回两个相同大小的列表，分别为脸部信息和标签
    def prepareTrainingData(self, data_folder_path):
        # 获取数据文件夹中的目录
        dirs = os.listdir(data_folder_path)
        # 两个列表分别保存所有的脸部和标签
        faces = []
        labels = []

        face_id = 1
        con_mysql(self)
        cursor = self.cur
        conn = self.connection

        # 遍历人脸库
        for dir_name in dirs:
            if not dir_name.startswith('stu_'):
                continue
            stu_id = dir_name.replace('stu_', '')
            try:
                cursor.execute("select * from pes_show where 工号 = '" + stu_id + "'")
                ret = cursor.fetchall()
                # print(ret)
                if (len(ret)==0):
                    cursor.execute("select * from ad_show where  账号 = '" + stu_id + "'")
                    ret1 = cursor.fetchall()
                    # print(ret1)
                    if (len(ret1)==0):
                        raise RecordNotFound
                    cursor.execute("update ad_show set face_id= '" + str(face_id) + "'WHERE 账号 = '" + stu_id + "'")
                # print("hello")
                else:
                    cursor.execute("update pes_show set face_id= '" + str(face_id) + "'WHERE 工号 = '" + stu_id + "'")
                # print("hello")
            except RecordNotFound:
                logging.warning('数据库中找不到工号或账号为{}的用户记录'.format(stu_id))
                self.logQueue.put('发现工号或账号为{}的人脸数据，但数据库中找不到相应记录，已忽略'.format(stu_id))
                continue
            # 建立包含当前主题主题图像的目录路径
            subject_dir_path = data_folder_path + '/' + dir_name
            # 获取给定主题目录内的图像名称
            subject_images_names = os.listdir(subject_dir_path)
            # 浏览每张图片并检测脸部，然后将脸部信息添加到脸部列表faces[]
            for image_name in subject_images_names:
                if image_name.startswith('.'):
                    continue
                # 建立图像路径
                image_path = subject_dir_path + '/' + image_name
                # 读取图像
                image = cv2.imread(image_path)
                # 检测脸部
                face, rect = self.detectFace(image)
                # 我们忽略未检测到的脸部
                if face is not None:
                    faces.append(face)
                    labels.append(face_id)
            face_id = face_id + 1

        cursor.close()
        conn.commit()
        conn.close()
        # 最终返回值为人脸和标签列表
        return faces, labels


    # 训练人脸数据
    def btn_train_cb(self):
        try:
            if not os.path.isdir(self.datasets):
                raise FileNotFoundError

            text = '系统将开始训练人脸数据，界面会暂停响应一段时间，完成后会弹出提示。'
            informativeText = '<b>训练过程请勿进行其它操作，是否继续？</b>'
            ret = qw.QMessageBox.question(self, "提示",text+informativeText, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                          qw.QMessageBox.No)
            if ret == qw.QMessageBox.Yes:
                # 创建LBPH识别器并开始训练
                face_recognizer = cv2.face.LBPHFaceRecognizer_create()
                if not os.path.exists('./recognizer'):
                    os.makedirs('./recognizer')
            # 训练数据
            faces, labels = self.prepareTrainingData(self.datasets)
            # 训练
            face_recognizer.train(faces, np.array(labels))
            # 训练的数据保存路径
            face_recognizer.save('./recognizer/trainingData.yml')
        except FileNotFoundError:
            logging.error('系统找不到人脸数据目录{}'.format(self.datasets))
            self.logQueue.put('未发现人脸数据目录{}，你可能未进行人脸采集'.format(self.datasets))
        except Exception as e:
            logging.error('遍历人脸库出现异常，训练人脸数据失败')
            self.logQueue.put('Error：遍历人脸库出现异常，训练失败')
        else:
            text = '<font color=green><b>Success!</b></font> 系统已生成./recognizer/trainingData.yml'
            informativeText = '<b>人脸数据训练完成！</b>'
            qw.QMessageBox.information(self,"提示",text+informativeText, qw.QMessageBox.Ok)
            self.logQueue.put('Success：人脸数据训练完成')
            self.btn_init_mysql_cb()

    # 系统日志服务常驻，接收并处理系统日志
    def receiveLog(self):
        while True:
            data = self.logQueue.get()
            if data:
                self.receiveLogSignal.emit(data)
            else:
                continue

    # LOG输出
    def logOutput(self,log):
        # 获取当前系统时间
        time = datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S]')
        log = time + ' ' + log + '\n'

        self.textEdit.moveCursor(qg.QTextCursor.End)
        self.textEdit.insertPlainText(log)
        self.textEdit.ensureCursorVisible()  # 自动滚屏

def InitUi(self):
        self.setupUi(self)
        self._translate = qc.QCoreApplication.translate
def con_mysql(self):
    self.connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                      database='students',
                                      charset='utf8')
    print('successfully connect')
    self.cur = self.connection.cursor()
def table_build(self,total,tableWidget):
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
def Table_Data(self, i, j, data):
    item = qw.QTableWidgetItem()
    self.tableWidget.setItem(i, j, item)
    item = self.tableWidget.item(i, j)
    item.setTextAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)  # 设置居中显示
    self.tableWidget.verticalHeader().setHidden(True)
    item.setText(self._translate("Form", str(data)))