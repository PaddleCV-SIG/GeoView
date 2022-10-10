import os.path as osp

import paddlers.utils.logging as logging
import yaml
from paddlers.transforms import build_transforms


def get_model_info(model_dir):
    if not osp.exists(model_dir):
        logging.error("Directory '{}' does not exist!".format(model_dir))
    if not osp.exists(osp.join(model_dir, "model.yml")):
        raise FileNotFoundError(
            "There is no file named model.yml in {}.".format(model_dir))
    with open(osp.join(model_dir, "model.yml")) as f:
        model_info = yaml.load(f.read(), Loader=yaml.Loader)
    return model_info


def load_transformer_from_file(model_dir, exclude=None):
    exclude = exclude or []
    model_info = get_model_info(model_dir)
    if 'Transforms' in model_info:
        transform = []
        for t in model_info['Transforms']:
            if len(t.keys()) > 0 and list(t.keys())[0] not in exclude:
                transform.append(t)
        return build_transforms(transform)
    return None
