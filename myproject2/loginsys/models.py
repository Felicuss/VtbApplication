from django.contrib.auth.models import User
from django.db import models


class UserSecretCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    connect_2auf = models.BooleanField(default=False)
    secret_code_mobile = models.TextField(blank=True)
    secret_code_alise = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - Secret Code"
