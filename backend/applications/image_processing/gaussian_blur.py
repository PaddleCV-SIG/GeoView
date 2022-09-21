import os.path as osp

import cv2

from applications.common.path_global import md5_name


def gaussian_blur(src_dir, save_dir,
                  names):  # src_dir为原图文件夹，save_dir为保存结果的文件夹路径
    temps = list()
    for name in names:
        Gn = cv2.imread(osp.join(src_dir, name))
        Gf = cv2.GaussianBlur(Gn, (3, 3), 0, 0)
        new_name = md5_name(name)
        cv2.imwrite(osp.join(save_dir, new_name), Gf)  # 第一个参数为保存地址，第二个参数Gf为处理结果
        temps.append(new_name)
    return temps
