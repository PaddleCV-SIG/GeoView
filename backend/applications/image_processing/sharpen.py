import os.path as osp

import cv2
import numpy as np

from applications.common.path_global import md5_name


def sharpen(src_dir, save_dir, names):  # src_dir为原图文件夹，save_dir为保存结果的文件夹路径
    temps = list()
    for name in names:
        im = cv2.imread(osp.join(src_dir, name))
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=int)
        im = cv2.filter2D(im, -1, kernel)
        new_name = md5_name(name)
        cv2.imwrite(osp.join(save_dir, new_name), im)
        temps.append(new_name)
    return temps


# # 4邻域模板与8邻域模板
# kernel_4 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=int)
# kernel_8 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]], dtype=int)
