# 训练模型
import sys, os
sys.path.append("..")
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.callbacks import ModelCheckpoint
import tensorflow as tf
import logging
from modelCode.CreateModel import CreateModel
import json
import os



class TrainModel(object):
    def __init__(self, config):
        self.logger = logging.getLogger('分类')
        self.im_size = config["global"]["im_size"]
        self.class_mode = config["global"]["class_mode"]
        self.lr = config["train"]["lr"]
        self.train_dir = config["train"]["train_dir"]
        self.validation_dir = config["train"]["validation_dir"]
        self.batch_size = int(config["train"]["batch_size"])
        self.loss = config["train"]["loss"]
        self.model_file_path = config["train"]["model_file_path"]
        self.epochs = int(config["train"]["epochs"])

        train_data_gen, total_train, val_data_gen, total_val = self.read_data()
        createModel = CreateModel(config)
        model = createModel.create()

        self.train_model(model, train_data_gen, total_train, val_data_gen, total_val)

    def read_data(self):
        # 读取数据
        # 定义训练集图像生成器，并进行图像增强
        train_image_generator = ImageDataGenerator(rescale=1. / 255,  # 归一化
                                                   )
        # 使用图像生成器从文件夹train_dir中读取样本，对标签进行one-hot编码
        train_data_gen = train_image_generator.flow_from_directory(directory=self.train_dir,
                                                                   batch_size=self.batch_size,
                                                                   shuffle=True,  # 打乱数据
                                                                   target_size=(self.im_size, self.im_size),
                                                                   class_mode=self.class_mode)
        # 训练集样本数
        total_train = train_data_gen.n
        # 定义验证集图像生成器，并对图像进行预处理
        validation_image_generator = ImageDataGenerator(rescale=1. / 255)  # 归一化
        # 使用图像生成器从验证集validation_dir中读取样本
        val_data_gen = validation_image_generator.flow_from_directory(directory=self.validation_dir,
                                                                      batch_size=self.batch_size,
                                                                      shuffle=False,  # 不打乱数据
                                                                      target_size=(self.im_size, self.im_size),
                                                                      class_mode=self.class_mode)
        total_val = val_data_gen.n
        return train_data_gen, total_train, val_data_gen, total_val

    def train_model(self, model, train_data_gen, total_train, val_data_gen, total_val):
        # 编辑模型
        model.compile(optimizer=tf.keras.optimizers.Adam(lr=self.lr),  # 使用adam优化器，学习率为0.0001
                      loss=self.loss,  # 交叉熵损失函数
                      metrics=["accuracy"])  # 评价函数

        # 回调函数
        checkpoint = ModelCheckpoint(self.model_file_path,
                                     monitor='val_acc',
                                     verbose=1,
                                     save_best_only=True)

        # 开始训练
        history = model.fit_generator(generator=train_data_gen,
                                      steps_per_epoch=total_train // self.batch_size,
                                      epochs=self.epochs,
                                      validation_data=val_data_gen,
                                      validation_steps=total_val // self.batch_size,
                                      callbacks=[checkpoint])
        return history


def train_script(model_file):
    with open(model_file, "r", encoding="UTF-8") as fr:
        config = json.load(fr)
    TrainModel(config)

if __name__ == '__main__':
    file_path = r"..\model\07567fce18804e329737a21b407eae14\model_config.json"
    train_script(file_path)