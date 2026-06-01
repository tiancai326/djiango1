from captcha.fields import CaptchaField
from django import forms

from .models import Member


class LoginForm(forms.Form):
    username = forms.CharField(
        label="账号",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入账号",
            }
        ),
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入密码",
            }
        ),
    )
    captcha = CaptchaField(label="验证码")


class SignonForm(forms.ModelForm):
    password1 = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入密码",
            }
        ),
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "请再次输入密码",
            }
        ),
    )
    email = forms.EmailField(
        label="邮箱",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入邮箱",
            }
        ),
    )
    captcha = CaptchaField(label="验证码")

    class Meta:
        model = Member
        fields = ("email", "username", "password1", "password2", "captcha")
        labels = {
            "username": "姓名",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "请输入姓名",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Member.objects.filter(email=email).exists():
            raise forms.ValidationError("该邮箱已经注册。")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Member.objects.filter(username=username).exists():
            raise forms.ValidationError("该账号已经注册。")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "两次输入的密码不一致。")
        return cleaned_data
