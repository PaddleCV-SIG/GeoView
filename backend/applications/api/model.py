import os

from flask import Blueprint

from applications.common.utils.http import success_api, fail_api
from applications.interface.utils import get_model_info

model_api = Blueprint('model_api', __name__, url_prefix='/api/model')


@model_api.get('/list/<string:model_type>')
def get_model_list(model_type):
    types_list = {
        "change_detector": "change_detector",
        "classification": "classifier",
        "image_restoration": "restorer",
        "object_detector": "detector",
        "semantic_segmentation": "segmenter"
    }
    if model_type not in types_list:
        return fail_api("模型类型不正确")
    model_list = []
    for dirname in os.listdir("model/{}".format(model_type)):
        try:
            model_info = get_model_info("model/{}/{}".format(model_type,
                                                             dirname))
            if model_info["_Attributes"]["model_type"] == types_list[
                    model_type]:
                model_list.append({
                    "model_path": "model/{}/{}".format(model_type, dirname),
                    "model_type": model_info["_Attributes"]["model_type"],
                    "model_name": model_info["Model"]
                })
        except:
            pass
    return success_api(data=model_list)
