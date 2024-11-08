from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    secret_code = models.CharField(blank=True, null=True, default='')

    # Настраиваем уникальные `related_name` для полей `groups` и `user_permissions`
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Уникальное имя обратной ссылки для группы
        blank=True,
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Уникальное имя обратной ссылки для разрешений
        blank=True,
        verbose_name='user permissions'
    )
