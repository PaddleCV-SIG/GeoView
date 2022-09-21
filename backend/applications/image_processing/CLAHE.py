import os.path as osp

import cv2

from applications.common.path_global import md5_name


def CLAHE(src_dir, save_dir, names):
    temps = list()
    for name in names:
        Gn = cv2.imread(osp.join(src_dir, name))
        B, G, R = cv2.split(Gn)
        clahe = cv2.createCLAHE(
            clipLimit=2, tileGridSize=(8, 8))  # 调节第二个参数可以控制力度大小
        clahe_B = clahe.apply(B)
        clahe_G = clahe.apply(G)
        clahe_R = clahe.apply(R)
        clahe_result = cv2.merge((clahe_B, clahe_G, clahe_R))
        new_name = md5_name(name)
        cv2.imwrite(osp.join(save_dir, new_name), clahe_result)
        temps.append(new_name)
    return temps
