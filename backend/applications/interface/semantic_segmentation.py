import os.path as osp
from collections import Counter

import cv2
import numpy as np
import paddlers as pdrs
from paddlers.tasks.utils.visualize import get_color_map_list
from skimage.io import imsave

from applications.common.path_global import md5_name, generate_url


def execute(model_path, data_path, out_dir, test_names):
    image_list = [osp.join(data_path, name) for name in test_names]
    predictor = pdrs.deploy.Predictor(model_path, use_gpu=True)
    pred = predictor.predict(image_list)
    ims = [i['label_map'] for i in pred]
    temps = list()
    lut = np.array(get_color_map_list(256))
    for idx, im in zip(range(len(image_list)), ims):
        im = lut[im]
        new_name = md5_name(test_names[idx])
        imsave(osp.join(out_dir, new_name), im)
        temps.append(generate_url + new_name)
    return temps
