from .function_class import *
import pymysql



# 创建python和MySQL连接
def create_connection():
    conn = pymysql.connect(
        host="localhost",  # 根据你的数据库主机设置
        user="root",  # MySQL用户名#
        # password="daerwen",# MySQL密码
        # password="123456",
        password = "Cyf20040629",
        database="bookweb",  # 数据库名称
    )
    return conn


# 创建用户，输入用户名，返回user_id，用户名已存在返回None
def create_user(username, password, mobile, email):
    """
    创建用户，如果用户名已存在返回 None，否则返回 user_id。

    :param username: 用户名
    :return: 用户 ID 或 None
    """
    user_id = None
    conn = create_connection()  # 假设已定义此函数建立数据库连接
    cur = conn.cursor()

    # 检查用户名是否已存在
    sql_check = """
        SELECT username
        FROM user
        WHERE username = %s
    """

    cur.execute(sql_check, (username,))
    if cur.rowcount > 0:
        # 如果用户名已存在，关闭连接并返回 None
        cur.close()
        conn.close()
        return None

    # 插入新用户
    sql_insert = """
        INSERT INTO user (username, password, mobile_phone, email, gender, edu_ground, school, major, my_love_book, my_love_author, maxim)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    default_values = (
        username,                # 用户名
        password,      # 默认密码
        mobile,           # 默认手机号
        email,  # 默认邮箱
        1,                       # 默认性别
        "unknown",               # 默认学历
        "unknown",               # 默认学校
        "unknown",               # 默认专业
        "unknown",               # 默认最喜爱的书籍
        "unknown",               # 默认最喜爱的作者
        "unknown"                # 默认格言
    )
    cur.execute(sql_insert, default_values)
    conn.commit()
    user_id = cur.lastrowid  # 获取插入用户的 ID

    # 关闭连接
    cur.close()
    conn.close()

    return user_id

def search_user_id(user_id):
    conn = create_connection()
    cur = conn.cursor()

    sql = """
        SELECT *
        FROM user
        WHERE id = %s
    """
    val = user_id
    cur.execute(sql, val)
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    user = None

    if cur.rowcount != 0:
        res = cur.fetchone()
        user_id = res[0]
        username = res[1]
        password = res[2]
        mobile = res[3]
        email = res[4]
        gender = res[5]
        edu_ground = res[6]
        school = res[7]
        major = res[8]
        my_love_book = res[9]
        my_love_author = res[10]
        maxim = res[11]

        user = Users(user_id, username, password, mobile, email, gender, edu_ground, school, major, my_love_book, my_love_author, maxim)

    cur.close()
    conn.close()

    return user


def search_user_name(username):
    user_id = None
    conn = create_connection()
    cur = conn.cursor()

    sql = """
        SELECT *
        FROM user
        WHERE username = %s
    """
    val = username
    cur.execute(sql, val)
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    user = None

    if cur.rowcount != 0:
        res = cur.fetchone()
        user_id = res[0]
        username = res[1]
        password = res[2]
        mobile = res[3]
        email = res[4]
        gender = res[5]
        edu_ground = res[6]
        school = res[7]
        major = res[8]
        my_love_book = res[9]
        my_love_author = res[10]
        maxim = res[11]

        user = Users(user_id, username, password, mobile, email, gender, edu_ground, school, major, my_love_book, my_love_author, maxim)

    cur.close()
    conn.close()

    return user

def search_user_mobile(mobile_phone):
    user_id = None
    conn = create_connection()
    cur = conn.cursor()

    sql = """
        SELECT *
        FROM user
        WHERE mobile_phone = %s
    """
    val = mobile_phone
    cur.execute(sql, val)
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    user = None

    if cur.rowcount != 0:
        res = cur.fetchone()
        user_id = res[0]
        username = res[1]
        password = res[2]
        mobile = res[3]
        email = res[4]
        gender = res[5]
        edu_ground = res[6]
        school = res[7]
        major = res[8]
        my_love_book = res[9]
        my_love_author = res[10]
        maxim = res[11]

        user = Users(user_id, username, password, mobile, email, gender, edu_ground, school, major, my_love_book, my_love_author, maxim)

    cur.close()
    conn.close()

    return user

def change_user(user: Users):
    if_success = False
    conn = create_connection()
    cur = conn.cursor()

    sql = """
        UPDATE user
        SET username = (%s), password = (%s), mobile_phone = (%s), email = (%s), gender = (%s), edu_ground = (%s), school = (%s), major = (%s), my_love_book = (%s), my_love_author = (%s), maxim = (%s)
        WHERE id = (%s);
    """
    val = (
        user.username,
        user.password,
        user.mobile_phone,
        user.email,
        user.gender,
        user.edu_ground,
        user.school,
        user.major,
        user.my_love_book,
        user.my_love_author,
        user.maxim,
        user.id,
    )
    rtn = cur.execute(sql, val)
    conn.commit()

    if cur.rowcount:
        if_success = True

    cur.close()
    conn.close()

    return if_success

def change_user_id(id_pre, id_post):
    if_success = False
    conn = create_connection()
    cur = conn.cursor()

    sql = """
        UPDATE user
        SET id = (%s)
        WHERE id = (%s);
    """
    val = (
        id_post,
        id_pre,
    )
    rtn = cur.execute(sql, val)
    conn.commit()

    if cur.rowcount:
        if_success = True

    cur.close()
    conn.close()

    return if_success

def create_book(title, author, average_rating, total_numbers):
    """
    创建用户，如果用户名已存在返回 None，否则返回 user_id。

    :param username: 用户名
    :return: 用户 ID 或 None
    """
    book_id = None
    conn = create_connection()  # 假设已定义此函数建立数据库连接
    cur = conn.cursor()

    # 检查用户名是否已存在
    sql_check = """
        SELECT title
        FROM book
        WHERE title = %s
    """
    cur.execute(sql_check, (title,))
    if cur.rowcount > 0:
        # 如果用户名已存在，关闭连接并返回 None
        cur.close()
        conn.close()
        return None

    # 插入新用户
    sql_insert = """
        INSERT INTO book (title,author,average_rating,total_numbers, image)
        VALUES (%s, %s, %s, %s, %s)
    """
    val = (title, author, average_rating, total_numbers, '')
    cur.execute(sql_insert, val)
    conn.commit()
    user_id = cur.lastrowid  # 获取插入用户的 ID

    # 关闭连接
    cur.close()
    conn.close()

    return user_id


def get_top_rated_books_sql():
    conn = create_connection()
    cur = conn.cursor()

    sql = """
        SELECT *
        FROM book
        ORDER BY average_rating DESC;
    """
    cur.execute(sql)
    rows = cur.fetchall()
    book_list = []
    for row in rows:
        book_n = Books(row[0], row[1], row[2], row[3], row[4])
        book_list.append(book_n)
    # 假设你有一个Book类来存储书籍信息
    # books = [Book(*row) for row in rows]  # 注意：这里需要调整Book类的初始化方法以匹配数据库中的列

    cur.close()
    conn.close()

    return book_list


def search_book_name(book_name):
    """
    搜索书籍信息。

    :param book_name: 书籍名称
    :return: 书籍对象或 None（如果未找到）
    """
    book_id = None
    conn = create_connection()  # 假设这是您定义的创建数据库连接的函数
    cur = conn.cursor()

    sql = """           
        SELECT *
        FROM book
        WHERE title LIKE %s
    """
    val = book_name
    cur.execute(sql, val)
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None
    rows = cur.fetchall()
    book_list = []
    for row in rows:
        book_n = Books(row[0], row[1], row[2], row[3], row[4])
        book_list.append(book_n)

    cur.close()
    conn.close()

    return book_list

def create_topic(subject, message, starter):
    """
    创建主题，如果主题插入成功返回 topic_id，否则返回 None。

    :param subject: 主题名称
    :param message: 主题内容
    :param starter: 发起者的用户 ID
    :return: 主题 ID 或 None
    """
    topic_id = None
    conn = create_connection()  # 假设已定义此函数建立数据库连接
    cur = conn.cursor()

    try:
        # 插入新主题
        sql_insert = """
            INSERT INTO topic (subject, last_updated, starter_id, views)
            VALUES (%s, NOW(), %s, 0)
        """
        cur.execute(sql_insert, (subject, starter))
        conn.commit()
        topic_id = cur.lastrowid  # 获取插入主题的 ID

        # 插入主题内容到另一个表 (假设有 message 表)
        sql_message_insert = """
            INSERT INTO message (topic_id, content, created_at, created_by)
            VALUES (%s, %s, NOW(), %s)
        """
        cur.execute(sql_message_insert, (topic_id, message, starter))
        conn.commit()

    except Exception as e:
        conn.rollback()  # 出现异常时回滚事务
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

    return topic_id

def get_top_topics():
    conn = create_connection()
    cur = conn.cursor()

    sql = """
        SELECT *
        FROM topic
        ORDER BY average_rating DESC;
    """
    cur.execute(sql)
    rows = cur.fetchall()
    topic_list = []
    for row in rows:
        topic_n = Topics(row[0], row[1], row[2], row[3])
        topic_list.append(topic_n)
    # 假设你有一个Book类来存储书籍信息
    # books = [Book(*row) for row in rows]  # 注意：这里需要调整Book类的初始化方法以匹配数据库中的列

    cur.close()
    conn.close()

    return topic_list

def search_topic_name(topic_name):
    """
    搜索话题信息。

    :param book_name: 话题主题
    :return: 具体的话题或者空
    """
    topic_id = None
    conn = create_connection()  # 假设这是您定义的创建数据库连接的函数
    cur = conn.cursor()

    sql = """           
        SELECT *
        FROM topic
        WHERE subject LIKE %s
    """
    val = topic_name
    cur.execute(sql, val)
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None
    rows = cur.fetchall()
    topic_list = []
    for row in rows:
        topic_n = Topics(row[0], row[1], row[2], row[3])
        topic_list.append(topic_n)

    cur.close()
    conn.close()

    return topic_list

def create_post(topic_id, message, starter):
    """
    创建帖子，如果插入成功返回 post_id，否则返回 None。

    :param topic_id: 关联的主题 ID
    :param message: 帖子内容
    :param starter: 发帖用户 ID
    :return: 帖子 ID 或 None
    """
    post_id = None
    conn = create_connection()  # 假设已定义此函数建立数据库连接
    cur = conn.cursor()

    try:
        # 插入新帖子
        sql_insert = """
            INSERT INTO post_table (message, topic_id, created_at,created_by_id)
            VALUES (%s, %s, NOW(), %s)
        """
        cur.execute(sql_insert, (message, topic_id, starter))
        conn.commit()
        post_id = cur.lastrowid  # 获取插入帖子的 ID
    except Exception as e:
        conn.rollback()  # 出现异常时回滚事务
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

    return post_id


def search_topic_post(topic_id):
    """
    搜索某个话题的回帖信息。

    :param topic_id: 对应话题的id
    :return: 具体的话题或者空
    """
    post_id = None
    conn = create_connection()  # 假设这是您定义的创建数据库连接的函数
    cur = conn.cursor()

    sql = """           
        SELECT *
        FROM post_table
        WHERE topic_id LIKE %s
    """
    val = topic_id
    cur.execute(sql, val)
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None
    rows = cur.fetchall()
    post_list = []
    for row in rows:
        post_n = Posts(row[0], row[1], row[2], row[3],row[5])
        post_list.append(post_n)
    cur.close()
    conn.close()

    return post_list


def create_comment(book_id, rating,comment,commenter ):
    """
    创建评论

    :param book_id: 对应书籍的id
    :param rating: 评分分数
    :param comment: 评价内容
    :param commenter: 发帖用户 ID
    """
    review_id = None
    conn = create_connection()  # 假设已定义此函数建立数据库连接
    cur = conn.cursor()

    try:
        # 插入新帖子
        sql_insert = """
            INSERT INTO review (book_id, rating, comment，commenter，)
            VALUES (%s, %s,%s, %s)
        """
        cur.execute(sql_insert, (book_id, rating, comment,commenter))
        conn.commit()
        review_id = cur.lastrowid
    except Exception as e:
        conn.rollback()  # 出现异常时回滚事务
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

    return review_id

def search_book_review(book_id):
    """
    搜索某本书籍的评价信息。

    :param book_id: 对应书本的id
    """
    review_id = None
    conn = create_connection()  # 假设这是您定义的创建数据库连接的函数
    cur = conn.cursor()

    sql = """           
        SELECT *
        FROM review
        WHERE book_id LIKE %s
    """
    val = book_id
    cur.execute(sql, val)
    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None
    rows = cur.fetchall()
    review_list = []
    for row in rows:
        review_n = Posts(row[0], row[1], row[2], row[3],row[4])
        review_list.append(review_n)
    cur.close()
    conn.close()

    return review_list