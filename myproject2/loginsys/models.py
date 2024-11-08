from django.contrib.auth.models import User
from django.db import models


class UserSecretCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret_code = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Secret Code"
