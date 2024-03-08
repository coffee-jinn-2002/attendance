from django.urls import path

from . import views

app_name = "attendance_app"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("ad/dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"), 
    path("user/dashboard/", views.UserDashboardView.as_view(), name="user_dashboard"),
]

# urlpatterns = [
#     path("", views.IndexView.as_view(), name="index"),
#     path('signup/', views.SignupView.as_view(), name="signup"),
#     path('login/', views.LoginView.as_view(), name="login"),
#     path('logout/', views.LogoutView.as_view(), name="logout"),
# ]
