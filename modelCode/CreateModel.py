import tensorflow as tf


class CreateModel(object):
    def __init__(self, config):
        self.model_type = config["global"]["model_type"]
        self.im_size = config["global"]["im_size"]
        self.class_num = config["global"]["class_num"]

    def create(self):
        # 搭建模型
        if self.model_type == "MobileNet":
            conv_base = tf.keras.applications.MobileNet(input_shape=(self.im_size, self.im_size, 3),
                                                        weights='imagenet',
                                                        include_top=False)
        elif self.model_type == "Xception":
            conv_base = tf.keras.applications.Xception(
                weights='imagenet',
                include_top=False)
        elif self.model_type == "ResNet50":
            conv_base = tf.keras.applications.ResNet50(
                weights='imagenet',
                include_top=False)
        conv_base.trainable = True
        # 构建模型
        model = tf.keras.models.Sequential()
        model.add(conv_base)
        model.add(tf.keras.layers.GlobalAveragePooling2D())
        model.add(tf.keras.layers.Dense(self.class_num, activation='relu'))  # 最后全连接层
        model.summary()  # 每层参数信息
        return model
