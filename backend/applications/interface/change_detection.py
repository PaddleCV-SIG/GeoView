import os
import os.path as osp

import numpy as np
from skimage.io import imsave

import paddlers as pdrs
from paddlers.transforms import decode_image

from applications.common.path_global import generate_url


def execute(model_path, data_path, out_dir, names, window_size=256, stride=128):
    image_list = [(osp.join(data_path, name["first"]), osp.join(data_path,
                                                                name["second"]))
                  for name in names]
    temps = list()  # 存储查看链接
    temps1 = list()  # 存储生成的图片名
    predictor = pdrs.deploy.Predictor(model_path, use_gpu=True)
    for image in image_list:
        predictor.slider_predict(
            image,
            save_dir=out_dir,
            transforms=None,
            block_size=window_size,  #注意block_size的值不能等于overlap的值
            overlap=window_size - stride,
            merge_strategy='accum')
    for name in names:
        raw_name = os.path.splitext(name["first"])[0] + ".tif"
        img = decode_image(osp.join(out_dir, raw_name))
        save_img = np.where(img == 0, img, 255)
        imsave(osp.join(out_dir, name["first"]), save_img)
        temps.append(generate_url + name["first"])
        temps1.append(name["first"])
        os.remove(osp.join(out_dir, raw_name))
    return temps, temps1
