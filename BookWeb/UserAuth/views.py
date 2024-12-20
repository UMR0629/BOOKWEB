from io import BytesIO
import re

from Demos.win32ts_logoff_disconnected import username
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from UserAuth.utils.Forms import RegisterForm, LoginForm, ResetPasswordForm
from UserAuth.utils.Forms import Register

from UserAuth import models

from UserAuth.utils.generateCode import check_code, send_sms_code
from UserAuth.utils.validators import is_valid_email
from UserAuth.utils.encrypt import md5_encrypt

from database.database import *
# Create your views here.
"""视图页面开始"""


def register(request):
    if request.method == 'GET':
        form = RegisterForm(request=request)
        context = {
            'form': form,
            'nid': 1  # represent registration
        }
        return render(request, 'UserAuth/UserAuth.html', context=context)

    # if method is post
    form = RegisterForm(data=request.POST, request=request)
    if not form.is_valid():
        context = {
            'form': form,
            'nid': 1
        }
        return render(request, 'UserAuth/UserAuth.html', context=context)

    # store userinfo
    user_name = form.clean_username()
    password = form.clean_password()
    password = md5_encrypt(password)
    mobile_phone = form.clean_mobile_phone()
    email = form.clean_email()
    id = create_user(user_name, password, mobile_phone, email)

    form.instance.identity = 1  # default: User
    form.instance.password = md5_encrypt(form.instance.password)
    form.save()

    row_obj = models.User.objects.filter(username=form.cleaned_data['username']).first()
    user = search_user_id(id)
    print(row_obj.id)
    change_user_id(user.id, row_obj.id)



    # generate cookie
    user = search_user_name(user_name)
    # obj = models.User.objects.filter(username=form.cleaned_data["username"]).first()
    request.session["UserInfo"] = {
        'id': user.id,
        'username': user.username
    }
    request.session.set_expiry(60 * 60 * 24 * 7)  # 7天免登录
    return redirect("/")


def login(request):
    if request.method == 'GET':
        form = LoginForm(request=request)
        context = {
            'form': form,
            'nid': 2
        }
        return render(request, 'UserAuth/UserAuth.html', context=context)

    # if method is POST
    form = LoginForm(data=request.POST, request=request)
    if not form.is_valid():
        context = {
            'form': form,
            'nid': 2
        }
        return render(request, 'UserAuth/UserAuth.html', context=context)

    # row_obj = models.User.objects.filter(username=form.cleaned_data['username']).first()
    # 通过username检索，获得某一个user元组的内容
    row_user = search_user_name(form.cleaned_data['username'])
    # request.session["UserInfo"] = {
    #     'id': row_obj.id,
    #     'username': row_obj.username
    # }
    # 传递userid和username
    request.session["UserInfo"] = {
        'id': row_user.id,
        'username': row_user.username
    }
    request.session.set_expiry(60 * 60 * 24 * 7)  # 7天免登录
    return redirect(reverse('Forum:home'))


def reset_password(request):
    if request.method == 'GET':
        form = ResetPasswordForm(request=request)
        context = {
            'form': form,
            'nid': 2
        }
        return render(request, 'UserAuth/forget_password.html', context=context)

    # else POST method
    form = ResetPasswordForm(data=request.POST, request=request)
    if not form.is_valid():
        context = {
            'form': form,
        }
        return render(request, 'UserAuth/forget_password.html', context=context)

    username_or_mobile = form.cleaned_data['username_or_mobile']
    # 判断输入的是手机号还是用户名
    pattern = r'\d{11}'
    if re.search(pattern=pattern, string=username_or_mobile):  # 是手机号
        query_set =search_user_mobile(username_or_mobile)
        query_set_d = models.User.objects.filter(mobile_phone=username_or_mobile)
    else:
        query_set = search_user_name(username_or_mobile)
        query_set_d = models.User.objects.filter(username=username_or_mobile)

    # 能到这里一般不会为空了，但为了确保程序健壮性，依然判空
    if not query_set:
        return render(request, "UserAuth/alert_page.html", {'msg': '错误的用户信息'})

    # 重置密码
    query_set.password = md5_encrypt(form.cleaned_data['password'])
    change_user(query_set)
    query_set_d.update(password=form.cleaned_data['password'])
    return render(request, "UserAuth/alert_page.html", context={'msg': "您的密码已被重置！", 'success': True})





def generate_verification_code(request):
    """产生图片验证码"""
    stream = BytesIO()
    img, code = check_code()
    # img 储存到内存流中
    img.save(stream, 'png')
    request.session["login_verification_code"] = code
    request.session.set_expiry(120)  # 验证码120秒有效期
    return HttpResponse(stream.getvalue())


@csrf_exempt
def register_email(request):
    """注册时发送邮箱验证码"""
    if request.method == 'GET':
        data = {
            'state': False,
            'msg': 'Invalid request method'
        }
        return JsonResponse(data)

    email = request.POST.get('email_address')
    if not is_valid_email(email):
        data = {
            'state': False,
            'msg': 'Invalid Email format'
        }
        return JsonResponse(data)
    else:
        # 发送邮件
        state, code = send_sms_code(target_email=email)
        request.session['register_verification_code'] = code
        request.session.set_expiry(2 * 60)
        data = {
            'state': True,
            'msg': 'Send Email successfully'
        }
        return JsonResponse(data)


@csrf_exempt
def reset_password_email(request):
    """重置密码的邮箱验证码"""
    if not request.method == 'POST':
        data = {
            'state': False,
            'msg': 'Unsupported method'
        }
        return JsonResponse(data)

    username_or_mobile = request.POST.get('username_or_mobile')
    # 判断输入的是手机号还是用户名
    query_set = search_user_name(username_or_mobile)

    # 判空
    if not query_set:
        data = {
            'state': False,
            'msg': '不存在的用户名或手机号'
        }
        return JsonResponse(data)

    # 非空
    email = query_set.email
    # print(email)
    state_code, code = send_sms_code(target_email=email)
    if not state_code:  # 发送失败
        data = {
            'state': False,
            'msg': '邮件发送失败，请稍后重试'
        }
        return JsonResponse(data)

    # 发送成功, state_code == 0
    request.session['reset_password_verification_code'] = code  # 将重置验证码写入session
    request.session.set_expiry(2 * 60)
    # 返回信息
    return_msg = '验证码已发送至{}'.format(email)
    data = {
        'state': True,
        'msg': return_msg
    }
    return JsonResponse(data)


def index(request):
    userinfo = request.session.get("UserInfo")
    context = {
        'username': userinfo
    }
    return render(request, 'UserAuth/index.html', context=context)


def logout(request):
    request.session.clear() 
    return redirect("/auth/login/")


def check_login_state(request):
    user_info = request.session.get("UserInfo")
    if not user_info:
        return HttpResponse("您尚未登录")

    return HttpResponse("Welcome User: " + user_info["username"])


