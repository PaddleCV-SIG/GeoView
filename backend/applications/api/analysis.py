import json
import os

import cv2
from flask import Blueprint, request
from sqlalchemy import desc

from applications.common.curd import model_to_dicts
from applications.common.path_global import up_dir, generate_dir, fun_type_1, fun_type_4, fun_type_5, fun_type_3, \
    fun_type_2, generate_url
from applications.common.utils import type_utils
from applications.common.utils.http import fail_api, success_api, table_api
from applications.common.utils.type_utils import items_handle
from applications.common.utils.upload import img_url_handle
from applications.extensions import db
from applications.image_processing import histogram_match
from applications.interface.analysis import change_detection, object_detection, terrain_classification, hole_handle, \
    handle, classification, image_restoration
from applications.interface.compute_variation import compute_variation
from applications.interface.draw_mask import draw_masks
from applications.interface.utils import get_model_info
from applications.models.analysis import Analysis
from applications.schemas import AnalysisSchema

analysis_api = Blueprint('analysis_api', __name__, url_prefix='/api/analysis')
"""
    结果展示
"""


@analysis_api.get('/show/<string:type>')
def show_result(type):
    # orm查询
    # 使用分页获取data需要.items
    to_type = type_utils.str_to_type(type)
    log = Analysis.query.filter_by(
        type=to_type).order_by(desc(Analysis.create_time)).layui_paginate()
    log_items = log.items
    items_handle(log_items)
    count = log.total
    return table_api(
        data=model_to_dicts(
            schema=AnalysisSchema, data=log_items), count=count)


"""
    变化检测
"""


@analysis_api.post('/change_detection')
def change_detection_api():
    req_json = request.json
    model_path = req_json["model_path"]
    try:
        model_info = get_model_info(model_path)
        if model_info["_Attributes"]["model_type"] != "change_detector":
            return fail_api("模型类型不正确，请检查")
    except:
        return fail_api("模型不存在，请检查")
    list_ = req_json["list"]
    step1_ = req_json["prehandle"]
    step2_ = req_json["denoise"]
    if step1_ is None or step1_ is None or step1_ not in (
            0, fun_type_1, fun_type_4) or step2_ not in (0, fun_type_3,
                                                         fun_type_5):
        return fail_api("参数异常")
    if list_ is None:
        return fail_api("请上传图片")

    for pair in list_:
        if "first" not in pair or "second" not in pair or pair[
                "first"] == "" or pair["second"] == "":
            return fail_api("请求参数异常")
    print("----------------->change_detection" + json.dumps(req_json))
    type_ = 1
    change_detection(model_path, up_dir, generate_dir, list_, step1_, step2_,
                     type_)
    return success_api()


"""
    目标检测
"""


@analysis_api.post('/object_detection')
def object_detection_api():
    req_json = request.json
    model_path = req_json["model_path"]
    try:
        model_info = get_model_info(model_path)
        if model_info["_Attributes"]["model_type"] != "detector":
            return fail_api("模型类型不正确，请检查")
    except:
        return fail_api("模型不存在，请检查")
    list_ = req_json["list"]
    step1_ = req_json["prehandle"]
    step2_ = req_json["denoise"]
    if step1_ is None or step1_ is None or step1_ not in (
            0, fun_type_2, fun_type_4) or step2_ not in (0, fun_type_3,
                                                         fun_type_5):
        return fail_api("参数异常")
    if list_ is None:
        return fail_api("请上传图片")
    type_ = 2
    object_detection(model_path, up_dir, generate_dir, list_, step1_, step2_,
                     type_)

    return success_api()


"""
    地物分类
"""


@analysis_api.post('/semantic_segmentation')
def semantic_segmentation_api():
    req_json = request.json
    model_path = req_json["model_path"]
    try:
        model_info = get_model_info(model_path)
        if model_info["_Attributes"]["model_type"] != "segmenter":
            return fail_api("模型类型不正确，请检查")
    except:
        return fail_api("模型不存在，请检查")
    list_ = req_json["list"]
    step1_ = req_json["prehandle"]
    step2_ = req_json["denoise"]
    if step1_ is None or step1_ is None or step1_ not in (
            0, fun_type_2, fun_type_4) or step2_ not in (0, fun_type_3,
                                                         fun_type_5):
        return fail_api("参数异常")
    if list_ is None:
        return fail_api("请上传图片")
    type_ = 3
    terrain_classification(model_path, up_dir, generate_dir, list_, step1_,
                           step2_, type_)
    return success_api()


"""
    场景分类
"""


