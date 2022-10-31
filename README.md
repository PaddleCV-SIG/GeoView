<div align="center">
    <p align="center">
        <img src="https://user-images.githubusercontent.com/78073130/198640332-3edba236-db03-4eb0-b803-90a1053e87f3.png" alt="logo" width = "500" />
    </p>

[![build status](https://github.com/PaddleCV-SIG/PP-GeoView/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/PaddleCV-SIG/PP-GeoView/actions)
[![contributors](https://img.shields.io/github/contributors/PaddleCV-SIG/PP-GeoView?color=9ea)](https://github.com/PaddleCV-SIG/PP-GeoView/graphs/contributors)
[![commits](https://img.shields.io/github/commit-activity/m/PaddleCV-SIG/PP-GeoView?color=3af)](https://github.com/PaddleCV-SIG/PP-GeoView/commits)
[![issues](https://img.shields.io/github/issues/PaddleCV-SIG/PP-GeoView?color=9cc)](https://github.com/PaddleCV-SIG/PP-GeoView/issues)
![python version](https://img.shields.io/badge/python-3.7+-orange.svg)
![node.js version](https://img.shields.io/badge/nodejs-16+-orange.svg)

</div>

## 简介

PP-GeoView是一款开源、轻量、功能丰富的**遥感影像智能解译工具**，致力于实现遥感领域深度学习模型在Web平台的快速部署。

## 特性

PP-GeoView支持5大遥感影像解译任务：

- 变化检测
- 场景分类
- 目标检测
- 图像复原
- 地物分类

此外，PP-GeoView提供以下辅助功能：

- 遥感影像预处理
- 解译结果后处理
- 解译结果导出
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

上述依赖安装完毕后，首先从GitHub将PP-GeoView项目克隆到本地：

```shell
git clone --recursive https://github.com/PaddleCV-SIG/PP-GeoView.git
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

至此，PP-GeoView安装完成。根据您的需求，您可以参考[开发者文档](./docs/dev.md)或[用户文档](./docs/user.md)进行PP-GeoView工具的使用。

## 使用说明

- 若您的需求是使用PP-GeoView部署和发布模型，请阅读[开发者文档](./docs/dev.md)。
- 若您希望了解基于PP-GeoView发布的产品的使用方式，请阅读[用户文档](./docs/user.md)。

## 代码结构

PP-GeoView目录树中关键部分如下：

``` plain
├── backend              # Web后端
│     ├── applications   # 后端核心代码
│     ├── model          # 模型存放目录
│     └── static         # 图像存储目录
└── frontend             # Web前端
```

## 开源贡献

PP-GeoView欢迎各种形式的开源贡献。

特别感谢以下开发者对本项目的贡献：（排名不分先后）[曹凌铭](https://github.com/terayco)，[卢利栋](https://github.com/jscslld)，[易博坤](https://github.com/yibaikuai)。
