# PP-GeoView 开发者文档

> 阅读如下教程前，请确保您已参照[文档](../README.md)正确安装PP-GeoView。

## 模型准备

PP-GeoView基于PaddleRS导出的推理格式（静态图）模型进行图像解译。您可以选择下载PP-GeoView提供的预训练模型或使用自定义模型。

下表包含PP-GeoView提供的预训练模型信息：

|模型名称|任务|下载链接|输入波段数|推荐输入尺寸（高*宽）|推荐空间分辨率|适用场景|预训练数据集|
|-|-|-|-|-|-|-|-|
|BIT|变化检测|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/cd/bit_levircd_static.zip)|3|256*256|0.5 m/像素|建筑物变化检测|[LEVIR-CD](https://justchenhao.github.io/LEVIR/)|
|ResNet50-vd|场景分类|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/clas/resnet50_vd_ucmerced_static.zip)|3|256*256|0.3 m/像素|农业用地、河流、棒球场等土地利用类型识别|[UC Merced](http://weegee.vision.ucmerced.edu/datasets/landuse.html)|
|PP-YOLO|目标检测|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/det//ppyolo_rsod_static.zip)|3|608*608|0.3-3 m/像素|飞机、操场、立交桥、油桶等目标检测|[RSOD](https://github.com/RSIA-LIESMARS-WHU/RSOD-Dataset-)|
|DRN|图像复原|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/res/drn_rssr_static.zip)|3|256*256|-|影像超分辨率重建|未公开数据集|
|DeepLab V3+|地物分类|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/seg/deeplabv3p_rsseg_rgb_static.zip)|3|512*512|-|云、阴影、雪、水体、土地等区域识别|未公开数据集|

**请注意**：每个预训练模型均有对应的输入波段数要求和适用场景，且仅在处理推荐的输入尺寸和空间分辨率范围内的图像时才能取得较好的效果。

若您需要使用自定义模型，请参考[使用PaddleRS训练和导出模型](https://github.com/PaddlePaddle/PaddleRS/blob/develop/deploy/export/README.md#11)
。

### （可选）使用PaddleRS训练和导出模型

请参考PaddleRS[模型训练文档](https://github.com/PaddlePaddle/PaddleRS/blob/develop/tutorials/train/README.md)
与[模型导出文档](https://github.com/PaddlePaddle/PaddleRS/blob/develop/deploy/export/README.md)
。

### 将模型导入到PP-GeoView

请遵循如下步骤导入模型：

1. 在项目根目录新建`model`目录。
2. 将解压后的预训练模型或导出的自定义模型拷贝到对应任务的*功能区*中。功能区是`model`中的子目录，各任务与功能区的对应关系如下：
    - 变化检测：`model/change_detection`
    - 场景分类：`model/classification`
    - 目标检测：`model/object_detection`
    - 图像复原: `model/image_restoration`
    - 地物分类：`model/semantic_segmentation`
3. 根据需要，为拷贝后的模型目录修改一个易于辩识的名称，该名称将在Web前端被用于模型选择。

如下展示了模型存放的例子：
<p align="center">
<img src="https://user-images.githubusercontent.com/78073130/198609273-b301ab64-02c8-4b9f-9ead-df1b6ff93a10.png" align="middle" width = "600" />
</p>
模型目录中应包含如下文件：
<p align="center">
<img src="https://user-images.githubusercontent.com/78073130/198609366-5f6e8f02-d249-44a1-bcaf-48ab8ec0db47.png" align="middle" width = "600" />
</p>

## Web 前后端配置

### 修改 Web 后端配置文件

首先切换到`backend/`目录。将`.flaskenv_template`文件重命名为`.flaskenv`。在`.flaskenv`中，修改MySQL配置信息，各配置项含义如下：

```plain
# MySQL配置信息
MYSQL_HOST={MySQL服务器IP}
MYSQL_PORT={MySQL服务器端口}
MYSQL_DATABASE={MySQL数据库名}
MYSQL_USERNAME={MySQL用户名}
MYSQL_PASSWORD={MySQL用户密码}
```

### 设置百度地图Access Key
在根目录下的`config.yaml`文件中，按以下规则替换百度地图的Access Key。百度地图的Access Key可在[百度地图开放平台](http://lbsyun.baidu.com/apiconsole/key?application=key)申请。
``` yaml
baidu_map:
  access_key: {百度地图ACCESS_KEY}
```

### （可选）修改IP地址和端口号

若您需要指定前端、后端的IP地址或端口号，请按以下规则编辑项目根目录下的`config.yaml`文件：

``` yaml
port:
  backend: {后端端口号}
  frontend: {前端端口号}
host:
  backend: {后端监听ip}
  frontend: {前端监听ip}
```

## Web 前后端启动

### 启动 Web 后端

在项目根目录执行如下指令以启动 Web 后端：

```shell
cd backend
python app.py
```

启动后，数据库将自动得到初始化。

### 启动 Web 前端

在项目根目录执行如下指令以启动 Web 前端：

```shell
cd frontend
npm run serve
```

前端和后端均启动后，在浏览器中可通过IP地址+端口号访问PP-GeoView工具。例如，在默认的IP与端口配置下，可通过`http://127.0.0.1:3000`访问。

关于PP-GeoView各项功能的具体使用方式，请参考[用户文档](./user.md)。
