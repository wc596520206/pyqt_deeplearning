import sys, os
sys.path.append("..")
from PyQt5.QtWidgets import QTableWidgetItem
import json

from view.untitled import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from util import split_data, mkdir_file_path
from modelCode.TrainModel import train_script
from PyQt5.QtWidgets import QMessageBox

# 完成模型训练功能
class p2(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(p2, self).__init__()
        self.setupUi(self)

    # 导入类别信息
    def load_data(self):
        self.tableWidget_2.setRowCount(len(self.category_dict))
        for i, key in enumerate(self.category_dict.keys()):
            value = self.category_dict[key]
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(str(value))
            self.tableWidget_2.setItem(i, 0, key_item)
            self.tableWidget_2.setItem(i, 1, value_item)
        self.tableWidget_2.show()


    def config_model_file(self, train_path, dev_path):
        model_config_file = os.path.join("model", self.uuid_str)
        mkdir_file_path(model_config_file)
        with open("resources/model_config.json", "r", encoding="UTF-8") as fr:
            model_config = json.load(fr)
        model_config["train"]["train_dir"] = train_path
        model_config["train"]["validation_dir"] = dev_path
        model_config["global"]["log_path"] = os.path.join(model_config_file, "log.json")
        model_config["train"]["model_file_path"] = model_config_file +"//" +"xxx.hdf5"
        model_config["global"]["class_ch"] = list(self.category_dict.keys())
        model_config["global"]["class_num"] = len(self.category_dict.keys())
        label_index_dict = {}
        for i, key in enumerate(self.category_dict.keys()):
            label_index_dict[i] = key

        model_config["label_dict"] = label_index_dict
        new_model_config_file = os.path.join(model_config_file, "model_config.json")
        with open(new_model_config_file, "w", encoding="UTF-8") as fout:
            json.dump(model_config, fout, indent=4, ensure_ascii=False)
        return  new_model_config_file

    # 获取信息，todo 需要完善，将参数都写入json配置文件中。
    def get_info(self):
        #mode = self.textEdit_2.toPlainText()
        self.train_data_ratio = float(self.textEdit_3.toPlainText())


    def train(self):
        #0 获取参数
        self.get_info()

        #1 划分数据
        uuid_data_path = os.path.join("data", self.uuid_str)
        train_path, dev_path = split_data(uuid_data_path, self.train_data_ratio)
        msg = QMessageBox()
        msg.setText("数据集划分完成")
        msg.exec()

        #2 配置参数
        self.new_model_config_file = self.config_model_file(train_path, dev_path)

        # # 3 开始训练
        train_script(self.new_model_config_file)
        msg = QMessageBox()
        msg.setText("模型保存成功")
        msg.exec()



