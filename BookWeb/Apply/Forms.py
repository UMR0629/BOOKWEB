from Apply import models 
from django import forms
from django.core.validators import RegexValidator
class BootStrapForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环每个字段为其插件进行设置
        for name, field in self.fields.items():
            # 字段中有属性，则增加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = "请输入" + field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    # 还可以添加其他的标签，例如placeholder
                    "placeholder": field.label
                }

class CreateForm(BootStrapForm, forms.ModelForm):
    applicant = forms.CharField(
        label="用户名",
        max_length=32,
    )
    applyreason = forms.CharField(
        label="入村理由",
        max_length=32,
    )
    applyemail = forms.CharField(
        label="个人邮箱",
        max_length=32,
        validators=[RegexValidator(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', '邮箱格式错误')]
    )
    class Meta:
        model = models.Application
        fields = ['applicant', 'applyreason', 'applyemail']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    