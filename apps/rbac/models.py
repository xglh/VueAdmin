from django.db import models
from django.contrib.auth.models import AbstractUser
from common.custom import BaseModel


class Menu(BaseModel):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True,
                            verbose_name="菜单名", help_text="菜单名")
    icon = models.CharField(max_length=50, null=True,
                            blank=True, verbose_name="图标", help_text="图标")
    path = models.CharField(max_length=158, null=True,
                            blank=True, verbose_name="链接地址", help_text="链接地址")
    is_frame = models.BooleanField(
        default=False, verbose_name="外部菜单", help_text="外部菜单")
    is_show = models.BooleanField(
        default=True, verbose_name="显示标记", help_text="显示标记")
    sort = models.IntegerField(
        null=True, blank=True, verbose_name="排序标记", help_text="排序标记")
    component = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="组件", help_text="组件")
    pid = models.ForeignKey("self", null=True, blank=True,
                            on_delete=models.SET_NULL, verbose_name="父菜单", help_text="父菜单")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rbac_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=30, unique=True,
                            verbose_name="权限名", help_text="权限名")
    method = models.CharField(max_length=50, null=True,
                              blank=True, verbose_name="方法", help_text="方法")
    pid = models.ForeignKey("self", null=True, blank=True,
                            on_delete=models.SET_NULL, verbose_name="父权限", help_text="父权限")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rbac_permission'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(
        max_length=32, unique=True, verbose_name="角色", help_text="角色")
    permissions = models.ManyToManyField(
        "Permission", blank=True, verbose_name="权限", help_text="权限")
    menus = models.ManyToManyField(
        "Menu", blank=True, verbose_name="菜单", help_text="菜单")
    environment = models.CharField(
        max_length=300, blank=True, null=True, verbose_name="环境", help_text="环境")
    desc = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="描述", help_text="描述")

    class Meta:
        db_table = 'rbac_role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']

class Organization(models.Model):
    """
    组织架构
    """
    organization_type_choices = (
        ("company", "公司"),
        ("department", "部门")
    )
    name = models.CharField(max_length=60, verbose_name="名称", help_text="名称")
    type = models.CharField(
        max_length=20, choices=organization_type_choices, default="company", verbose_name="类型", help_text="类型")
    pid = models.ForeignKey("self", null=True, blank=True,
                            on_delete=models.SET_NULL, verbose_name="父类组织", help_text="父类组织")

    class Meta:
        db_table = 'rbac_organization'
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(
        max_length=20, default="", verbose_name="姓名", help_text="姓名")
    mobile = models.CharField(
        max_length=11, default="", null=True, blank=True, verbose_name="手机号码", help_text="手机号码")
    email = models.EmailField(
        max_length=50, verbose_name="邮箱", help_text="邮箱")
    image = models.ImageField(
        upload_to="be-static/%Y/%m", default="image/default.png", max_length=100, null=True, blank=True)
    department = models.ForeignKey(
        "Organization", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="部门", help_text="部门")
    position = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="职位", help_text="部门")
    superior = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管", help_text="上级主管")
    roles = models.ManyToManyField(
        "Role", verbose_name="角色", blank=True, help_text="角色")

    class Meta:
        db_table = 'rbac_user_profile'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username
