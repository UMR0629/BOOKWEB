from django.test import TestCase
from django.urls import reverse, resolve

from UserAuth.models import User
from UserInfo.views import index

from Groups.models import Village,Experience
from UserAuth.utils.encrypt import md5_encrypt
# Create your tests here.
class GroupIndexTest(TestCase):    #检测能否创建群组并进行相关的页面跳转

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
        self.group = Village.objects.create(villagename='group', admin=self.user,adminemail='2335915224@qq.com',maxim="good good study")
        index_url = reverse('Groups:group', kwargs={'pk': self.group.pk})
        url = reverse('Groups:show_group')
        add_url=reverse('Groups:applicants', kwargs={'pk': self.group.pk})
        self.response = self.client.get(url)
        self.indexresponse=self.client.get(index_url)
        self.addresponse=self.client.get(add_url)

    def test_index_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    #def test_index_url_resolve_index_view(self):
    #    view = resolve('/info/index/1/')
    #    self.assertEqual(view.func, index)

    def test_contain_home_url(self):
        home_url = reverse('Forum:home')
        self.assertContains(self.response, f'href="{home_url}"')

    def test_contain_group_insex(self):
        index_url=reverse('Groups:group', kwargs={'pk': self.group.pk})
        #index_url=reverse('Groups:show_group')
        self.assertContains(self.response, f'href="{index_url}"')
    
    def test_index_contain_home_url(self):
        home_url = reverse('Forum:home')
        self.assertContains(self.indexresponse, f'href="{home_url}"')

    def test_contain_applicant_insex(self):
        index_url=reverse('Groups:applicants', kwargs={'pk': self.group.pk})
        #index_url=reverse('Groups:show_group')
        self.assertContains(self.indexresponse, f'href="{index_url}"')
    
    #def test_contain_delete_insex(self):
        #index_url=reverse('Groups:delete',kwargs={'gid': self.group.pk,'theapplicant':self.user.username})
        #index_url=reverse('Groups:show_group')
        #self.assertContains(self.response, f'href="{index_url}"')
    #def test_contain_add_member_insex(self):
        #index_url=reverse('Groups:addmember', kwargs={'gid': self.group.pk,'theapplicant':self.user.username})
        #index_url=reverse('Groups:show_group')
        #self.assertContains(self.addresponse, f'href="{index_url}"')

class GroupLevelTest(TestCase):     #检测能否正常建立经验实例

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
        self.group = Village.objects.create(villagename='group', admin=self.user,adminemail='2335915224@qq.com',maxim="good good study")
        #url = reverse('Groups:show_group', kwargs={'pk': self.user.pk})
        self.level=Experience.objects.create(admin=self.group,user=self.user,experience=0)
        url = reverse('Groups:show_group')
        self.response = self.client.get(url)

    def test_index_status_code(self):
        self.assertEqual(self.response.status_code, 200)
