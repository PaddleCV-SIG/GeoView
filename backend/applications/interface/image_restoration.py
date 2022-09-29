import os.path as osp

from skimage.io import imsave

import paddlers as pdrs

from applications.common.path_global import generate_url


def execute(model_path, data_path, out_dir, names):
    """
        :param model_path: 模型路径
        :param data_path: 数据文件夹路径，里面只包含图片
        :param out_dir: 结果保存路径
        :param names: 待处理文件名列表
    """
    temps = list()
    image_list = [osp.join(data_path, name) for name in names]
    predictor = pdrs.deploy.Predictor(model_dir=model_path, use_gpu=True)
    pred = predictor.predict(image_list)
    imgs = [im['res_map'] for im in pred]
    for name, im in zip(names, imgs):
        imsave(osp.join(out_dir, name), im)
        temps.append(generate_url + name)
    return temps
