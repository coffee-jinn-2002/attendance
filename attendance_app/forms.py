from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "organization_name",
        )

# ログインフォームを追加
class LoginFrom(AuthenticationForm):
    class Meta:
        model = User

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password','email')