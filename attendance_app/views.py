from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView,  LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginFrom, CreateUserForm
from .models import User
from django.views.generic import FormView

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
    
class LoginView(BaseLoginView):
    form_class = LoginFrom
    template_name = "attendance_app/login.html"

    def form_valid(self, form):
        # 親クラスのform_validを呼び出してログインを処理
        response = super().form_valid(form)
        # ログインしたユーザーを取得
        user = form.get_user()
        # is_adminの値によってリダイレクト先を設定
        if user.is_authenticated and user.is_admin:
            return HttpResponseRedirect(reverse('attendance_app:admin_dashboard'))
        else:
            return HttpResponseRedirect(reverse('attendance_app:user_dashboard'))

# LogoutViewを追加
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("attendance_app:index")

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance_app/admindash.html'


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance_app/userdash.html'


class CreateUserView(FormView):
    template_name = 'attendance_app/create_user.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        organization_name = self.request.user.organization_name
        # create_staffメソッドを使用して新しいユーザーを作成
        User.objects.create_staff(username=username, email=email, password=password, organization_name=organization_name)
        return redirect('attendance_app:admin_dashboard')