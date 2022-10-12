# 导入需要用到的库
import os.path as osp

import paddle
import numpy as np
from skimage.io import imsave
from paddlers.models.ppdet.utils.colormap import colormap

import paddlers as pdrs
from paddlers.transforms import decode_image
from paddlers.tasks.utils.visualize import visualize_detection

from applications.common.path_global import md5_name, generate_url


def execute(model_path, data_path, out_dir, names, threshold=0.2):
    """
    :param model_path: 模型路径
    :param data_path: 数据文件夹路径，里面只包含图片
    :param out_dir: 结果保存路径
    :param names: 待处理文件名列表
    :param threshold: 阈值
    """
    image_list = [osp.join(data_path, name) for name in names]
    predictor = pdrs.deploy.Predictor(model_dir=model_path, use_gpu=True)
    pred = predictor.predict(image_list)
    # 读取输入影像
    ims = [decode_image(i) for i in image_list]
    temps = list()
    # 绘制目标框
    with paddle.no_grad():
        for idx, im in zip(range(len(names)), ims):
            vis = im
            # 绘制预测目标框
            if len(pred[idx]) > 0:
                vis = visualize_detection(
                    np.array(vis),
                    pred[idx],
                    threshold=threshold,
                    save_dir=None)
            name = names[idx]
            new_name = md5_name(name)
            imsave(osp.join(out_dir, new_name), vis)
            temps.append(generate_url + new_name)
    return temps
