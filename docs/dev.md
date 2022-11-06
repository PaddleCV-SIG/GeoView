# GeoView 开发者文档

> 阅读如下教程前，请确保您已参照[文档](../README.md)正确安装GeoView。

## 1 模型准备

GeoView基于PaddleRS导出的预测模型（静态图）进行图像解译。您可以选择下载GeoView提供的预测模型，或者使用自己训练的模型（简称自训练模型）。

下表包含GeoView提供的预训练模型信息：

|模型名称|任务|下载链接|输入波段数|推荐输入尺寸（高*宽）|推荐空间分辨率|适用场景|预训练数据集|
|-|-|-|-|-|-|-|-|
|BIT|变化检测|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/cd/bit_levircd_static.zip)|3|256*256|0.5 m/像素|建筑物变化检测|[LEVIR-CD](https://justchenhao.github.io/LEVIR/)|
|ResNet50-vd|场景分类|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/clas/resnet50_vd_ucmerced_static.zip)|3|256*256|0.3 m/像素|农业用地、河流、棒球场等土地利用类型识别|[UC Merced](http://weegee.vision.ucmerced.edu/datasets/landuse.html)|
|PP-YOLO|目标检测|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/det//ppyolo_rsod_static.zip)|3|608*608|0.3-3 m/像素|飞机、操场、立交桥、油桶等目标检测|[RSOD](https://github.com/RSIA-LIESMARS-WHU/RSOD-Dataset-)|
|DeepLab V3+|地物分类|[链接](https://paddlers.bj.bcebos.com/geoview/pretrained/seg/deeplabv3p_rsseg_rgb_static.zip)|3|512*512|-|云、阴影、雪、水体、土地等区域识别|未公开数据集|

**请注意**：每个预测模型均有对应的输入波段数要求和适用场景，且仅在处理推荐的输入尺寸和空间分辨率范围内的图像时才能取得较好的效果。

若您需要使用自训练模型，请参考[使用PaddleRS训练和导出模型](https://github.com/PaddlePaddle/PaddleRS/blob/develop/deploy/export/README.md)。在准备自训练模型时请注意，**目前GeoView仅支持对三波段影像的处理**。

### （可选）使用 PaddleRS 训练和导出模型

请参考PaddleRS[模型训练文档](https://github.com/PaddlePaddle/PaddleRS/blob/develop/tutorials/train/README.md)与[模型导出文档](https://github.com/PaddlePaddle/PaddleRS/blob/develop/deploy/export/README.md)。

### 将模型导入到 GeoView

请遵循如下步骤导入模型：

1. 在`backend`目录下新建`model`目录。
2. 将解压后的预测模型或导出的自训练模型拷贝到任务对应的目录中（如目录不存在需要新建），各任务与目录的对应关系如下：
    - 变化检测：`backend/model/change_detection`
    - 场景分类：`backend/model/classification`
    - 目标检测：`backend/model/object_detection`
    - 图像复原：`backend/model/image_restoration`
    - 地物分类：`backend/model/semantic_segmentation`
3. （可选）根据需要，为拷贝后的模型目录修改一个易于辩识的名称。需要说明的是，用户在前端选择模型时主要根据模型架构名称，而不是此处设置的目录名称。

如下展示了模型存放的例子：
<p align="center">
<img src="https://user-images.githubusercontent.com/78073130/199014094-82d36df8-bb7c-4209-ac1f-b5f0cb2c0f2e.png" align="middle" width = "600" />
</p>
模型目录中应包含如下文件：
<p align="center">
<img src="https://user-images.githubusercontent.com/78073130/199014099-33d754a0-e89c-496a-a9fb-a38660f10ed1.png" align="middle" width = "600" />
</p>

## 2 Web 前后端配置

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

### 百度地图 Access Key 设置

在项目根目录下的`config.yaml`文件中将`<ACCESS_KEY>`替换为百度地图的Access Key。百度地图的Access Key可在[百度地图开放平台](http://lbsyun.baidu.com/apiconsole/key?application=key)申请。

``` yaml
baidu_map:
  access_key: <ACCESS_KEY>
```

## 3 Web 前后端启动

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

前端和后端均启动后，在浏览器中可通过IP地址+端口号访问GeoView工具。例如，在默认的IP与端口配置下，可通过`http://127.0.0.1:3000`访问。

关于GeoView各项功能的具体使用方式，请参考[用户文档](./user.md)。
