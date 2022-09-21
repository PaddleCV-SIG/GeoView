import os.path as osp

import cv2
from skimage import morphology

from applications.common.path_global import md5_name


def hole_fill(src_dir, save_dir, names):  # src_dir为待处理文件夹名称，save_dir为储存结果的文件夹名称
    temps = list()
    for name in names:
        img = cv2.imread(osp.join(src_dir, name))
        # 转换为灰度图
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 转换为二值图
        ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        # 转换为布尔值
        thresh1 = thresh1 > 1
        # 去除外部噪点
        stage1 = morphology.remove_small_objects(
            thresh1, min_size=256, connectivity=2)
        # 去除内部孔洞，注意到第二个参数为area_threshold,而不是min_size
        stage2 = morphology.remove_small_holes(
            stage1, area_threshold=5000, connectivity=1)
        stage2 = stage2.astype('uint8')
        stage2 = cv2.cvtColor(stage2 * 255, cv2.COLOR_GRAY2RGB)
        new_name = md5_name(name)
        cv2.imwrite(osp.join(save_dir, new_name), stage2)
        temps.append(new_name)
    return temps
