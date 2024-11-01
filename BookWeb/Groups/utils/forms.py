'''from django import forms  
from models import Village  
from UserAuth.models import User  
  
class CreateForm(forms.ModelForm):

    class Meta:  
        model = Village  
        fields = ['villagename', 'maxim', 'adminemail']  # 注意：我们没有包括 admin 字段，因为它是一个 ForeignKey，通常不适合直接在表单中处理  
  
    def __init__(self, *args, **kwargs):  
        self.admin_user = kwargs.pop('admin_user', None)  
        super(RegisterForm, self).__init__(*args, **kwargs)  
  
    def clean_adminemail(self):  
        # 这里可以添加额外的验证逻辑，比如检查邮箱是否已经被其他村长使用  
        return self.cleaned_data['adminemail']  
  
    def save(self, commit=True):  
        instance = super(RegisterForm, self).save(commit=False)  
        instance.admin = self.admin_user  
        if commit:  
            instance.save()  
        return instance'''

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from Groups import models
from UserAuth.utils.bootstrapform import BootStrapForm
from Groups.utils.validators import is_name_valid
from UserAuth.utils.encrypt import md5_encrypt

class CreateForm(BootStrapForm, forms.ModelForm):
    villagename = forms.CharField(
        label="村名",
        max_length=32,
    )
    maxim = forms.CharField(
        label="宣言",
        max_length=32,
    )
    adminemail = forms.CharField(
        label="邮箱",
        max_length=32,
        validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', '邮箱格式错误')]
    )
    verification_code = forms.CharField(
        label="验证码",
        max_length=10
    )
    class Meta:
        model = models.Village
        fields = ['villagename', 'maxim', 'adminemail', 'verification_code']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_villagename(self):
        #if not is_name_valid(self.cleaned_data['villagename']):
            #raise ValidationError("村名不允许存在特殊字符")
        if models.User.objects.filter(username=self.cleaned_data["villagename"]).exists():
            raise ValidationError("村名已存在")
        return self.cleaned_data['villagename']

    '''def clean_mobile_phone(self):
        if models.User.objects.filter(mobile_phone=self.cleaned_data['mobile_phone']).exists():
            raise ValidationError("手机号已存在")
        return self.cleaned_data['mobile_phone']

    def clean_email(self):
        if models.User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise ValidationError("邮箱已存在")
        return self.cleaned_data['email']'''
    def clean_verification_code(self):
        code_in_session = self.request.session.get('register_verification_code')
        if not code_in_session:
            raise ValidationError("验证码已过期")
        if not self.cleaned_data['verification_code'] == code_in_session:
            raise ValidationError("验证码错误")
        return self.cleaned_data['verification_code']
    

