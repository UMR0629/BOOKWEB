import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.core.mail import send_mail
from django.conf import settings

from UserAuth.utils.validators import is_valid_email


def check_code(width=120, height=40, char_length=5, font_file='MONACO.ttf', font_size=24):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(240, 240, 240))  # 浅灰色背景
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """生成随机大写字母和数字"""
        return random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789')

    def rndColor():
        """生成较深的随机颜色"""
        return random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)

    def rndBackgroundColor():
        """生成背景随机浅色"""
        return random.randint(180, 255), random.randint(180, 255), random.randint(180, 255)

    # 设置字体
    font = ImageFont.truetype(font_file, font_size)

    # 添加验证码字符
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        # 调整字符的水平间距和高度
        x = i * width / char_length + random.randint(-2, 2)
        y = random.randint(2, height - font_size - 2)
        draw.text((x, y), char, font=font, fill=rndColor())

    # 添加干扰圆圈（减少数量、透明化）
    for _ in range(10):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(5, 10)
        draw.ellipse((x, y, x + radius, y + radius), outline=rndBackgroundColor(), width=1)

    # 添加干扰线（减小数量并调整透明度）
    for _ in range(3):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndBackgroundColor(), width=1)

    # 应用滤镜提升对比度
    img = img.filter(ImageFilter.SMOOTH)

    return img, ''.join(code)



def send_sms_code(target_email):
    """
    发送邮箱验证码
    :param target_email: 发到这个邮箱
    :return:
        send_status: 0 成功 -1 失败
        sms_code: 验证码
    """
    # 验证邮箱地址是否正确
    if not is_valid_email(target_email):
        return -1
    # 生成邮箱验证码
    sms_code = '%06d' % random.randint(0, 999999)
    email_from = settings.EMAIL_FROM  # 邮箱来自
    email_title = settings.EMAIL_TITLE
    email_body = "您的邮箱验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
    send_status = send_mail(email_title, email_body, email_from, [target_email])
    return send_status, str(sms_code)
