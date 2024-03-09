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
from django.views.generic import FormView
from .models import User, Attendance
# from .forms import AttendanceForm
from django.utils import timezone
import datetime

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログイン中のユーザーの組織名を取得
        organization_name = self.request.user.organization_name
        # 組織名に基づいてユーザーをフィルタリングして取得
        users = User.objects.filter(organization_name=organization_name)
        context['users'] = users
        return context



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
    
# 勤怠機能
class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'attendance_app/userdash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            attendance = Attendance.objects.get(user=user)
        except Attendance.DoesNotExist:
            # 関連する Attendance オブジェクトが存在しない場合は新しいオブジェクトを作成
            attendance = Attendance.objects.create(user=user, status='出勤前')
        context['attendance'] = attendance
        # 現在時刻をテンプレートに渡す
        context['current_date'] = datetime.date.today().strftime('%Y年%m月%d日')
        context['current_time'] = timezone.localtime(timezone.now()).strftime('%H:%M:%S')
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        action = request.POST.get('action')
        attendance = Attendance.objects.filter(user=user).latest('id')
        
        if action == 'start':
            attendance.start_time = timezone.now()
            attendance.status = '出勤中'
            attendance.save()
        elif action == 'break_start':
            attendance.break_start_time = timezone.now()
            attendance.status = '休憩中'
            attendance.save()
        elif action == 'break_end':
            attendance.break_end_time = timezone.now()
            attendance.status = '出勤中'
            attendance.save()
        elif action == 'end':
            attendance.end_time = timezone.now()
            attendance.status = '退勤済み'
            attendance.save()
        
        return redirect('attendance_app:user_dashboard')
