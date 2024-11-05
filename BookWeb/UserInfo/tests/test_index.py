from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.models import User
from UserInfo.views import index

from Forum.models import Topic, Post
from UserAuth.utils.encrypt import md5_encrypt

class InfoIndexTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='dyx', password=md5_encrypt('123'), mobile_phone='15726359738',
                                   email='2335915224@qq.com',
                                   gender=1, hr_allowed=1, identity=1)
        self.client.get(reverse('UserAuth:gencode'))
        data = {
            'username': 'dyx',
            'password': '123',
            'verification_code': self.client.session['login_verification_code']
        }
        self.client.post(reverse('UserAuth:login'), data)
        self.topic = Topic.objects.create(subject='hello', starter=self.user)
        url = reverse('UserInfo:index', kwargs={'pk': self.user.pk})
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_url_resolve_index_view(self):
        view = resolve('/info/index/1/')
        self.assertEqual(view.func, index)

    def test_contain_home_url(self):
        home_url = reverse('Forum:home')
        self.assertContains(self.response, f'href="{home_url}"')


    def test_contain_added_topic(self):
        url = reverse('Forum:topic_posts', kwargs={'pk': self.topic.pk})
        self.assertContains(self.response, f'href="{url}"')
