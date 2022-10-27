# PP-GeoView

[![build status](https://github.com/PaddleCV-SIG/PP-GeoView/actions/workflows/build.yml/badge.svg?branch=develop)](https://github.com/PaddleCV-SIG/PP-GeoView/actions)
![python version](https://img.shields.io/badge/python-3.7+-orange.svg)
![node.js version](https://img.shields.io/badge/nodejs-16+-orange.svg)
![support os](https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-yellow.svg)

## 简介

PP-GeoView是一款开源、轻量、功能丰富的遥感影像智能解译工具，致力于实现遥感领域深度学习模型在Web平台的快速部署。

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

#### PaddlePaddle 安装

请参考[PaddlePaddle官网](https://www.paddlepaddle.org.cn/)安装。这里给出安装CPU版本的例子：

```shell
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

#### Node.js 安装

**Windows系统安装方法**

进入[Node.js官网](https://nodejs.org/en/)，选择16.18.0 LTS版本下载。下载后，按照安装向导进行安装，详细安装步骤可以参考[CSDN博文](https://blog.csdn.net/bbj12345678/article/details/106741758)。

**Linux系统安装方法**

Linux下建议使用nvm完成Node.js的安装。安装指令如下：

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.2/install.sh | bash
nvm use 16
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

### Web后端的安装

#### 安装依赖

进入`backend`目录后，运行如下命令即可安装Web后端的所有依赖。

```bash
pip install -r requirements.txt
```

#### 修改配置文件

首先，将`.flaskenv_template`文件重命名为`.flaskenv`。在`.flaskenv`中，修改Mysql配置信息，具体为：

```plain
# MySql配置信息
MYSQL_HOST=MYSQL服务器IP
MYSQL_PORT=MYSQL服务器端口
MYSQL_DATABASE=MYSQL数据库名
MYSQL_USERNAME=MYSQL用户名
MYSQL_PASSWORD=MYSQL密码
```

#### 启动Web后端

运行`python app.py`，即可启动Web后端。启动后，系统会自动初始化数据库。

### Web前端的安装

#### 安装依赖

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
