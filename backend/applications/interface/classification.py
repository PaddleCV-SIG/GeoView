# 导入需要用到的库
import os.path as osp

import cv2
import paddlers as pdrs


def read_rgb(path):
    im = cv2.imread(path)
    im = im[..., ::-1]
    return im


def execute(model_path, data_path, names):
    image_list = [osp.join(data_path, name) for name in names]
    ims = [read_rgb(i) for i in image_list]
    predictor = pdrs.deploy.Predictor(model_path, use_gpu=True)
    temps = predictor.predict(ims)
    return temps
