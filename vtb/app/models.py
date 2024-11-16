from django.contrib.auth.models import User
from django.db import models

import secrets
from cryptography.fernet import Fernet

secret_key = b'gnehx6C8O2o2JquonBEzPVrDGfdnRns8K34zzkqiPi8='


def hash_key(key):
    f = Fernet(secret_key)
    encrypted_key = f.encrypt(key.encode())
    return encrypted_key.decode()


def decrypt_key(encrypted_key):
    f = Fernet(secret_key)
    decrypted_key = f.decrypt(encrypted_key.encode())
    return decrypted_key.decode()


def generate_key():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    key = ''.join(secrets.choice(characters) for _ in range(8))
    return key


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    secret_key = models.CharField(max_length=255, default=hash_key(generate_key()))
    has_yandex_2fa = models.BooleanField(default=False)
    made_2fa = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Secret Key"
