class Users:
    def __init__(self, id, username, password, mobile_phone, email, gender=1,
                 edu_ground='', school='', major='', my_love_book='',
                 my_love_author='', maxim=''):
        """
        用户类，表示用户表的一个实例。

        :param id: 用户ID
        :param username: 用户名
        :param password: 密码
        :param mobile_phone: 手机号
        :param email: 邮箱
        :param gender: 性别，默认值为1
        :param edu_ground: 学历，默认值为空
        :param school: 学校，默认值为空
        :param major: 专业，默认值为空
        :param my_love_book: 最喜爱的书籍，默认值为空
        :param my_love_author: 最喜爱的作者，默认值为空
        :param maxim: 格言，默认值为空
        """
        self.id = id
        self.username = username
        self.password = password
        self.mobile_phone = mobile_phone
        self.email = email
        self.gender = gender
        self.edu_ground = edu_ground
        self.school = school
        self.major = major
        self.my_love_book = my_love_book
        self.my_love_author = my_love_author
        self.maxim = maxim


class Books:
    def __init__(self, id, title, author='未知', average_rating=0, total_numbers=0):
        """
        书籍类，表示书籍表的一个实例。

        :param book_id: 书籍ID
        :param title: 书籍名称
        :param author: 作者，默认值为'未知'
        :param average_rating: 平均评分，默认值为0
        :param total_numbers: 总评分人数，默认值为0
        """
        self.id = id
        self.title = title
        self.author = author
        self.average_rating = average_rating
        self.total_numbers = total_numbers


class Topics:
    def __init__(self, id, subject,update_time,views):
        """
        书籍类，表示书籍表的一个实例。

        :param book_id: 书籍ID
        :param title: 书籍名称
        :param author: 作者，默认值为'未知'
        :param average_rating: 平均评分，默认值为0
        :param total_numbers: 总评分人数，默认值为0
        """
        self.id = id
        self.subject = subject
        self.update_time = update_time
        self.views = views

class Posts:
    def __init__(self, id, message,topic_id,create_time,stater):
        """
        书籍类，表示书籍表的一个实例。

        :param book_id: 书籍ID
        :param title: 书籍名称
        :param author: 作者，默认值为'未知'
        :param average_rating: 平均评分，默认值为0
        :param total_numbers: 总评分人数，默认值为0
        """
        self.id = id
        self.message = message
        self.topic_id = topic_id
        self.created_at = create_time
        self.stater = stater

class Reviews:
    def __init__(self, id, book_id,rating,comment,commenter):
        """
        书籍类，表示书籍表的一个实例。

        :param book_id: 书籍ID
        :param title: 书籍名称
        :param author: 作者，默认值为'未知'
        :param average_rating: 平均评分，默认值为0
        :param total_numbers: 总评分人数，默认值为0
        """
        self.id = id
        self.book_id = book_id
        self.rating = rating
        self.comment = comment
        self.commenter = commenter