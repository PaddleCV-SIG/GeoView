import os.path as osp
from copy import deepcopy
from functools import partial
from operator import itemgetter

import numpy as np
import paddle
import paddlers as pdrs
from skimage.io import imsave
from tqdm import tqdm

from applications.common.path_global import md5_name, generate_url
from applications.interface.utils import load_transformer_from_file


def write_rel_paths(phase, names, out_dir):
    """将文件相对路径存储在txt格式文件中"""
    with open(osp.join(out_dir, phase + '.txt'), 'w') as f:
        for name in names:
            f.write(
                ' '.join([
                    osp.join('A', name),
                    osp.join('B', name),
                ])
            )
            f.write('\n')


def execute(model_path, data_path, out_dir, names_):
    # 实例化测试集
    # 创建DataLoader
    test_dataset = InferDataset(
        # 注意，测试阶段使用的归一化方式需与训练时相同
        model_path,
        data_path,
        names_
    )
    test_dataloader = paddle.io.DataLoader(
        test_dataset,
        batch_size=1,
        shuffle=False,
        num_workers=0,
        drop_last=False,
        return_list=True
    )
    # 设置滑窗大小与滑动步长
    WINDOW_SIZE = 256
    STRIDE = 128

    ORIGINAL_SIZE = (1024, 1024)

    # 把滑窗中的内容全部取出，存在一个列表中

    test_patches = crop_patches(
        test_dataloader,
        ORIGINAL_SIZE,
        WINDOW_SIZE,
        STRIDE
    )

    # 构建预测器并执行推理
    predictor = pdrs.deploy.Predictor(model_path, use_gpu=True)
    len_test = len(test_dataset)
    temps = list()
    temps1 = list()
    for name, (t1, t2) in tqdm(test_patches, total=len_test):
        patch_pairs = list(zip(np.transpose(t1.numpy(), (0, 2, 3, 1)), np.transpose(t2.numpy(), (0, 2, 3, 1))))
        # 导出输入尺寸为滑窗大小的模型，--fixed_input_shape中的batch_size等于len(patch_pairs)
        res = predictor.predict(patch_pairs)

        # 取出所有的概率图patch并重建
        prob_patches = map(itemgetter((..., 1)), map(itemgetter('score_map'), res))
        prob_map = recons_prob_map(prob_patches, ORIGINAL_SIZE, WINDOW_SIZE, STRIDE)

        # 对概率图进行阈值分割，得到二值变化图
        cm_slide = (prob_map > 0.5).astype('int32')
        new_name = md5_name(name)
        imsave(osp.join(out_dir, new_name), cm_slide, check_contrast=False)
        temps.append(generate_url + new_name)
        temps1.append(new_name)
    return temps, temps1


# 定义推理阶段使用的数据集

class InferDataset(paddle.io.Dataset):
    """
    变化检测推理数据集。

    Args:
        data_dir (str): 数据集所在的目录路径。
        model_dir 模型目录
    """

    def __init__(
            self,
            model_dir,
            data_dir,
            names_
    ):
        super().__init__()
        # self.data_dir = data_dir
        # self.transforms = load_model(model_dir, with_net=False).test_transforms
        self.transforms = load_transformer_from_file(model_dir, ["Resize"])
        samples = []
        names = []
        for items in names_:
            print(items)
            item_dict = {
                'image_t1': osp.join(data_dir, items["first"]),
                'image_t2': osp.join(data_dir, items["second"])
            }
            samples.append(item_dict)
            names.append(osp.basename(items["first"]))

        self.samples = samples
        self.names = names

    def __getitem__(self, idx):
        name = self.names[idx]
        sample = deepcopy(self.samples[idx])
        output = self.transforms(sample)
        return name, \
               paddle.to_tensor(output[0]), \
               paddle.to_tensor(output[1]),

    def __len__(self):
        return len(self.samples)


# 考虑到原始影像尺寸较大，以下类和函数与影像裁块-拼接有关。

class WindowGenerator:
    def __init__(self, h, w, ch, cw, si=1, sj=1):
        self.h = h
        self.w = w
        self.ch = ch
        self.cw = cw
        if self.h < self.ch or self.w < self.cw:
            raise NotImplementedError
        self.si = si
        self.sj = sj
        self._i, self._j = 0, 0

    def __next__(self):
        # 列优先移动（C-order）
        if self._i > self.h:
            raise StopIteration

        bottom = min(self._i + self.ch, self.h)
        right = min(self._j + self.cw, self.w)
        top = max(0, bottom - self.ch)
        left = max(0, right - self.cw)

        if self._j >= self.w - self.cw:
            if self._i >= self.h - self.ch:
                # 设置一个非法值，使得迭代可以early stop
                self._i = self.h + 1
            self._goto_next_row()
        else:
            self._j += self.sj
            if self._j > self.w:
                self._goto_next_row()

        return slice(top, bottom, 1), slice(left, right, 1)

    def __iter__(self):
        return self

    def _goto_next_row(self):
        self._i += self.si
        self._j = 0


def crop_patches(dataloader, ori_size, window_size, stride):
    """
    将`dataloader`中的数据裁块。

    Args:
        dataloader (paddle.io.DataLoader): 可迭代对象，能够产生原始样本（每个样本中包含任意数量影像）。
        ori_size (tuple): 原始影像的长和宽，表示为二元组形式(h,w)。
        window_size (int): 裁块大小。
        stride (int): 裁块使用的滑窗每次在水平或垂直方向上移动的像素数。

    Returns:
        一个生成器，能够产生iter(`dataloader`)中每一项的裁块结果。一幅图像产生的块在batch维度拼接。例如，当`ori_size`为1024，而
            `window_size`和`stride`均为512时，`crop_patches`返回的每一项的batch_size都将是iter(`dataloader`)中对应项的4倍。
    """

    for name, *ims in dataloader:
        ims = list(ims)  # 两张图片,每张为shape=[1, 3, 1024, 1024]
        h, w = ori_size
        win_gen = WindowGenerator(h, w, window_size, window_size, stride, stride)  # (256，256)
        all_patches = []  # 两张图片的全部裁块 len=169
        for rows, cols in win_gen:
            # NOTE: 此处不能使用生成器，否则因为lazy evaluation的缘故会导致结果不是预期的
            patches = [im[..., rows, cols] for im in ims]  # Tensor shape=[1, 3, 256, 256], dtype=float32
            all_patches.append(patches)
        yield name[0], tuple(map(partial(paddle.concat, axis=0), zip(*all_patches)))


def recons_prob_map(patches, ori_size, window_size, stride):
    """从裁块结果重建原始尺寸影像，与`crop_patches`相对应"""
    # NOTE: 目前只能处理batch size为1的情况
    h, w = ori_size
    win_gen = WindowGenerator(h, w, window_size, window_size, stride, stride)
    prob_map = np.zeros((h, w), dtype=np.float)
    cnt = np.zeros((h, w), dtype=np.float)
    # XXX: 需要保证win_gen与patches具有相同长度。此处未做检查
    for (rows, cols), patch in zip(win_gen, patches):
        prob_map[rows, cols] += patch
        cnt[rows, cols] += 1
    # prob_map /= cnt
    prob_map /= cnt
    return prob_map
