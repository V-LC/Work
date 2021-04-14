# -*- coding: utf-8 -*-
import pymysql
import queue
import cv2
import PyQt5.QtWidgets as qw
import logging
import os
import dlib



def run():
    trainingData = './recognizer/trainingData.yml'  # 训练集
    cap = cv2.VideoCapture()    #打开摄像头
    captureQueue = queue.Queue()  # 图像队列

    # 加载haarcascade文件来预测图像中的人脸
    faceCascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')

    # 帧数、人脸ID初始化
    frameCounter = 0
    currentFaceID = 0

    # 人脸跟踪器字典初始化
    faceTrackers = {}

    isFaceTrackerEnabled = True  # 是否开启人脸踪
    isFaceRecognizerEnabled = True  # 是否开启人脸识别

    isTrainingDataLoaded = False
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',
                                      database='students',
                                      charset='utf8')
    print('successfully connect')
    cursor = conn.cursor()

    confidenceThreshold = 50  # 置信度
    autoAlarmThreshold = 65  # 阈值

    isRunning = True    #是否继续识别
    en_name = ""
    re_data = ""

    #打开摄像头
    camID = 0
    cap.open(camID)
    #初始化识别时间
    time = 0
    while isRunning:
        time += 1
        if cap.isOpened():
            # print("hello")
            # 读取图像
            ret, frame = cap.read()
            # 灰度化
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 检测人脸，将每一帧摄像头记录的数据带入OpenCv中，让Classifier判断人脸
            # 其中gray为要检测的灰度图像，1.3为每次图像尺寸减小的比例，5为构成检测目标的相邻矩形的最小个数，minSize限制目标区域范围
            faces = faceCascade.detectMultiScale(gray, 1.3, 5, minSize=(90, 90))

            # 预加载数据文件
            if not isTrainingDataLoaded and os.path.isfile(trainingData):
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(trainingData)
                isTrainingDataLoaded = True

            captureData = {}
            realTimeFrame = frame.copy()

            # 人脸跟踪
            if isFaceTrackerEnabled:
                # 要删除的人脸跟踪器列表初始化
                fidsToDelete = []

                for fid in faceTrackers.keys():
                    # 实时跟踪
                    trackingQuality = faceTrackers[fid].update(realTimeFrame)#1
                    # 如果跟踪质量过低，删除该人脸跟踪器
                    if trackingQuality < 7:
                        fidsToDelete.append(fid)

                # 删除跟踪质量过低的人脸跟踪器
                for fid in fidsToDelete:
                    faceTrackers.pop(fid, None)

                # 框选人脸，for循环保证一个能检测的实时动态视频流
                for (_x, _y, _w, _h) in faces:
                    isKnown = False
                    if isFaceRecognizerEnabled:
                        cv2.rectangle(realTimeFrame, (_x, _y), (_x + _w, _y + _h), (232, 138, 30), 2)#2
                        face_id, confidence = recognizer.predict(gray[_y:_y + _h, _x:_x + _w])
                        logging.debug('face_id：{}，confidence：{}'.format(face_id, confidence))
                        # 从数据库中获取识别人脸的身份信息
                        try:
                            cursor.execute("select * from pes_show where face_id = '" + str(face_id) + "'")
                            result = cursor.fetchall()
                            if (len(result) == 0):
                                cursor.execute(
                                    "select * from ad_show where face_id = '" + str(face_id) + "'")
                                result1 = cursor.fetchall()
                                # print(result1)
                                if (len(result1) == 0):
                                    raise Exception
                                else:
                                    # re_data = result1
                                    # print(re_data)
                                    en_name = result1[0][0]
                            else:
                                en_name = result[0][0]

                        except Exception as e:
                            logging.error('读取数据库异常，系统无法获取Face ID为{}的身份信息'.format(face_id))
                            en_name = ''

                        # 若置信度评分小于置信度阈值，认为是可靠识别
                        if confidence < confidenceThreshold:
                            isKnown = True
                            cv2.putText(realTimeFrame, en_name, (_x - 5, _y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                        1,
                                        (0, 97, 255), 2)
                            re_data = en_name
                        else:
                            # 若置信度评分大于置信度阈值，该人脸可能是陌生人
                            cv2.putText(realTimeFrame, 'unknown', (_x - 5, _y - 10),    #4
                                        cv2.FONT_HERSHEY_SIMPLEX, 1,
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
                            tracker.start_track(realTimeFrame,
                                                dlib.rectangle(x - 5, y - 10, x + w + 5, y + h + 10))
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
                    cv2.putText(realTimeFrame, 'tracking...', (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                (0, 0, 255),
                                2)
                cv2.imshow("capture", realTimeFrame)

                # 按q退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # print(re_data)
                if re_data != "":
                    cursor.execute("select * from ad_show where 账号 = '" + re_data + "'")
                    judge = cursor.fetchall()
                    if(len(judge)!=0):
                        cv2.destroyAllWindows()
                        return "True"
                    cursor.execute("select * from pes_show where 工号 = '" + re_data + "'")
                    judge1 = cursor.fetchall()
                    if (len(judge1) != 0):
                        logging.error('错误，{}不是管理员！'.format(re_data))
                        cv2.destroyAllWindows()
                        return "False"
            captureData['originFrame'] = frame
            captureData['realTimeFrame'] = realTimeFrame
            captureQueue.put(captureData)

        else:
            continue
        if time > 300:  # 大约10秒识别时间
            logging.error('错误，无法识别管理员！')
            cv2.destroyAllWindows()
            return ""
    return en_name
