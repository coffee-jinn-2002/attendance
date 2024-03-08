from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView,  LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginFrom

# Create your views here.

class IndexView(TemplateView):
    """ ホームビュー """
    template_name = "attendance_app/index.html"


class SignupView(CreateView):
    """ ユーザー登録用ビュー """
    form_class = SignUpForm # 作成した登録用フォームを設定
    template_name = "attendance_app/signup.html" 
    success_url = reverse_lazy("attendance_app:index") # ユーザー作成後のリダイレクト先ページ

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
    
# ログインビューを作成
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "attendance_app/login.html"

# LogoutViewを追加
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("attendance_app:index")