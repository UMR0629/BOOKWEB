class User:
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

    def __str__(self):
        return (f"User(id={self.id}, username='{self.username}', password='****', "
                f"mobile_phone='{self.mobile_phone}', email='{self.email}', "
                f"gender={self.gender}, edu_ground='{self.edu_ground}', "
                f"school='{self.school}', major='{self.major}', "
                f"my_love_book='{self.my_love_book}', "
                f"my_love_author='{self.my_love_author}', maxim='{self.maxim}')")

    def to_dict(self):
        """
        将用户对象转换为字典表示。
        """
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "mobile_phone": self.mobile_phone,
            "email": self.email,
            "gender": self.gender,
            "edu_ground": self.edu_ground,
            "school": self.school,
            "major": self.major,
            "my_love_book": self.my_love_book,
            "my_love_author": self.my_love_author,
            "maxim": self.maxim,
        }
