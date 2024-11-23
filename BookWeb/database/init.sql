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

-- 创建图书评论表
CREATE TABLE review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL COMMENT '关联图书',
    rating FLOAT NOT NULL COMMENT '评分',
    comment TEXT NOT NULL COMMENT '评分理由',
    commenter VARCHAR(32) NOT NULL DEFAULT '未知用户' COMMENT '用户名',
    FOREIGN KEY (book_id) REFERENCES book(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图书评论表';

-- 创建主题表
CREATE TABLE topic (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(255) NOT NULL COMMENT '主题',
    last_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
    starter_id INT NOT NULL COMMENT '发起者',
    views INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '浏览次数',
    FOREIGN KEY (starter_id) REFERENCES user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='主题表';

-- 创建帖子表
CREATE TABLE post_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL COMMENT '消息内容',
    topic_id INT NOT NULL COMMENT '关联主题',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NULL COMMENT '更新时间',
    created_by_id INT NOT NULL COMMENT '创建者',
    updated_by_id INT NULL COMMENT '更新者',
    FOREIGN KEY (topic_id) REFERENCES topic(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (updated_by_id) REFERENCES user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帖子表';


