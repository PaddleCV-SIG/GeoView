import os.path as osp

from skimage.io import imsave

import paddlers as pdrs


def execute(model_path, data_path, out_dir, names):
    image_list = [osp.join(data_path, name) for name in names]
    predictor = pdrs.deploy.Predictor(model_dir=model_path, use_gpu=True)
    pred = predictor.predict(image_list)
    imgs = [im['res_map'] for im in pred]
    for name, im in zip(names, imgs):
        imsave(osp.join(out_dir, name), im)
