# 在线地图使用说明

## 功能描述

提供在线百度地图服务，允许用户搜索位置定位，截取图片，自定义训练模型，上传至目标检测、地物分类、场景分类和图像复原功能区。

## 使用方法

### 填充百度地图Access Key

在根目录下的`config.yaml`文件中百度地图配置处，将`<ACCESS_KEY>`替换为百度地图的Access Key。百度地图的Access Key可在[百度地图开放平台](http://lbsyun.baidu.com/apiconsole/key?application=key)申请。
``` yaml
baidu_map:
  access_key: <ACCESS_KEY>
```

### 基本使用

在输入框输入位置信息，选择搜索结果，定位到该地，可在地图右上角设置地图模式（混合地图模式和卫星地图模式），如图：
<p align="center">
    <img src="https://user-images.githubusercontent.com/90198481/198829346-67e8945d-d587-4feb-a9cb-dc787e267114.png" alt = "pic" width = "600" />
</p>
截取图片后，可选择上传功能区和训练模型，上传成功后即可查看效果，如图：
<p align="center">
    <img src="https://user-images.githubusercontent.com/90198481/198829708-61aed428-4a9d-4cc9-8619-b26164900011.png" alt = "pic" width="600" />
</p>
<p align="center">
    <img src="https://user-images.githubusercontent.com/90198481/198829771-6d437401-d78e-4f30-b36e-1b5b6bf5fddf.png" alt = "pic" width="600" />
</p>
