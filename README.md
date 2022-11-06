<div align="center">
    <p align="center">
        <img src="https://user-images.githubusercontent.com/78073130/198640332-3edba236-db03-4eb0-b803-90a1053e87f3.png" alt="logo" width="500" />
    </p>

[![build status](https://github.com/PaddleCV-SIG/GeoView/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/PaddleCV-SIG/GeoView/actions)
[![contributors](https://img.shields.io/github/contributors/PaddleCV-SIG/GeoView?color=9ea)](https://github.com/PaddleCV-SIG/GeoView/graphs/contributors)
[![commits](https://img.shields.io/github/commit-activity/m/PaddleCV-SIG/GeoView?color=3af)](https://github.com/PaddleCV-SIG/GeoView/commits)
[![issues](https://img.shields.io/github/issues/PaddleCV-SIG/GeoView?color=9cc)](https://github.com/PaddleCV-SIG/GeoView/issues)
![python version](https://img.shields.io/badge/python-3.7+-orange.svg)
![node.js version](https://img.shields.io/badge/nodejs-16+-orange.svg)

</div>

<div align="center">
<table>
    <tr>
        <td><img src="https://user-images.githubusercontent.com/21275753/199176961-97466391-6cea-4a11-999a-78b8b0e0d602.gif", width="250"></td>
        <td><img src="https://user-images.githubusercontent.com/21275753/199176518-c3e63a6d-f96b-4c8d-bc2e-932d7fb9c324.gif", width="250"></td>
        <td><img src="https://user-images.githubusercontent.com/21275753/199176786-0cc5156d-b0e9-4922-a555-737af5555a49.gif", width="250"></td>
    <tr>
    <tr>
        <td align="center">变化检测</td>
        <td align="center">场景分类</td>
        <td align="center">目标检测</td>
    <tr>
    <tr>
        <td><img src="https://user-images.githubusercontent.com/21275753/199176761-ac67b553-309c-4d3a-90cc-31ffe3c8522a.gif", width="250"></td>
        <td><img src="https://user-images.githubusercontent.com/21275753/199175092-cf640078-868e-4633-aca0-e5b69971bc75.gif", width="250"></td>
        <td><img src="https://user-images.githubusercontent.com/90198481/198829346-67e8945d-d587-4feb-a9cb-dc787e267114.png", width="250"></td>
    <tr>
    <tr>
        <td align="center">图像复原</td>
        <td align="center">地物分类</td>
        <td align="center">在线地图</td>
    <tr>
</table>
</div>

## 简介

GeoView是一款开源、轻量、功能丰富的**遥感影像智能解译工具**，致力于实现遥感领域深度学习模型在Web平台的快速部署。

## 特性

GeoView支持5大遥感影像解译任务：

- 变化检测
- 场景分类
- 目标检测
- 图像复原
- 地物分类

除基本解译功能外，GeoView提供以下辅助功能：

- 遥感影像预处理
- 解译结果后处理
- 图像在线编辑
- 解译结果导出
- 历史记录查询
- 在线地图解译

## 安装说明

### 前置依赖安装

在执行后续步骤之前，请确保您安装了如下依赖库：

- MySQL >= 5.7
- Node.js >= 16.0
- PaddlePaddle >= 2.2.0

其中，PaddlePaddle安装可以参考[PaddlePaddle官网](https://www.paddlepaddle.org.cn/)。这里给出安装CPU版本的例子：

```shell
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

### 项目下载与安装

上述依赖安装完毕后，首先从GitHub将GeoView项目克隆到本地：

```shell
git clone --recursive https://github.com/PaddleCV-SIG/GeoView.git
```

运行如下命令安装PaddleRS：

```shell
pip install -r PaddleRS/requirements.txt
pip install -e PaddleRS/
```

接着，运行如下命令以安装Web后端的所有依赖：

```shell
pip install -r backend/requirements.txt
```

最后，运行如下命令安装Web前端的所有依赖：

```shell
cd frontend
npm install
```

## 使用说明

- 若您的需求是使用GeoView部署和发布模型，请阅读[开发者文档](./docs/dev.md)。
- 若您希望了解基于GeoView发布的产品的使用方式，请阅读[用户文档](./docs/user.md)。
- 完整使用GeoView的所有功能，请首先根据[开发者文档](./docs/dev.md)配置环境并启动服务，然后阅读[用户文档](./docs/user.md)了解使用细节。

## 代码结构

GeoView目录树中关键部分如下：

``` plain
├── backend              # Web后端
│     ├── applications   # 后端核心代码
│     ├── model          # 模型存放目录
│     └── static         # 图像存储目录
└── frontend             # Web前端
```

## 开源贡献

GeoView欢迎各种形式的开源贡献。

特别感谢以下开发者对本项目的贡献：（排名不分先后）[曹凌铭](https://github.com/terayco)，[卢利栋](https://github.com/jscslld)，[易博坤](https://github.com/yibaikuai)。
