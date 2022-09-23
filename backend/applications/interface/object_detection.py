# 导入需要用到的库
import os.path as osp

import cv2
import numpy as np
import paddle
import paddlers as pdrs
from paddlers.tasks.utils.visualize import visualize_detection
from skimage.io import imsave

from applications.common.path_global import md5_name, generate_url


def read_rgb(path):
    im = cv2.imread(path)
    im = im[..., ::-1]
    return im


def execute(model_path, data_path, out_dir, names):
    """

    :param model_path: 模型路径
    :param data_path: 数据文件夹路径，里面只包含图片
    :param out_dir: 结果保存路径
    :return: None
    """
    # names = listdir(data_path)
    # 对文件名进行排序，以确保多次运行结果一致
    # names.sort()
    image_list = [osp.join(data_path, name) for name in names]
    predictor = pdrs.deploy.Predictor(model_dir=model_path, use_gpu=True)
    pred = predictor.predict(image_list)
    print('预测完毕！')
    # 参考 https://stackoverflow.com/a/68209152
    # 读取输入影像
    ims = [read_rgb(i) for i in image_list]
    temps = list()
    # 绘制目标框
    with paddle.no_grad():
        for idx, im in zip(range(len(names)), ims):
            im = cv2.resize(
                im[..., ::-1], (608, 608), interpolation=cv2.INTER_CUBIC)
            vis = im
            # 用绿色画出预测目标框
            if len(pred[idx]) > 0:
                vis = visualize_detection(
                    np.array(vis),
                    pred[idx],
                    color=np.asarray(
                        [[0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0]],
                        dtype=np.uint8),
                    threshold=0.2,
                    save_dir=None)
            vis = cv2.cvtColor(vis, cv2.COLOR_RGB2BGR)
            name = names[idx]
            new_name = md5_name(name)
            imsave(osp.join(out_dir, new_name), vis)
            temps.append(generate_url + new_name)
    return temps
