from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入用户名",
                "autofocus": True,
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
