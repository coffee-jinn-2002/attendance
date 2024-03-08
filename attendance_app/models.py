from django.db import models

from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_admin=False, date_joined=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_admin=is_admin,
            date_joined=date_joined
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            date_joined=None  # date_joined は必要なので None を渡す
        )
        user.is_admin = True
        user.is_staff = True  # スーパーユーザーはスタッフ権限を持つ必要がある
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 
    date_joined = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
