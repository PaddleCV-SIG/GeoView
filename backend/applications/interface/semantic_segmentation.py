import os.path as osp
from collections import Counter

import cv2
import numpy as np
import paddlers as pdrs
from paddlers.tasks.utils.visualize import get_color_map_list
from skimage.io import imsave

from applications.common.path_global import md5_name, generate_url


def get_lut(classes_num):
    lut = np.zeros((256, 3), dtype=np.uint8)
    lut[0:classes_num] = get_color_map_list(classes_num + 1)[1:]  # +1是为了去掉黑色
    print(lut)
    return lut


def execute(model_path, data_path, out_dir, test_names):
    image_list = [osp.join(data_path, name) for name in test_names]
    predictor = pdrs.deploy.Predictor(model_path, use_gpu=True)
    pred = predictor.predict(image_list)
    ims = [i['label_map'] for i in pred]
    temps = list()
    for idx, im in zip(range(len(image_list)), ims):
        im = get_lut(np.max(im) + 1)[im]
        new_name = md5_name(test_names[idx])
        imsave(osp.join(out_dir, new_name), im)
        temps.append(generate_url + new_name)
    return temps
