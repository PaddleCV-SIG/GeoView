# 场景分类使用说明

## 功能界面

在左侧导航栏选择“场景分类”进入。

<p align="center">
    <img src="https://user-images.githubusercontent.com/21275753/199176384-5fc41715-545d-45d9-9c25-889d59abfef3.png" alt = "pic" width = "600" />
</p>

## 功能描述

对图像进行场景分类，输出类别名称和置信度。

## 操作流程演示

<p align="center">
    <img src="https://user-images.githubusercontent.com/21275753/199176518-c3e63a6d-f96b-4c8d-bc2e-932d7fb9c324.gif" alt = "demo" width = "600" />
</p>

## 使用方法

### 基本使用

1. 单击“点击上传”选择单张或多张图像，或点击“上传文件夹”选择包含多张图像的文件夹。如果需要编辑上传的图片，例如进行裁剪、缩放等操作，请勾选“上传时编辑图片”（该操作仅适用于上传单张图像的情形）。关于图像在线编辑的功能请参考[文档](./edit_image.md)。点击“清空图片”可以撤销选择。
2. 在“可选训练模型”中选择需要使用的模型。
3. 点击“开始处理”提交任务，等待模型处理完毕后可在下方获取解译结果。若上传多张图像或文件夹，则依次显示每张图像的解译结果。如下图所示：

<p align="center">
    <img src="https://user-images.githubusercontent.com/21275753/199176201-4017f248-3134-4936-a51e-224eed46012a.png" alt = "res" width = "600" />
</p>
