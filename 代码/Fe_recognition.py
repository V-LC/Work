# -*- coding: utf-8 -*-
import FaceRecognition
import pymysql
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import PyQt5.QtGui as qg
import queue
import cv2
import multiprocessing
import logging
import os
import dlib
import threading
import datetime

# 找不到已训练的人脸数据文件
class TrainingDataNotFoundError(FileNotFoundError):
    pass

class Fe_recognition(qw.QWidget, FaceRecognition.Ui_Form):   #创建人脸识别系统类
    trainingData = './recognizer/trainingData.yml'  #训练集
    cap = cv2.VideoCapture()
    captureQueue = queue.Queue()  # 图像队列
    logQueue = multiprocessing.Queue()  # 日志队列
    receiveLogSignal = qc.pyqtSignal(str)  # LOG信号

    def __init__(self):
        super().__init__()
        InitUi(self)
        # 初始化窗口
        style = qw.QStyleFactory.create("Fusion")
        qw.QApplication.setStyle(style)

        # 数据库
        self.btn_Init_mysql.clicked.connect(self.btn_Init_mysql_cb)

        # 图像捕获
        self.isExternalCameraUsed = 0  # 0为不使用外接摄像头，1为使用外接摄像头
        self.cam_status = 0  # 0未未打开摄像头
        self.checkBox_external.stateChanged.connect(self.checkBox_external_cb)
        self.faceProcessingThread = FaceProcessingThread()
        self.btn_open_camera.clicked.connect(self.startWebcam)

        self.timer = qc.QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.updateFrame)

        # 功能开关
        self.checkBox_track.stateChanged.connect(
            lambda: self.faceProcessingThread.enableFaceTracker(self))
        self.checkBox_face_recognition.stateChanged.connect(
            lambda: self.faceProcessingThread.enableFaceRecognizer(self))

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
            if (self.isExternalCameraUsed == 1):
                camID = 1
            else:
                camID = 0
            self.cap.open(camID)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 591)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 491)
            ret, frame = self.cap.read()
            # print(ret)
            if not ret:
                logging.error('无法调用电脑摄像头{}'.format(camID))
                self.logQueue.put('Error：初始化摄像头失败')
                self.cap.release()
                self.btn_open_camera.setChecked(False)
            else:
                self.faceProcessingThread.start()  # 启动OpenCV图像处理线程
                self.timer.start(5)  # 启动定时器
                self.btn_open_camera.setText('关闭摄像头')
        else:
            text = '如果关闭摄像头，须重启程序才能再次打开。'
            informativeText = '<b>是否继续？</b>'
            ret = qw.QMessageBox.question(self, "提示",text+informativeText, qw.QMessageBox.Yes | qw.QMessageBox.No,
                                          qw.QMessageBox.No)
            if ret == qw.QMessageBox.Yes:
                self.faceProcessingThread.stop()
                if self.cap.isOpened():
                    if self.timer.isActive():
                        self.timer.stop()
                    self.cap.release()
                    self.face_label.clear()
                    self.face_label.setText('<font color=red>摄像头未开启</font>')
                    self.btn_open_camera.setText('打开摄像头')
                    self.btn_open_camera.setEnabled(False)

    # 定时器，实时更新画面
    def updateFrame(self):
        if self.cap.isOpened():
            # ret, frame = self.cap.read()
            # if ret:
            #     self.showImg(frame, self.realTimeCaptureLabel)
            if not self.captureQueue.empty():
                captureData = self.captureQueue.get()
                realTimeFrame = captureData.get('realTimeFrame')
                self.displayImage(realTimeFrame)

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

    def btn_Init_mysql_cb(self):
        try:
            if not os.path.isfile(self.trainingData):
                raise TrainingDataNotFoundError
            con_mysql(self)
            cursor = self.cur
            conn = self.connection
            # 查询数据表记录数
            cursor.execute('SELECT Count(*) FROM pes_show')
            result1 = cursor.fetchone()
            cursor.execute('SELECT Count(*) FROM ad_show')
            result2 = cursor.fetchone()
            dbUserCount = result1[0] + result2[0]
        except TrainingDataNotFoundError:
            logging.error('系统找不到已训练的人脸数据{}'.format(self.trainingData))
            self.logQueue.put('Error：未发现已训练的人脸数据文件，请完成训练后继续')
        except Exception as e:
            logging.error('读取数据库异常，无法完成数据库初始化')
            self.logQueue.put('Error：读取数据库异常，初始化数据库失败')
        else:
            cursor.close()
            conn.close()
            if not dbUserCount > 0:
                logging.warning('数据库为空')
                self.logQueue.put('warning：数据库为空，人脸识别功能不可用')
            else:
                self.logQueue.put('Success：数据库状态正常，发现用户数：{}'.format(dbUserCount))
                self.lcd_save.display(dbUserCount)
                self.btn_Init_mysql.setEnabled(False)
                self.checkBox_face_recognition.setToolTip('须先开启人脸跟踪')
                self.checkBox_face_recognition.setEnabled(True)

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


