
import numpy as np
import cv2
from modelCode.CreateModel import CreateModel


class InferModel(object):
    def __init__(self, config):
        createModel = CreateModel(config)
        self.im_size = config["global"]["im_size"]
        self.label_dict = config["label_dict"]
        model_file_path = config["train"]["model_file_path"]
        self.model = createModel.create()
        self.model.load_weights(model_file_path)

    def infer_model(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.im_size, self.im_size), cv2.INTER_LINEAR) / 255
        image = np.expand_dims(image, 0)
        score = self.model.predict(image)[0]
        label_dict = {int(k): v for k, v in self.label_dict.items()}
        label = label_dict[np.argmax(score)]
        score = max(score)
        return label, score

    #  后处理
    def pos_process(self):
        pass
