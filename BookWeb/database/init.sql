CREATE DATABASE IF NOT EXISTS bookweb;

use bookweb;

-- 创建用户表
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) NOT NULL COMMENT '用户名',
    password VARCHAR(64) NOT NULL COMMENT '密码',
    mobile_phone VARCHAR(32) NOT NULL COMMENT '手机号',
    email VARCHAR(32) NOT NULL COMMENT '邮箱',
    gender TINYINT NOT NULL DEFAULT 1 COMMENT '性别',
#     identity TINYINT NOT NULL DEFAULT 1 COMMENT '权限身份',
#     hr_allowed TINYINT NOT NULL DEFAULT 1 COMMENT '身份切换权限',
    edu_ground VARCHAR(30) DEFAULT '' COMMENT '学历',
    school VARCHAR(30) DEFAULT '' COMMENT '学校',
    major VARCHAR(30) DEFAULT '' COMMENT '专业',
    my_love_book VARCHAR(30) DEFAULT '' COMMENT '最喜爱的书籍',
    my_love_author VARCHAR(30) DEFAULT '' COMMENT '最喜爱的作者',
    maxim VARCHAR(30) DEFAULT '' COMMENT '格言'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 创建图书表
CREATE TABLE book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL COMMENT '书名',
    author VARCHAR(10) NOT NULL DEFAULT 'Unknown' COMMENT '作者',
    average_rating FLOAT NOT NULL DEFAULT 0.0 COMMENT '平均评分',
    total_numbers INT NOT NULL DEFAULT 0 COMMENT '总评分人数',
    image VARCHAR(255) DEFAULT 'default.png' COMMENT '封面图片'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图书表';


