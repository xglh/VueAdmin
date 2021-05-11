from django.db import models
from django.contrib.auth.models import AbstractUser
from common.basic import BaseModel


# role_choice = (('admin', 'admin'), ('editor', 'editor'))


# 角色表
class SysRole(BaseModel):
    role = models.CharField(max_length=255, unique=True, verbose_name='角色')
    role_name = models.CharField(max_length=255, verbose_name='角色名称')

    class Meta:
        db_table = 'user_sys_role'
        verbose_name = '系统角色'
        verbose_name_plural = '系统角色'

    def __str__(self):
        return self.role


# 用户表
class SysUser(AbstractUser):
    role_id = models.ForeignKey(SysRole, null=True, blank=True, on_delete=models.SET_NULL, db_column=u'role_id',
                                verbose_name=u'角色id')
    email = models.CharField(max_length=255, default='', verbose_name=u'邮箱')
    phone = models.CharField(max_length=255, default='', verbose_name=u'电话')
    avatar = models.CharField(max_length=255, default='', verbose_name=u'头像地址')
    nick_name = models.CharField(max_length=255, default='', verbose_name=u'昵称')

    class Meta:
        db_table = 'user_sys_user'
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.username
