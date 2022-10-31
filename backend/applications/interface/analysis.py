import copy
import json
import os

import cv2

from applications.common.path_global import fun_type_1, fun_type_2, fun_type_3, fun_type_4, fun_type_5, \
    fun_type_6, fun_type_7, generate_url, fun_type_8, up_url, generate_dir
from applications.common.utils.upload import img_url_handle
from applications.extensions import db
from applications.image_processing import histogram_match
from applications.image_processing.CLAHE import CLAHE
from applications.image_processing.gaussian_blur import gaussian_blur
from applications.image_processing.hole import hole_fill
from applications.image_processing.median_blur import median_blur
from applications.image_processing.render import batch_render
from applications.image_processing.render_seg import batch_render_seg
from applications.image_processing.resize import resize
from applications.image_processing.sharpen import sharpen
from applications.interface import change_detection as CD
from applications.interface import classification as C
from applications.interface import object_detection as OD
from applications.interface import semantic_segmentation as SS
from applications.interface import image_restoration as IR
from applications.interface.compute_variation import compute_variation
from applications.interface.draw_mask import draw_masks
from applications.models.analysis import Analysis


def save_analysis(type_,
                  pic1,
                  retPic,
                  pic2="",
                  data="{}",
                  is_hole=False,
                  checked="0,0"):
    analysis = Analysis()

    analysis.type = type_
    analysis.before_img = pic1
    analysis.before_img1 = pic2
    analysis.after_img = retPic
    analysis.data = data
    analysis.is_hole = is_hole
    analysis.checked = checked
    db.session.add(analysis)
    db.session.commit()


def change_detection(model_path,
                     data_path,
                     out_dir,
                     names,
                     step1,
                     step2,
                     type_,
                     window_size=256,
                     stride=128):
    """
    变化检测
    :param model_path: 静态图模型路径
    :param data_path: 图片数据路径，路径中有名称为A和B的两个文件夹分别存储不同时相的图片（1024，1024），且相应图片名称相同
    :param out_dir:图片保存路径
    :param window_size:滑窗大小
    :param stride:步长
    :return:
    """
    print("变化检测----------------->start")
    imgs = list()
    imgs1 = list()
    temp_names = copy.deepcopy(names)
    for pair in names:
        pair["first"] = img_url_handle(pair["first"])
        pair['second'] = img_url_handle(pair['second'])
        imgs.append(pair["first"])
        imgs1.append(pair["second"])

    # 1.直图or锐化
    if step1 != 0:
        if step1 == fun_type_1:
            imgs = handle(step1, names, data_path, data_path)
        else:
            imgs = handle(step1, imgs, data_path, data_path)
            imgs1 = handle(step1, imgs1, data_path, data_path)
    # 2.平滑or滤波
    if step2 != 0:
        imgs = handle(step2, imgs, data_path, data_path)
        imgs1 = handle(step2, imgs1, data_path, data_path)

    # 3.resize
    resizes = resize(data_path, data_path, imgs, mode=0)
    resizes1 = resize(data_path, data_path, imgs1, mode=0)
    i = 0
    for pair in names:
        pair["first"] = resizes[i]
        pair["second"] = resizes1[i]
        i += 1
    # 3.检测对比，带地址的文件名，纯文件名
    retPics, filenames = CD.execute(
        model_path,
        data_path,
        out_dir,
        names,
        window_size=window_size,
        stride=stride)
    # 4.检测渲染
    res = handle(fun_type_6, filenames, out_dir, out_dir)
    # 5.入库
    i = 0
    for pair in temp_names:
        # first_ = pair["first"]
        first_ = up_url + resizes[i]
        second_ = pair['second']
        retPic = retPics[i]
        mask, count = draw_masks(os.path.join(out_dir, filenames[i]))
        cv2.imwrite(
            os.path.join(out_dir,
                         os.path.splitext(filenames[i])[0] + "_mask.png"), mask)
        res[i]["mask"] = out_dir + os.path.splitext(filenames[i])[
            0] + "_mask.png"
        res[i]["count"] = count
        res[i]["fractional_variation"] = compute_variation(
            os.path.join(out_dir, filenames[i]))
        after_img, data = hole_handle(out_dir, out_dir + "hole/", [retPic])
        res[i]["hole"] = after_img
        res[i]["hole_style"] = handle(
            fun_type_6, [os.path.basename(after_img)],
            out_dir + "hole/",
            out_dir + "hole/",
            prefix="hole")[0]
        mask, count = draw_masks(
            os.path.join(out_dir + "hole/", os.path.basename(after_img)))
        cv2.imwrite(
            os.path.join(
                out_dir + "hole/",
                os.path.splitext(os.path.basename(after_img))[0] + "_mask.png"),
            mask)
        res[i]["mask_hole"] = out_dir + "hole/" + os.path.splitext(
            os.path.basename(after_img))[0] + "_mask.png"
        res[i]["count_hole"] = count
        res[i]["fractional_variation_hole"] = compute_variation(
            os.path.join(generate_dir + "hole/", os.path.basename(after_img)))
        data = json.dumps(res[i])
        save_analysis(
            type_,
            first_,
            retPic,
            pic2=second_,
            data=data,
            checked=str(step1) + "," + str(step2),
            is_hole=True)
        i += 1
    print("变化检测----------------->end")


def hole_handle(data_path, out_dir, names):
    url_handle(names)
    # 1.孔洞处理
    res = handle(fun_type_8, names, data_path, out_dir)
    # 4.检测渲染
    res1 = handle(fun_type_6, res, out_dir, out_dir)
    return generate_url + "hole/" + res[0], res1[0]


