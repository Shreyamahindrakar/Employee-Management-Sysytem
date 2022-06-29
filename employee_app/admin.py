from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .models import *


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(AdminMain)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
