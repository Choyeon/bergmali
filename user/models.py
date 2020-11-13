import re

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('用户必须有一个电子邮件地址')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        用给定的电子邮件创建并保存超级用户，创建时间和密码.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    email = models.EmailField(
        verbose_name='Email地址',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    # 是否活跃
    is_active = models.BooleanField(default=True)
    # 是否是管理员
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # 用户通过其电子邮件地址标识
        return self.email

    def get_short_name(self):
        # 用户通过其电子邮件地址标识
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        # 用户是否具有特定权限?
        # 可能的最简单答案：是，总是
        return True

    def has_module_perms(self, app_label):
        # 用户是否有权查看应用程序“ app_label”？
        # 可能的最简单答案：是，总是
        return True

    @property
    def is_staff(self):
        # 用户是工作人员吗？
        # 最简单的答案：所有管理员都是员工
        return self.is_admin


User = get_user_model()


class Userinfo(models.Model):
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE, related_name='info')
