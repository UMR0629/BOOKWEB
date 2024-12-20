from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.models import User
from UserInfo.views import modify

from Forum.models import Topic, Post
from UserAuth.utils.encrypt import md5_encrypt

class InfoResumeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='duyuxin', password=md5_encrypt('Duyuxin123'), mobile_phone='15726359756',
                                   email='2335915224@qq.com',
                                   gender=1, hr_allowed=1, identity=1)
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'duyuxin',
            'password': 'Duyuxin123',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        url = reverse('UserInfo:modify')
        self.response = self.client.get(url)
    
    def test_index_status_code(self):
        self.assertEqual(self.response.status_code, 200)
    
    def test_index_url_resolve_index_view(self):
        view = resolve('/info/modify/')
        self.assertEqual(view.func, modify)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contain_form(self):
        self.assertContains(self.response, '<form')

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 11)
        self.assertContains(self.response, 'type="text"', 6)


class SuccessfulModifyTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='duyuxin', password=md5_encrypt('Duyuxin123'), mobile_phone='15726359756',
                                        email='2335915224@qq.com',
                                        gender=1, hr_allowed=1, identity=1, school='SJTU')
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'duyuxin',
            'password': 'Duyuxin123',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        url = reverse('UserInfo:modify')
        self.client.get(url)
        data = {
            'id': self.user.pk,
            'username': self.user.username,
            'mobile_phone': self.user.mobile_phone,
            'email': self.user.email,
            'gender': 0,
            'edu_ground': '',
            'school': 'FDU',
            'major': '',
            'my_love_book': '',
            'my_love_author': '',
            'maxim': '',
        }
        self.success_response = self.client.post(reverse('UserInfo:user_info'), data)

    def test_valid_modify(self):
        self.assertEqual(self.success_response.status_code, 200)