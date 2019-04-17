from django import forms
from django.contrib import auth
from .models import UserProfile


class UserLoginForm(forms.Form):
    # 其中attrs为指定对应字段的前端样式，相当于html表单中的class指定样式
    username = forms.CharField(max_length=50, required=True, label='用户名', error_messages={'required': '请输入用户名'},
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, required=True, label='密码', error_messages={'required': '请输入密码'},
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # 定义clean方法，该方法是Django  Form中特定的方法，只要一执行is_valid这个数据检查方法，就会执行clean这个方法
    # 所以用户验证的内容可以放在这个方法里面，验证时只需要验证is_valid通过，则表示用户信息没有问题，可以直接登录
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        # 判断用户信息
        if user is None:
            # 用户信息错误，返回错误提示信息
            raise forms.ValidationError('用户名或密码错误！')
        else:
            # 用户信息正确
            self.cleaned_data['user'] = user
        return self.cleaned_data


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"原密码",
            }
        ),
    )
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"新密码",
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class UserRegisterForm(forms.Form):
    # 其中attrs为指定对应字段的前端样式，相当于html表单中的class指定样式
    username = forms.CharField(max_length=50, required=True, label='用户名', error_messages={'required': '请输入用户名'},
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(max_length=50, required=True, label="昵称", error_messages={'required': '请输入昵称'},
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, required=True, label='密码', error_messages={'required': '请输入密码'},
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=50, required=True, label="确认密码", error_messages={'required': '请再次输入密码'},
                                widget=forms.PasswordInput(attrs={'placeholder': "确认密码", 'class': 'form-control'}))

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError("两次输入的新密码不一样")
        else:
            if UserProfile.objects.filter(username=self.cleaned_data['username']).exists():
                raise forms.ValidationError("该用户已注册")
        return self.cleaned_data
