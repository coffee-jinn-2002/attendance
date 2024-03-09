from django.contrib import admin
from .models import User, Attendance, Workday, Break

class AttendanceInline(admin.TabularInline):
    model = Attendance

class BreakInline(admin.TabularInline):
    model = Break

class WorkdayAdmin(admin.ModelAdmin):
    inlines = [
        AttendanceInline,
        BreakInline,
    ]

admin.site.register(User)
admin.site.register(Workday, WorkdayAdmin)

# class AttendanceInline(admin.TabularInline):
#     model = Attendance

# class WorkdayInline(admin.TabularInline):
#     model = Workday

# class BreakInline(admin.TabularInline):
#     model = Break

# class UserAdmin(admin.ModelAdmin):
#     inlines = [
#         AttendanceInline,
#         WorkdayInline,
#     ]

# admin.site.register(User, UserAdmin)
# admin.site.register(Attendance)
# admin.site.register(Workday)
# admin.site.register(Break)