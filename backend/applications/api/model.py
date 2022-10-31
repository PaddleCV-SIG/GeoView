import os

from flask import Blueprint

from applications.common.utils.http import success_api, fail_api
from applications.interface.utils import get_model_info

model_api = Blueprint('model_api', __name__, url_prefix='/api/model')


@model_api.get('/list/<string:model_type>')
def get_model_list(model_type):
    types_list = {
        "change_detection": "change_detector",
        "classification": "classifier",
        "image_restoration": "restorer",
        "object_detection": "detector",
        "semantic_segmentation": "segmenter"
    }
    if model_type not in types_list:
        return fail_api("模型类型不正确")
    model_list = []
    if os.path.exists("model/{}".format(model_type)):
        for dirname in os.listdir("model/{}".format(model_type)):
            if not os.path.isdir("model/{}/{}".format(model_type, dirname)):
                continue
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
                return fail_api("model/{}/{}下存放的模型格式非法，请检查".format(model_type,
                                                                   dirname))
    return success_api(data=model_list)
