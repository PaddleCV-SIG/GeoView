CREATE TABLE `analysis` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` int(8) NOT NULL COMMENT '功能类型 1变化检测 2目标检测 3目标提取 4地物分类',
  `before_img` varchar(512) DEFAULT NULL COMMENT '图1',
  `before_img1` varchar(512) DEFAULT NULL COMMENT '图1 (变化检测)',
  `after_img` varchar(512) DEFAULT NULL COMMENT '结果图',
  `data` text COMMENT '结果',
  `is_hole` tinyint(1) DEFAULT NULL COMMENT '是否开启过孔洞',
  `checked` varchar(32) DEFAULT NULL COMMENT '勾选过那些功能,隔开',
  `create_time` datetime DEFAULT NULL COMMENT '分析时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='图像分析记录表';
CREATE TABLE `photo` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` int(8) DEFAULT NULL COMMENT '功能类型',
  `name` varchar(255)  NOT NULL COMMENT '图片名称',
  `href` varchar(255) DEFAULT NULL COMMENT '图片链接',
  `mime` char(50) NOT NULL COMMENT '图片类型',
  `size` char(30) NOT NULL COMMENT '图片大小',
  `create_time` datetime DEFAULT NULL COMMENT '上传时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='上传图片记录表';