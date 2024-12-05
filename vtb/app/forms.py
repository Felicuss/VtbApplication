from django import forms
from django.contrib.auth.models import User
from .models import UserInfo
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


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
        }),
        required=True,
        label="Password",
    )

    class Meta:
        model = User
        fields = ['email']

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            }),
        }

    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        # Create user
        user = User.objects.create_user(username=email, email=email, password=password)

        # Generate and save a secret_key
        secret_key = hash_key(generate_key())
        UserInfo.objects.create(user=user, secret_key=secret_key)

        return user
