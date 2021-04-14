# -*- coding: utf-8 -*-
import FaceRecord
import pymysql
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import cv2
import logging
import logging.config
import queue
import threading
import os
import sys
import datetime


# 采集过程中出现干扰
class RecordDisturbance(Exception):
    pass

# 自定义数据库记录不存在异常
class RecordNotFound(Exception):
    pass

class Fe_record(qw.QWidget, FaceRecord.Ui_Form):   #创建管理员信息查询类
    receiveLogSignal = qc.pyqtSignal(str) # 自定义信号
    def __init__(self):
        super().__init__()
        InitUi(self)
        # 初始化窗口
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # 数据库
        con_mysql(self) #连接数据库
        self.datasets = './datasets'
        self.isDbReady = False
        self.btn_Init_mysql.clicked.connect(self.init_mysql)

        # OpenCV
        self.cap = cv2.VideoCapture()
        self.faceCascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')

        self.logQueue = queue.Queue()  # 日志队列

        # 图像捕获
        self.isExternalCameraUsed = 0 # 0为不使用外接摄像头，1为使用外接摄像头
        self.cam_status = 0 #0未未打开摄像头
        self.checkBox_external.stateChanged.connect(self.checkBox_external_cb)
        self.btn_open_camera.clicked.connect(self.startWebcam)

        # 定时器
        self.timer = qc.QTimer(self)
        self.timer.timeout.connect(self.updateFrame)

        # 人脸检测
        self.isFaceDetectEnabled = False
        self.face_check_status = 0  # 0为未打开人脸检测
        self.btn_start_check.clicked.connect(self.enableFaceDetect)
        self.btn_start_check.setCheckable(True)

        # 用户信息
        self.isUserInfoReady = False
        self.btn_sync_mysql.clicked.connect(self.migrateToDb)

        # 人脸采集
        self.btn_start_rec.clicked.connect(self.start_face_rec_cb)
        self.spinBox.setSingleStep(20)    #设置步数调整的大小
        self.spinBox.setRange(0,1000)  # 设置重复发送时间的范围
        self.spinBox.setValue(100)  # 设置起始数值
        self.spinBox.setWrapping(True)  # 设置循环显示
        self.faceRecordCount = 0
        self.minFaceRecordCount = self.spinBox.value()
        self.isFaceDataReady = False
        self.isFaceRecordEnabled = False
        self.btn_rec_current.clicked.connect(self.btn_rec_current_cb)

        # 日志系统
        self.receiveLogSignal.connect(lambda log: self.logOutput(log))
        self.logOutputThread = threading.Thread(target=self.receiveLog, daemon=True)
        self.logOutputThread.start()

    def checkBox_external_cb(self): #设置外接摄像头chekBox槽函数
        if self.checkBox_external.isChecked():
            self.isExternalCameraUsed = 1
        else:
            self.isExternalCameraUsed = 0

    # 打开/关闭摄像头
    def startWebcam(self):
        if (self.cam_status == 0):
            self.cam_status = 1
            if (self.isExternalCameraUsed==1):
                camID = 1
            else:
                camID = 0
            self.cap.open(camID)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 591)#设置图像宽度
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 471)#设置图像高度
            ret, frame = self.cap.read()
            # print(ret)
            if not ret:
                logging.error('无法调用电脑摄像头{}'.format(camID))
                self.logQueue.put('Error：初始化摄像头失败')
                self.cap.release()
                self.btn_open_camera.setChecked(False)
            else:
                self.btn_open_camera.setText('关闭摄像头')
                self.btn_start_check.setEnabled(True)
                self.timer.start(5)
        else:
            if self.cap.isOpened():
                if self.timer.isActive():
                    self.timer.stop()
                self.cap.release()
                self.face_label.clear()
                self.face_label.setText('<font color=red>摄像头未开启</font>')
                self.btn_open_camera.setText('打开摄像头')
                self.btn_start_check.setEnabled(False)

    # 开启/关闭人脸检测
    def enableFaceDetect(self):
        if self.cap.isOpened():
            if (self.face_check_status==0):
                self.face_check_status = 1
                self.btn_start_check.setText('关闭人脸检测')
                self.isFaceDetectEnabled = True
            else:
                self.face_check_status = 0
                self.enableFaceDetectButton.setText('开启人脸检测')
                self.isFaceDetectEnabled = False

    # 采集当前捕获帧
    def btn_rec_current_cb(self):
        if not self.isFaceRecordEnabled:
            self.minFaceRecordCount = self.spinBox.value()  # 更新数值
            if self.minFaceRecordCount < 100:
                self.logQueue.put('Error：当前采集数据过少，易导致较大的识别误差，请设置100-1000之间的数值！')
                text = '您当前设计了采集 <font color=blue>{}</font> 帧图像，采集数据过少会导致较大的识别误差。'.format(self.minFaceRecordCount)
                informativeText = '<b>请至少采集 <font color=red>{}</font> 帧图像。</b>'.format(100)
                qw.QMessageBox.information(self,"提示",text+informativeText, qw.QMessageBox.Ok)
            else:
                self.isFaceRecordEnabled = True
                self.btn_rec_current.setText("结束当前捕帧")
        else:
            self.isFaceRecordEnabled = True
            self.btn_rec_current.setText("采集当前捕帧")

    # 开始/结束采集人脸数据
    def start_face_rec_cb(self,):
        if self.btn_start_rec.text() == '开始采集数据':
            if self.isFaceDetectEnabled:
                if self.isUserInfoReady:
                    if not self.btn_rec_current.isEnabled():
                        self.btn_rec_current.setEnabled(True)
                    self.btn_start_rec.setText('结束当前采集')
                else:
                    self.btn_start_rec.setChecked(False)
                    self.logQueue.put('Error：操作失败，系统未检测到有效的用户信息')
            else:
                self.logQueue.put('Error：操作失败，请开启人脸检测')
        else:
            if self.faceRecordCount < self.minFaceRecordCount:
                text = '系统当前采集了 <font color=blue>{}</font> 帧图像，采集数据过少会导致较大的识别误差。'.format(self.faceRecordCount)
                informativeText = '<b>请至少采集 <font color=red>{}</font> 帧图像。</b>'.format(100)
                qw.QMessageBox.information(self, "提示",text+informativeText, qw.QMessageBox.Ok)
            else:
                text = '系统当前采集了 <font color=blue>{}</font> 帧图像，继续采集可以提高识别准确率。'.format(self.faceRecordCount)
                informativeText = '<b>你确定结束当前人脸采集吗？</b>'
                ret = qw.QMessageBox.question(self, "提示",text+informativeText, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                        qw.QMessageBox.No)
                if ret == qw.QMessageBox.Yes:
                    self.isFaceDataReady = True
                    if self.isFaceRecordEnabled:
                        self.isFaceRecordEnabled = False
                    self.btn_rec_current.setEnabled(False)
                    self.btn_start_rec.setText('开始采集数据')
                    self.btn_start_rec.setEnabled(False)
                    self.btn_sync_mysql.setEnabled(True)

    # 定时器，实时更新画面
    def updateFrame(self):
        ret, frame = self.cap.read()
        # self.image = cv2.flip(self.image, 1)
        if ret:
            self.displayImage(frame)

            if self.isFaceDetectEnabled:
                detected_frame = self.detectFace(frame)
                self.detectFace(detected_frame)
                self.displayImage(frame)
            else:
                self.displayImage(frame)

    # 检测人脸
    def detectFace(self, frame):
        # 图像灰度化，提高识别率
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸
        # 其中gray为要检测的灰度图像，1.2为每次图像尺寸减小的比例，5为构成检测目标的相邻矩形的最小个数，minSize限制目标区域范围
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 5, minSize=(90, 90))
        stu_id = self.mysql_msg[0][0]

        # 框选人脸，for循环保证一个能检测的实时动态视频流
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x - 5, y - 10), (x + w + 5, y + h + 10), (0, 0, 255), 2)
            if self.isFaceRecordEnabled:
                while (self.faceRecordCount < self.minFaceRecordCount) :
                    try:
                        if not os.path.exists('{}/stu_{}'.format(self.datasets, stu_id)):
                            os.makedirs('{}/stu_{}'.format(self.datasets, stu_id))
                        if len(faces) > 1:
                            raise RecordDisturbance
                        # 图片存储
                        cv2.imwrite('{}/stu_{}/img.{}.jpg'.format(self.datasets, stu_id, self.faceRecordCount + 1),
                                    gray[y - 20:y + h + 20, x - 20:x + w + 20])
                    except RecordDisturbance:
                        self.isFaceRecordEnabled = False
                        logging.error('检测到多张人脸或环境干扰')
                        self.logQueue.put('Warning：检测到多张人脸或环境干扰，请解决问题后继续')
                        continue
                    except Exception as e:
                        logging.error('写入人脸图像文件到计算机过程中发生异常')
                        self.logQueue.put('Error：无法保存人脸图像，采集当前捕获帧失败')
                        break
                    else:
                        self.faceRecordCount = self.faceRecordCount + 1
                        self.lcd_rec.display(self.faceRecordCount)
                # 画矩阵
                cv2.rectangle(frame, (x - 5, y - 10), (x + w + 5, y + h + 10), (0, 0, 255), 2)

        return frame

    # 显示图像
    def displayImage(self, img):
        # BGR -> RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # default：The image is stored using 8-bit indexes into a colormap， for example：a gray image
        qformat = qg.QImage.Format_Indexed8

        if len(img.shape) == 3:  # rows[0], cols[1], channels[2]
            if img.shape[2] == 4:
                # The image is stored using a 32-bit byte-ordered RGBA format (8-8-8-8)
                # A: alpha channel，不透明度参数。如果一个像素的alpha通道数值为0%，那它就是完全透明的
                qformat = qg.QImage.Format_RGBA8888
            else:
                qformat = qg.QImage.Format_RGB888

        # img.shape[1]：图像宽度width，img.shape[0]：图像高度height，img.shape[2]：图像通道数
        # QImage.__init__ (self, bytes data, int width, int height, int bytesPerLine, Format format)
        # 从内存缓冲流获取img数据构造QImage类
        # img.strides[0]：每行的字节数（width*3）,rgb为3，rgba为4
        # strides[0]为最外层(即一个二维数组所占的字节长度)，strides[1]为次外层（即一维数组所占字节长度），strides[2]为最内层（即一个元素所占字节长度）
        # 从里往外看，strides[2]为1个字节长度（uint8），strides[1]为3*1个字节长度（3即rgb 3个通道）
        # strides[0]为width*3个字节长度，width代表一行有几个像素

        outImage = qg.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        self.face_label.setPixmap(qg.QPixmap.fromImage(outImage))
        self.face_label.setScaledContents(True)

    # 初始化数据库
    def init_mysql(self):
        cursor = self.cur
        conn =self.connection
        try:
            # 检测人脸数据目录是否存在，不存在则创建
            if not os.path.isdir(self.datasets):
                os.makedirs(self.datasets)
            # 查询数据表记录数
            cursor.execute('SELECT Count(*) FROM pes_show')
            result1 = cursor.fetchone()
            cursor.execute('SELECT Count(*) FROM ad_show')
            result2 = cursor.fetchone()
            dbUserCount = result1[0] +result2[0]
        except Exception as e:
            logging.error('读取数据库异常，无法完成数据库初始化')
            self.isDbReady = False
            self.logQueue.put('Error：初始化数据库失败')
        else:
            self.isDbReady = True
            self.lcd_save.display(dbUserCount)
            self.logQueue.put('Success：数据库初始化完成')
            self.btn_Init_mysql.setEnabled(False)
        finally:
            cursor.close()
            conn.commit()
            conn.close()

    # 同步用户信息到数据库
    def migrateToDb(self):
        if self.isFaceDataReady:

            stu_id = self.mysql_msg[0][0]
            text = '<font color=blue>{}</font> 已添加/更新到数据库。'.format(stu_id)
            informativeText = '人脸数据采集已完成！'
            qw.QMessageBox.information(self, text, informativeText, qw.QMessageBox.Ok)

            con_mysql(self)
            cursor = self.cur
            conn = self.connection
            face_id = 0
            cursor.execute("select * from pes_show where 工号 = '" + stu_id + "'")
            ret = cursor.fetchall()
            # print(ret)
            if (len(ret)==0):
                cursor.execute("select * from ad_show where  账号 = '" + stu_id + "'")
                ret1 = cursor.fetchall()
                print(ret1)
                if (len(ret1)==0):
                    raise RecordNotFound
                cursor.execute("update ad_show set face_id= '" + str(face_id) + "'WHERE 账号 = '" + stu_id + "'")
            else:
                cursor.execute("update pes_show set face_id= '" + str(face_id) + "'WHERE 工号 = '" + stu_id + "'")
            conn.commit()
            self.isUserInfoReady = False

            self.faceRecordCount = 0
            self.isFaceDataReady = False
            self.lcd_rec.display(self.faceRecordCount)
        else:
            self.logQueue.put('Error：操作失败，你尚未完成人脸数据采集')

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

    # 从数据库读取信息显示在tableWidght中
    def re_table(self,sql):
        cur = self.cur
        cur.execute(query=sql)
        total = cur.fetchall()
        self.mysql_msg = total
        self.isUserInfoReady = True
        # print(self.mysql_msg[0][0])
        if (len(total) == 0):
            qw.QMessageBox.information(self, '提示', '该员工或账号不存在,请重新输入！', qw.QMessageBox.Ok)
        else:
            table_build(self, total)

def InitUi(self):
    self.setupUi(self)
    self._translate = qc.QCoreApplication.translate
def con_mysql(self):
    self.connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                      database='students',
                                      charset='utf8')
    print('successfully connect')
    self.cur = self.connection.cursor()
def table_build(self,total):
    cur = self.cur
    col_result = cur.description
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
    item.setText(self._translate("Form", str(data)))
    self.tableWidget.verticalHeader().setHidden(True)

