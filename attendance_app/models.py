from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, organization_name=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            organization_name=organization_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, organization_name=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(username, email, password, organization_name, **extra_fields)

    def create_staff(self, username, email, password=None, organization_name=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        return self.create_user(username, email, password, organization_name, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False) 
    date_joined = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 勤怠関連
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('出勤前', '出勤前'),
        ('出勤中', '出勤中'),
        ('休憩中', '休憩中'),
        ('退勤済み', '退勤済み'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='出勤前')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    total_work_time = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.total_work_time = self.end_time - self.start_time
        super().save(*args, **kwargs)

class Break(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)

class Workday(models.Model):
    attendance = models.OneToOneField(Attendance, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    date = models.DateField(default=timezone.now)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    break_start_time = models.DateTimeField(blank=True, null=True)
    break_end_time = models.DateTimeField(blank=True, null=True)
    total_work_time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s workday on {self.date}"