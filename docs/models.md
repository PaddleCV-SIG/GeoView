# 模型文件放置说明
本系统支持用户自定义模型权重功能，用户可选择用自己训练的模型进行预测。

具体操作方法如下：
 - 1.将模型文件放在对应的功能区下
 - 2.待系统检测到模型后用户自行选择想要使用的模型

各功能区对应的名称如下：
 - 变化检测：change_detection
 - 目标检测：object_detection
 - 地物分类：semantic_segmentation
 - 场景分类：classification
 - 图像复原: image_restoration
 ## 注意事项：用户应将模型放在一个文件夹中，之后再将此文件夹放在上述文件夹下。
 以下是实例示范，将用于变化检测的bit模型放在change_detecion文件夹下
