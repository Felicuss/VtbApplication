from django.db import models
# Делаются модельки для бдшки
class Contact(models.Model):
    phone_id = models.CharField(max_length=50)  # Идентификатор телефона
    name = models.CharField(max_length=100)      # Имя контакта
    phone_number = models.CharField(max_length=50)  # Номер контакта
    device_id = models.CharField(max_length=50, blank=True, null=True)  # Уникальный ID устройства

    def __str__(self):
        return f"{self.name} - {self.phone_number}"