def url_handle(imgs):
    j = 0
    for pair in imgs:
        imgs[j] = img_url_handle(pair)
        j += 1


def object_detection(model_path, data_path, out_dir, names, step1, step2,
                     type_):
    """
    目标检测
    :param model_path:
    :param data_path:
    :param out_dir:
    :return:
    """
    print("目标检测----------------->start")
    imgs = list()
    temp_names = copy.deepcopy(names)
    for j, pair in enumerate(names):
        names[j] = img_url_handle(pair)
        imgs.append(names[j])

    # 3.resize
    resizes = resize(data_path, data_path, imgs, mode=3)
    for i, pair in enumerate(imgs):
        imgs[i] = resizes[i]

    # 1.CLAHE or 锐化
    if step1 != 0:
        imgs = handle(step1, imgs, data_path, data_path)
    # 2.平滑or滤波
    if step2 != 0:
        imgs = handle(step2, imgs, data_path, data_path)

    # 4. 目标检测
    retPics = OD.execute(model_path, data_path, out_dir, imgs)
    # 5.入库
    for i, pair in enumerate(resizes):
        first_ = up_url + pair
        retPic = retPics[i]
        save_analysis(
            type_,
            first_,
            retPic,
            pic2="",
            data="",
            checked=str(step1) + "," + str(step2))
    print("目标检测----------------->end")


def terrain_classification(model_path, data_path, out_dir, names, step1, step2,
                           type_):
    """
    地物分类
    :param model_path:
    :param data_path:
    :param out_dir:
    :return:
    """
    print("地物分类----------------->start")
    imgs = list()
    temp_names = copy.deepcopy(names)
    for j, pair in enumerate(names):
        names[j] = img_url_handle(pair)
        imgs.append(names[j])
    # 3.resize
    resizes = resize(data_path, data_path, imgs, mode=2)
    for i, pair in enumerate(imgs):
        imgs[i] = resizes[i]

    # 1.CLAHE or 锐化
    if step1 != 0:
        imgs = handle(step1, imgs, data_path, data_path)
    # 2.平滑or滤波
    if step2 != 0:
        imgs = handle(step2, imgs, data_path, data_path)

    # 4. 地物分类
    retPics = SS.execute(model_path, data_path, out_dir, imgs)
    # 5.入库
    for i, pair in enumerate(resizes):
        first_ = up_url + pair
        retPic = retPics[i]
        save_analysis(
            type_,
            first_,
            retPic,
            pic2="",
            data="",
            checked=str(step1) + "," + str(step2))
    print("地物分类----------------->end")


def classification(model_path, data_path, names, type):
    """
    场景分类
    :param model_path: 模型存储目录
    :param data_path: 待推理图片存储目录
    :param names: 待推理图片列表
    :param type: 功能类别
    :return:
    """
    print("场景分类----------------->start")
    imgs = list()
    for j, pair in enumerate(names):
        names[j] = img_url_handle(pair)
        imgs.append(names[j])
    # 1. 场景分类
    result = C.execute(model_path, data_path, imgs)
    # 2.入库
    for i, pair in enumerate(names):
        first_ = up_url + pair
        ret = {}
        for j in range(0, len(result[i]["label_names_map"])):
            ret[result[i]["label_names_map"][j]] = result[i]["scores_map"][j]
        save_analysis(type, first_, "", pic2="", data=json.dumps(ret))
    print("场景分类----------------->end")


def image_restoration(model_path, data_path, out_dir, names, type_):
    """
    图像复原
    :param model_path:
    :param data_path:
    :param out_dir:
    :return:
    """
    print("图像复原----------------->start")
    imgs = list()
    for j, pair in enumerate(names):
        names[j] = img_url_handle(pair)
        imgs.append(names[j])

    # 1. 图像复原
    retPics = IR.execute(model_path, data_path, out_dir, imgs)
    # 2.入库
    for i, pair in enumerate(names):
        first_ = up_url + pair
        retPic = retPics[i]
        save_analysis(type_, first_, retPic, pic2="", data="")
    print("图像复原----------------->end")


def handle(fun_type, imgs, src_dir, save_dir, prefix=""):
    """

    :param fun_type:
            1=变化检测渲染，
            2=对比度自适应直方图均衡化(CLAHE)，
            3=平滑(中值滤波)，
            4=目标提取渲染，
            5=直方图匹配，
            6=锐化，
            7=高斯滤波

            1=直方图匹配，
            2=对比度自适应直方图均衡化(CLAHE)，
            3=平滑(中值滤波)，
            4=锐化，
            5=高斯滤波
            6=变化检测渲染，
            7=目标提取渲染，
            8=孔洞填充(用于变化检测结果图处理)
    """
    temps = list()
    if fun_type == fun_type_1:
        temps = histogram_match.gram_match(imgs, src_dir, save_dir, False)
    elif fun_type == fun_type_2:
        temps = CLAHE(src_dir, save_dir, imgs)
    elif fun_type == fun_type_3:
        temps = median_blur(src_dir, save_dir, imgs)
    elif fun_type == fun_type_4:
        temps = sharpen(src_dir, save_dir, imgs)
        pass
    elif fun_type == fun_type_5:
        temps = gaussian_blur(src_dir, save_dir, imgs)
    elif fun_type == fun_type_6:
        temps = batch_render(src_dir, save_dir, imgs, prefix)
    elif fun_type == fun_type_7:
        temps = batch_render_seg(src_dir, save_dir, imgs)
    elif fun_type == fun_type_8:
        temps = hole_fill(src_dir, save_dir, imgs)
    return temps
