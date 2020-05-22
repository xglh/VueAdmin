from django.db import models
from django.contrib.auth.models import AbstractUser

role_choice = (('admin', 'admin'), ('editor', 'editor'))
# 用户表
class SysUser(AbstractUser):
    email = models.CharField(max_length=255, default='', verbose_name=u'邮箱')
    phone = models.CharField(max_length=255, default='', verbose_name=u'电话')
    avatar = models.CharField(max_length=255, default='', verbose_name=u'头像地址')
    nick_name = models.CharField(max_length=255, default='', verbose_name=u'昵称')
    role = models.CharField(max_length=255, choices=role_choice, verbose_name=u'角色')

    class Meta:
        db_table = 'user_sys_user'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.username