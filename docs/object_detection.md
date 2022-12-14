# 目标检测使用说明

## 功能界面

在左侧导航栏选择“目标检测”进入。

<p align="center">
    <img src="https://user-images.githubusercontent.com/21275753/199168837-8d74876b-8c3f-4980-8409-52b4e573511d.png" alt = "pic" width = "600" />
</p>

## 功能描述

对图像进行目标检测，并将图像中不同类别的的目标用不同颜色的方框标记。

## 操作流程演示

<p align="center">
    <img src="https://user-images.githubusercontent.com/21275753/199176786-0cc5156d-b0e9-4922-a555-737af5555a49.gif" alt = "demo" width = "600" />
</p>

## 使用方法

### 基本使用

1. 单击“点击上传”选择单张或多张图像，或点击“上传文件夹”选择包含多张图像的文件夹。如果需要编辑上传的图片，例如进行裁剪、缩放等操作，请勾选“上传时编辑图片”（该操作仅适用于上传单张图像的情形）。关于图像在线编辑的功能请参考[文档](./edit_image.md)。点击“清空图片”可以撤销选择。
2. 在“可选训练模型”中选择需要使用的模型。
3. 点击“开始处理”提交任务，等待模型处理完毕后可在下方获取解译结果。若上传多张图像或文件夹，则依次显示每张图像的解译结果。如下图所示：

<p align="center">
    <img src="https://user-images.githubusercontent.com/21275753/199168981-c69806c4-b0fc-436d-9c81-6c0e44b014a7.png" alt = "res" width = "600" />
</p>

4. 解译结果的导出请参考[文档](./export_results.md)。

### 高级功能

+ 在进行目标检测前，可对输入图像进行增强。点击选项框添加需要进行的图像增强操作。启用图像增强功能后，可在界面预览处理结果。备选项如下：
    - **CLAHE**：适用于图像较暗的情况，效果为增强图像对比度。
    - **锐化**：适用于图像分辨率较低或建筑物边缘模糊的情况，效果为增强建筑物的边缘、轮廓。

+ 在进行目标检测前，可对输入图像进行降噪。点击选项框添加需要进行的图像降噪操作。备选项如下：
    - **平滑**：对影像进行中值滤波，适合用于去除类椒盐噪声。
    - **滤波**：对影像进行高斯滤波，适合用于去除类高斯噪声。

关于图像增强和图像降噪功能的更多细节，请参考[文档](./functions.md)。