# OpenCV线程
class FaceProcessingThread(qc.QThread):
    def __init__(self):
        super(FaceProcessingThread, self).__init__()
        self.isRunning = True

        self.isFaceTrackerEnabled = True # 是否开启人脸跟踪
        self.isFaceRecognizerEnabled = False    # 是否开启人脸识别

        self.confidenceThreshold = 50   #置信度
        self.autoAlarmThreshold = 65    #阈值


    # 是否开启人脸跟踪
    def enableFaceTracker(self, coreUI):
        if coreUI.checkBox_track.isChecked():
            self.isFaceTrackerEnabled = True
        else:
            self.isFaceTrackerEnabled = False

    # 是否开启人脸识别
    def enableFaceRecognizer(self, coreUI):
        if coreUI.checkBox_face_recognition.isChecked():
            if self.isFaceTrackerEnabled:
                self.isFaceRecognizerEnabled = True
            else:
                Fe_recognition.logQueue.put('Error：操作失败，请先开启人脸跟踪')
                coreUI.checkBox_face_recognition.setCheckState(qc.Qt.Unchecked)
                coreUI.checkBox_face_recognition.setChecked(False)
        else:
            self.isFaceRecognizerEnabled = False
            # coreUI.statusBar().showMessage('人脸识别：关闭')


    def run(self):
        faceCascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')

        # 帧数、人脸ID初始化
        frameCounter = 0
        currentFaceID = 0

        # 人脸跟踪器字典初始化
        faceTrackers = {}

        isTrainingDataLoaded = False
        con_mysql(self) #数据库

        while self.isRunning:
            if Fe_recognition.cap.isOpened():
                ret, frame = Fe_recognition.cap.read()#读取图像
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#灰度化图像，提高识别率
                # 检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸
                # 其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为构成检测目标的相邻矩形的最小个数，minSize限制目标区域范围
                faces = faceCascade.detectMultiScale(gray, 1.3, 5, minSize=(90, 90))

                # 预加载数据文件
                if not isTrainingDataLoaded and os.path.isfile(Fe_recognition.trainingData):
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    recognizer.read(Fe_recognition.trainingData)
                    isTrainingDataLoaded = True
                cursor = self.cur
                conn = self.connection

                captureData = {}
                realTimeFrame = frame.copy()

                # 人脸跟踪
                if self.isFaceTrackerEnabled:

                    # 要删除的人脸跟踪器列表初始化
                    fidsToDelete = []

                    for fid in faceTrackers.keys():
                        # 实时跟踪
                        trackingQuality = faceTrackers[fid].update(realTimeFrame)
                        # 如果跟踪质量过低，删除该人脸跟踪器
                        if trackingQuality < 7:
                            fidsToDelete.append(fid)

                    # 删除跟踪质量过低的人脸跟踪器
                    for fid in fidsToDelete:
                        faceTrackers.pop(fid, None)

                    for (_x, _y, _w, _h) in faces:
                        isKnown = False

                        if self.isFaceRecognizerEnabled:
                            cv2.rectangle(realTimeFrame, (_x, _y), (_x + _w, _y + _h), (232, 138, 30), 2)
                            face_id, confidence = recognizer.predict(gray[_y:_y + _h, _x:_x + _w])
                            logging.debug('face_id：{}，confidence：{}'.format(face_id, confidence))

                            # 从数据库中获取识别人脸的身份信息
                            try:
                                cursor.execute("select * from pes_show where face_id = '" + str(face_id) + "'")
                                result = cursor.fetchall()
                                if (len(result)==0):
                                    cursor.execute("select * from ad_show where face_id = '" + str(face_id) + "'")
                                    result1 = cursor.fetchall()
                                    if(len(result1)==0):
                                        raise Exception
                                    else:
                                        en_name = result1[0][0]
                                else:
                                    en_name = result[0][0]
                            except Exception as e:
                                logging.error('读取数据库异常，系统无法获取Face ID为{}的身份信息'.format(face_id))
                                Fe_recognition.logQueue.put('Error：读取数据库异常，系统无法获取Face ID为{}的身份信息'.format(face_id))
                                en_name = ''

                            # 若置信度评分小于置信度阈值，认为是可靠识别
                            if confidence < self.confidenceThreshold:
                                isKnown = True
                                cv2.putText(realTimeFrame, en_name, (_x - 5, _y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                            (0, 97, 255), 2)
                            else:
                                # 若置信度评分大于置信度阈值，该人脸可能是陌生人
                                cv2.putText(realTimeFrame, 'unknown', (_x - 5, _y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                            (0, 0, 255), 2)

                        # 帧数自增
                        frameCounter += 1

                        # 每读取10帧，检测跟踪器的人脸是否还在当前画面内
                        if frameCounter % 10 == 0:
                            # 这里必须转换成int类型，因为OpenCV人脸检测返回的是numpy.int32类型，
                            # 而dlib人脸跟踪器要求的是int类型
                            x = int(_x)
                            y = int(_y)
                            w = int(_w)
                            h = int(_h)

                            # 计算中心点
                            x_bar = x + 0.5 * w
                            y_bar = y + 0.5 * h

                            # matchedFid表征当前检测到的人脸是否已被跟踪
                            matchedFid = None

                            for fid in faceTrackers.keys():
                                # 获取人脸跟踪器的位置
                                # tracked_position 是 dlib.drectangle 类型，用来表征图像的矩形区域，坐标是浮点数
                                tracked_position = faceTrackers[fid].get_position()
                                # 浮点数取整
                                t_x = int(tracked_position.left())
                                t_y = int(tracked_position.top())
                                t_w = int(tracked_position.width())
                                t_h = int(tracked_position.height())

                                # 计算人脸跟踪器的中心点
                                t_x_bar = t_x + 0.5 * t_w
                                t_y_bar = t_y + 0.5 * t_h

                                # 如果当前检测到的人脸中心点落在人脸跟踪器内，且人脸跟踪器的中心点也落在当前检测到的人脸内
                                # 说明当前人脸已被跟踪
                                if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and
                                        (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
                                    matchedFid = fid

                            # 如果当前检测到的人脸是陌生人脸且未被跟踪
                            if not isKnown and matchedFid is None:
                                # 创建一个人脸跟踪器
                                tracker = dlib.correlation_tracker()
                                # 锁定跟踪范围
                                tracker.start_track(realTimeFrame, dlib.rectangle(x - 5, y - 10, x + w + 5, y + h + 10))
                                # 将该人脸跟踪器分配给当前检测到的人脸
                                faceTrackers[currentFaceID] = tracker
                                # 人脸ID自增
                                currentFaceID += 1

                    # 使用当前的人脸跟踪器，更新画面，输出跟踪结果
                    for fid in faceTrackers.keys():
                        tracked_position = faceTrackers[fid].get_position()

                        t_x = int(tracked_position.left())
                        t_y = int(tracked_position.top())
                        t_w = int(tracked_position.width())
                        t_h = int(tracked_position.height())

                        # 在跟踪帧中圈出人脸
                        cv2.rectangle(realTimeFrame, (t_x, t_y), (t_x + t_w, t_y + t_h), (0, 0, 255), 2)
                        cv2.putText(realTimeFrame, 'tracking...', (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                                    2)

                captureData['originFrame'] = frame
                captureData['realTimeFrame'] = realTimeFrame
                Fe_recognition.captureQueue.put(captureData)

            else:
                continue

    # 停止OpenCV线程
    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()



def InitUi(self):
    self.setupUi(self)
    self._translate = qc.QCoreApplication.translate
def con_mysql(self):
    self.connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                      database='students',
                                      charset='utf8')
    print('successfully connect')
    self.cur = self.connection.cursor()

