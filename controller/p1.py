import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtGui import QPixmap
import uuid
import os
import shutil
from PyQt5.QtWidgets import QMessageBox
from view.untitled import Ui_MainWindow


# 完成数据导入功能
class p1(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(p1, self).__init__()
        # super().__init__()
        self.setupUi(self)

    def load(self):
        filenames, _ = QFileDialog.getOpenFileNames(self.centralwidget, '打开文件', QDir.currentPath())
        self.tableWidget.setRowCount(len(filenames))
        for i, filename in enumerate(filenames):
            item_name = QTableWidgetItem(filename)
            # item_name.setFlags(QtCore.Qt.ItemFlag(1)) # 是否可编辑
            self.tableWidget.setItem(i, 0, item_name)
        self.tableWidget.show()

    # 单击列表文件路径，将文件显示在图像显示区域
    def show_image(self, Item):
        filename = Item.text()
        self.row = Item.row()  # 返回显示的是第几行的元素
        jpg = QtGui.QPixmap(filename)  # .scaled(self.graphicsView.width(), self.graphicsView.height())
        self.item = QGraphicsPixmapItem(jpg)  # 创建像素图元
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)  # 将场景添加至视图
        self.graphicsView.fitInView(QGraphicsPixmapItem(QPixmap(filename)))

    # 输入类别，将文本信息返回到table的第二列
    # todo 需要判断是否有内容
    def imageclass(self):
        category = self.textEdit.toPlainText()
        if category not in self.category_dict.keys():
            self.category_dict[category] = 1
        else:
            self.category_dict[category] += 1
        category = QTableWidgetItem(category)
        self.tableWidget.setItem(self.row, 1, category)
        self.tableWidget.show()

    # 保存
    def save(self):
        self.uuid_str = uuid.uuid4().hex  # 随机生成文件夹名字
        #self.uuid_str = "ec6dec3699684aeeb075ec5023a661e3"
        uuid_data_path = os.path.join("data", self.uuid_str)
        if not os.path.exists(uuid_data_path):
            os.mkdir(uuid_data_path)
        for key in self.category_dict.keys():
            path = os.path.join(uuid_data_path, str(key))
            if not os.path.exists(path):
                os.mkdir(path)
        for row in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(row, 0) and self.tableWidget.item(row, 1):
                src = self.tableWidget.item(row, 0).text()
                category = self.tableWidget.item(row, 1).text()
                file_name = os.path.basename(src)
                dst = uuid_data_path + "//" + str(category) + "//" + file_name
                shutil.copy(src, dst)

        msg = QMessageBox()
        msg.setText("保存完成")
        msg.exec()

    # 显示信息
    def info(self):
        msg = QMessageBox()
        str1 = "类别：数量 \n"
        for key, value in self.category_dict.items():
            str1 += key + ":" + str(value) + "\n"
        msg.setText(str1)
        msg.exec()

    # 删除需要重新写
    def clear(self):
        pass

