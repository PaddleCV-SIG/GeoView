# 推理结果展示
# 重复运行本单元可以查看不同结果

import os.path as osp

import cv2
from PIL import Image
from matplotlib import pyplot as plt
from skimage.io import imread

from applications.common.path_global import md5_name, generate_url


def show_images_in_row(im_paths, fig, title='', colormap=0):  # impaths为文件夹路径，colormap为渲染风格，可通过改变colormap的值来改变渲染风格
    if colormap == 0:
        map = plt.cm.plasma  # 闪电
    if colormap == 1:
        map = plt.cm.viridis  # 极光
    if colormap == 2:
        map = plt.cm.ocean  # 森林
    if colormap == 3:
        map = plt.cm.rainbow  # 霓虹
    # fig.suptitle(title)
    axs = fig.subplots(nrows=1, ncols=1)
    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    axs.spines['bottom'].set_visible(False)
    axs.spines['left'].set_visible(False)
    axs.get_xaxis().set_ticks([])
    axs.get_yaxis().set_ticks([])

    im = imread(im_paths)
    if im.ndim == 3:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    axs.imshow(im, cmap=map)


def render(name, data_dir, save_dir, colormap):  # 实现渲染的函数，考虑到我们的需要一次只能渲染一张，pic_source一样为图片位置
    # 参考 https://stackoverflow.com/a/68209152
    fig = plt.figure(constrained_layout=True)
    # fig.suptitle("")   设置标题用的，我们不用设置标题，因为下面已经设置了
    subfigs = fig.subfigures(nrows=1, ncols=1)
    # 读入变化图
    pic_source = osp.join(data_dir, name)
    show_images_in_row(pic_source, subfigs, title='Change Map', colormap=colormap)  # title为changemap，换成中文会乱码，勿换

    # 渲染结果
    fig.canvas.draw()
    Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    # plt.show()
    new_name = md5_name(str(colormap) + "_" + name)
    plt.savefig(osp.join(save_dir, new_name), bbox_inches='tight')
    return new_name


# 批量渲染
def bitch_render(data_dir, save_dir, imgs):
    temps = list()
    for img in imgs:
        maps = dict()
        for i in range(4):
            maps[i] = generate_url + render(img, data_dir, save_dir, i)
        temps.append(maps)
    return temps
