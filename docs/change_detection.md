# 变化检测功能使用说明

## 功能描述

对同一地点不同时期的两幅影像进行分析，定位区域内发生的变化情况。PP-GeoView目前仅支持二类变化检测任务，即，结果中以不同颜色标识“变化”与“不变”。

## 效果展示

+ 方式一：滑窗浏览
<p align="center">
    <img src="https://user-images.githubusercontent.com/78073130/198859495-2421f879-80ee-4766-9791-3f978c0c15e3.png" alt = "pic" width = "600" />
</p>

+ 方式二：前后时期影像并排对比浏览
<p align="center">
    <img src="https://user-images.githubusercontent.com/78073130/198859728-e702883e-d0e7-4ad8-9b1e-a3084b78371c.jpg" alt = "pic" width = "600" />
</p>

## 使用方法：

### 基本使用

变化检测需要分别在两个上传框内上传第一时期和第二时期的图像，支持一次上传一组图像。为了正确匹配影像对，请确保第一时期和第二时期对应的影像具有相同的文件名。若出现两个上传框上传图像数量不同、存在无法被正确匹配的图像、或是上传的文件格式错误的情况，将给出相应的错误信息提示。

### 高级功能

+ 在进行变化检测前，可对输入图像进行图像增强。在功能界面可以点击选项框添加需要进行的图像增强操作。备选项如下：
    - **直方图匹配**：适用于两幅图像风格差异比较大的情况，效果为使两幅图像的灰度值分布尽可能保持一致。
    - **图像锐化**：适用于图像分辨率较低或建筑物边缘模糊的情况，效果为增强建筑物的边缘、轮廓。

+ 在进行变化检测前，可对输入图像进行图像降噪。在功能界面可以点击选项框添加需要进行的图像降噪操作。备选项如下：
    - **平滑**：对影像进行中值滤波，适合用于去除类椒盐噪声。
    - **滤波**：对影像进行高斯滤波，适合用于去除类高斯噪声。

+ 在进行变化检测后，可在“结果图渲染”结果图像的配色方案。

+ 在进行变化检测后，可对结果图像进行后处理。勾选“开启连通域滤波并填充孔洞处理”以启用此功能。备选项如下：
    - **连通域滤波+孔洞填充**：去除伪变化噪声点以及填充变化区域内的孔洞，使结果更加接近真实情况。效果如下图所示：
        <p align="center">
            <img src="https://user-images.githubusercontent.com/78073130/198609084-a9b27edb-b6ba-40da-9e14-782a134ddc33.png" alt = "gif" width = "600" />
        </p>