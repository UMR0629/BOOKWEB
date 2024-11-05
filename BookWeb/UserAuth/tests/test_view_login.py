from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.views import login
from UserAuth.models import User
from UserAuth.utils.Forms import LoginForm
from UserAuth.utils.encrypt import md5_encrypt

class LoginTest(TestCase):

    def setUp(self):
        username = 'duyuxin'
        password = 'Duyuxin123'
        mobile_phone = '15726359756'
        email = 'susumiya@sjtu.edu.cn'
        gender = 1
        hr_allowed = 1
        identity = 1
        User.objects.create(username=username, password=password, mobile_phone=mobile_phone, email=email,
                            gender=gender, hr_allowed=hr_allowed, identity=identity)
        url = reverse('UserAuth:login')
        self.response = self.client.get(url)

    def test_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_login_url_resolves_login_view(self):
        view = resolve('/auth/login/')
        self.assertEquals(view.func, login)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, LoginForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="password"', 1)


class SuccessLoginTest(TestCase):

    def setUp(self):
        username = 'duyuxin'
        password = 'Duyuxin123'
        mobile_phone = '15726359756'
        email = 'susumiya@sjtu.edu.cn'
        gender = 1
        hr_allowed = 1
        identity = 1
        User.objects.create(username=username, password=md5_encrypt(password), mobile_phone=mobile_phone, email=email,
                            gender=gender, hr_allowed=hr_allowed, identity=identity)
        url = reverse('UserAuth:login')
        #print('\n',url)
        self.response = self.client.get(url)
        #print('\n',self.response)
        self.client.get(reverse('UserAuth:gencode'))
        #print('\n',self.client.get(reverse('UserAuth:gencode')))
        verification_code = self.client.session.get('login_verification_code')
        #print("\nVerification Code:", verification_code)  # Print for debugging
   
        data = {
            'username': username,
            'password': password,
            'verification_code': verification_code
        }
        self.valid_login_response = self.client.post(url, data,follow=False)
        #print('\n' ,self.valid_login_response)
    
    def test_valid_login(self):
        self.assertEqual(self.valid_login_response.status_code, 302)
    
    def test_redirection(self):
        '''测试能否正常重定向到首页'''
        
        self.assertEqual(self.valid_login_response['location'], '/')
    
    def test_user_creation(self):
        """
        测试用户有没有正常创建
        """
        self.assertTrue(User.objects.exists())

    
    def test_user_authentication(self):
        """
        测试进入主页后用户有没有被放在会话中
        """
        response = self.client.get(reverse('Forum:home'))
        UserInfo = self.client.session['UserInfo']
        self.assertEqual(UserInfo.get('username'), 'duyuxin')
    

class InvalidLoginTest(TestCase):

    def setUp(self):
        username = 'duyuxin'
        password = 'Duyuxin123'
        mobile_phone = '15726359756'
        email = 'susumiya@sjtu.edu.cn'
        gender = 1
        hr_allowed = 1
        identity = 1
        User.objects.create(username=username, password=password, mobile_phone=mobile_phone, email=email,
                            gender=gender, hr_allowed=hr_allowed, identity=identity)
        url = reverse('UserAuth:login')
        self.response = self.client.get(url)
        self.client.get(reverse('UserAuth:gencode'))
        expected = ['username', 'password', 'verification_code']
        data = {
            'username': username,
            'password': password,
            'verification_code': 'AAAAA'
        }
        self.invalid_login_response = self.client.post(url, data)
        self.blank_login_response = self.client.post(url, {})
    
    def test_invalid_login_status_code(self):
        """
        不合法提交应该返回当前页面
        """
        self.assertEquals(self.invalid_login_response.status_code, 200)
    
    def test_blank_form_error(self):
        form = self.blank_login_response.context.get('form')
        self.assertTrue(form.errors)
