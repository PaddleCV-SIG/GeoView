# PP-GeoView

## 代码结构

PP-GeoView目录树中关键部分如下：

``` plain
├── backend              # Web后端
│     ├── applications   # 后端核心代码
│     ├── model          # 模型存放目录
│     └── static         # 图像存储目录
└── frontend             # Web前端
```

## 安装

### 前置条件

- python >= 3.7

- mysql >= 5.7

- Node.js >= 16.0

- PaddlePaddle >= 2.2.0

- 操作系统: Linux, Windows, Mac OSX

PP-GeoView依赖于PaddlePaddle和PaddleRS。PaddlePaddle安装可以参考[PaddlePaddle官网](https://www.paddlepaddle.org.cn/)，根据自己机器的情况进行选择。这里给出 cpu 版本示例，其它版本大家可以根据自己机器的情况进行安装。

```bash
pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
```

paddleRS安装可以参考[PaddleRS文档](https://github.com/PaddlePaddle/PaddleRS/blob/develop/tutorials/train/README.md)。命令为

``` bash
cd PaddleRS
pip install -r requirements.txt
python setup.py install
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

进入`frontend`目录后，运行如下命令即可安装Web前端的所有依赖。

```bash
npm install
```

#### 启动Web前端

运行`npm run serve`，即可启动Web前端。启动后，可在浏览器中输入`http://127.0.0.1:3000`访问系统。
