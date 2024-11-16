# app/models.py
from django.db import models


class YandexUser(models.Model):
    yandex_id = models.CharField(max_length=255, unique=True)
    secret_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.yandex_id}: {self.secret_key}"


class UserState(models.Model):
    yandex_user = models.OneToOneField(YandexUser, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, default="DEFAULT")

    def __str__(self):
        return f"{self.yandex_user.yandex_id}: {self.state}"