@analysis_api.post('/classification')
def classification_api():
    req_json = request.json
    model_path = req_json["model_path"]
    try:
        model_info = get_model_info(model_path)
        if model_info["_Attributes"]["model_type"] != "classifier":
            return fail_api("模型类型不正确，请检查")
    except:
        return fail_api("模型不存在，请检查")
    img_list = req_json["list"]
    if img_list is None:
        return fail_api("请上传图片")
    type_ = 4
    classification(model_path, up_dir, img_list, type_)
    return success_api()


"""
    图像还原
"""


@analysis_api.post('/image_restoration')
def image_restoration_api():
    req_json = request.json
    model_path = req_json["model_path"]
    try:
        model_info = get_model_info(model_path)
        if model_info["_Attributes"]["model_type"] != "restorer":
            return fail_api("模型类型不正确，请检查")
    except:
        return fail_api("模型不存在，请检查")
    img_list = req_json["list"]
    if img_list is None:
        return fail_api("请上传图片")
    type_ = 5
    image_restoration(model_path, up_dir, generate_dir, img_list, type_)
    return success_api()


"""
    直图处理
"""


@analysis_api.post('/histogram_match')
def pre_handle():
    req_json = request.json
    list_ = req_json["list"]
    step1_ = req_json["prehandle"]
    if list_ is None:
        return fail_api("请上传图片")
    if step1_ not in (1, 4):
        return fail_api("请求参数异常")
    for pair in list_:
        if "first" not in pair or "second" not in pair or pair[
                "first"] == "" or pair["second"] == "":
            return fail_api("请求参数异常")
        pair["first"] = img_url_handle(pair["first"])
        pair['second'] = img_url_handle(pair['second'])
    match = list()
    if step1_ == fun_type_1:
        match = histogram_match.gram_match(list_, up_dir, generate_dir)
    else:
        for pair in list_:
            temps = [pair["first"], pair["second"]]
            imgs1 = handle(fun_type_4, temps, up_dir, generate_dir)
            match.append({
                "first": generate_url + imgs1[0],
                "second": generate_url + imgs1[1]
            })
    return success_api(data=match)


@analysis_api.post('/image_pre')
def image_pre():
    req_json = request.json
    list_ = req_json["list"]
    step1_ = req_json["prehandle"]
    type = req_json["type"]
    if list_ is None:
        return fail_api("请上传图片")
    if step1_ not in (2, 4):
        return fail_api("请求参数异常")
    imgs = list()
    if type == 1:
        for pair in list_:
            if "first" not in pair or "second" not in pair or pair[
                    "first"] == "" or pair["second"] == "":
                return fail_api("请求参数异常")
        for pair in list_:
            temps = [
                img_url_handle(pair["first"]), img_url_handle(pair["second"])
            ]
            imgs1 = handle(fun_type_4, temps, up_dir, generate_dir)
            imgs.append({
                "first": pair["first"],
                "first1": imgs1[0],
                "second": pair["second"],
                "second1": imgs1[1]
            })
    else:
        temps = list()
        for pair in list_:
            temps.append(img_url_handle(pair))
        imgs = handle(step1_, temps, up_dir, generate_dir)
        for i, img in enumerate(imgs):
            imgs[i] = generate_url + img
    return success_api(data=imgs)


"""
    孔洞处理
"""


@analysis_api.post('/hole')
def hole_handle1():
    req_json = request.json
    analysis_id = req_json["id"]
    if analysis_id is None:
        return fail_api("参数异常")

    analysis = Analysis.query.filter_by(id=analysis_id, type=1).first()
    if not analysis:
        return fail_api("这一组分析记录不存在")
    if analysis.type != 1:
        return fail_api("类型错误")
    if analysis.is_hole:
        return fail_api("这一组分析记录已经孔洞处理过")
    temps = list()
    temps.append(analysis.after_img)
    after_img, data = hole_handle(generate_dir, generate_dir, temps)
    old_data = json.loads(analysis.data)
    old_data.update(data)
    mask, count = draw_masks(
        os.path.join(generate_dir, os.path.basename(after_img)))
    cv2.imwrite(
        os.path.join(
            generate_dir,
            os.path.splitext(os.path.basename(after_img))[0] + "_mask.png"),
        mask)
    old_data["mask"] = generate_url + os.path.splitext(
        os.path.basename(after_img))[0] + "_mask.png"
    old_data["count"] = count
    old_data["fractional_variation"] = compute_variation(
        os.path.join(generate_dir, os.path.basename(after_img)))
    Analysis.query.filter_by(id=analysis_id).update({
        "after_img": after_img,
        "data": json.dumps(old_data),
        "is_hole": True
    })
    db.session.commit()
    return success_api()
