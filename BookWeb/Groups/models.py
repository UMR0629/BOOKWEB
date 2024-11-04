from UserAuth.models import User
from django.db import models

# Create your models here.
class Village(models.Model):
    villagename = models.CharField(verbose_name="村名", max_length=32)
    members = models.ManyToManyField(User, related_name='groups')  #要从Group实例查询其成员（User实例），使用group_instance.members.all()
    #要从User实例查询其所属的群组（Group实例），使用user_instance.groups.all()，这里的groups是由Group模型中的members字段的related_name参数指定的反向关系名称。
    admin = models.ForeignKey(User, related_name='admin_groups', on_delete=models.CASCADE)
    adminemail=models.CharField(verbose_name="村长信箱", max_length=32)
    maxim = models.CharField(verbose_name="宣言", max_length=30, blank=True)
    #numbers of members
    #numbers of topics
    def __str__(self):
        return self.villagename
    
class Experience(models.Model):
    experience=models.SmallIntegerField(verbose_name="经验")
    admin = models.ForeignKey(Village, related_name='admin_groups', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='exp', on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    