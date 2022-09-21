import os.path as osp

import cv2

from applications.common.path_global import md5_name


def resize(src_dir, save_dir, names,
           mode=0):  # 改变mode的值选择不同的resize方式，目标检测不用resize,直接把图丢进去就行
    temps = list()
    for name in names:
        img = cv2.imread(osp.join(src_dir, name))
        if mode == 0:
            img = cv2.resize(img, (1024, 1024))  # 变化检测选0
        if mode == 1:
            img = cv2.resize(img, (1500, 1500))  # 目标提取选1
        if mode == 2:
            img = cv2.resize(img, (512, 512))  # 地物分类选2
        if mode == 3:
            img = cv2.resize(img, (608, 608))
        new_name = md5_name(name)
        cv2.imwrite(osp.join(save_dir, new_name), img)
        temps.append(new_name)
    return temps


# Resize(r'D:\pictest\after',r'D:\pictest\resize',mode=2)    #测试
