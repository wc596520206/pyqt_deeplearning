import sys, os
sys.path.append("..")
from PyQt5.QtWidgets import QTableWidgetItem
import json

from view.untitled import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from util import split_data, mkdir_file_path
from modelCode.InferModel import InferModel
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

# 完成模型训练功能
class p3(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(p3, self).__init__()
        self.setupUi(self)
        self.my_timer = QTimer()  # 创建定时器
        self.my_timer.timeout.connect(self.my_timer_cb)  # 创建定时器任务
        '''按钮状态控制'''
        self.btn_status = False
        #self.loadModel() #导入模型

    # 停止摄像头
    def cameraStop(self):
        pass

    # 导入已经训练好的模型
    def loadModel(self):
        with open(self.new_model_config_file, "r", encoding="UTF-8") as fr:
            model_config = json.load(fr)
        self.inferModel = InferModel(model_config)
        msg = QMessageBox()
        msg.setText("导入成功")
        msg.exec()


    # 摄像头开始或关闭
    def cameraStart(self):
        if self.btn_status:
            self.btn_status = False
        else:
            self.btn_status = True
        if self.btn_status:
            self.pushButton.setText('暂停')
            self.my_timer.start(40)  # 25fps
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # start camera
        else:
            self.pushButton.setText('开始')
            self.label.clear()  # 清楚label内容
            self.my_timer.stop()  # 停止定时器
            self.cap.release()  # 关闭摄像头

    # 推断模型
    def infer(self,image):
        label, score = self.inferModel.infer_model(image)
        string1 = str(label) +":"+ str(round(score, 3))
        print(string1)
        self.textEdit_4.setText(string1)


    def my_timer_cb(self):
        if self.cap:
            """图像获取"""
            ret, image = self.cap.read()
            show = cv2.resize(image, (self.label_7.width(), self.label_7.height()))
            show = cv2.flip(show, 1)
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)

            """结果呈现"""
            showImage = QImage(show.data, show.shape[1], show.shape[0],  show.shape[1] * 3,QImage.Format_RGB888)
            self.label_7.setPixmap(QPixmap.fromImage(showImage))
            self.infer(image)