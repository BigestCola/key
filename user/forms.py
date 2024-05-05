# user/forms.py

from django import forms
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

class SubordinateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'user_type', 'is_active', 'day_quota', 'monthly_quota']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("密码不匹配")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user