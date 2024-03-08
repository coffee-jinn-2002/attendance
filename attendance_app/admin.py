from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User

# Register your models here.
admin.site.register(User)  # Userモデルを登録
# admin.site.register(User, UserAdmin)  # Userモデルを登録
admin.site.unregister(Group)  # Groupモデルは不要のため非表示にします