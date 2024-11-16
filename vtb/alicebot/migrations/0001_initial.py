# Generated by Django 5.1.3 on 2024-11-15 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="YandexUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("yandex_id", models.CharField(max_length=255, unique=True)),
                ("secret_key", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserState",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("state", models.CharField(default="DEFAULT", max_length=50)),
                (
                    "yandex_user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="alicebot.yandexuser",
                    ),
                ),
            ],
        ),
    ]
