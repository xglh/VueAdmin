from django.contrib import admin

# Register your models here.
from user.models import SysUser

admin.site.register(SysUser)