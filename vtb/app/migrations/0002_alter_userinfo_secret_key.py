# Generated by Django 5.1.3 on 2024-11-15 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="secret_key",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
