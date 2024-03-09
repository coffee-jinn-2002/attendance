from django.contrib import admin
from .models import User, Attendance, Workday

class AttendanceInline(admin.TabularInline):
    model = Attendance

class WorkdayInline(admin.TabularInline):
    model = Workday

class UserAdmin(admin.ModelAdmin):
    inlines = [
        AttendanceInline,
        WorkdayInline,
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Attendance)
admin.site.register(Workday)
