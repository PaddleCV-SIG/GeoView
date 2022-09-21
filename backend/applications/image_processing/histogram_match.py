import os.path as osp

import cv2
import numpy as np

from applications.common.path_global import md5_name, generate_url


def gram_match(
        names, data_dir, save_dir, flag=True
):  # DATA_DIR为第一时期图文件夹，Matched_dir为匹配的图片文件夹(第二时期)，save_dir为将储存结果放置的文件夹名称
    # names = list(map(osp.basename, glob(osp.join(DATA_DIR,'*.png'))))
    print(names)
    temps = list()
    for name in names:
        print("gram_match->" + str(name))
        img = cv2.imread(osp.join(data_dir, name["first"]))
        ref = cv2.imread(osp.join(data_dir, name["second"]))
        out = np.zeros_like(img)
        _, _, colorChannel = img.shape
        for i in range(colorChannel):
            hist_img, _ = np.histogram(img[:, :, i], 256)  # get the histogram
            hist_ref, _ = np.histogram(ref[:, :, i], 256)
            cdf_img = np.cumsum(hist_img)  # get the accumulative histogram
            cdf_ref = np.cumsum(hist_ref)

            for j in range(256):
                tmp = abs(cdf_img[j] - cdf_ref)
                tmp = tmp.tolist()
                idx = tmp.index(
                    min(tmp)
                )  # find the smallest number in tmp, get the index of this number
                out[:, :, i][img[:, :, i] == j] = idx
        new_name = md5_name(str(name["first"]))
        cv2.imwrite(osp.join(save_dir, new_name), out)
        if flag:
            temps.append(generate_url + new_name)
        else:
            temps.append(new_name)
    return temps
