from rest_framework import serializers
from .models import Contact
# класс сериализатора, который преобразует объекты модели Contact
# в формат данных JSON и обратно, что удобно для передачи данных через API.

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone_id', 'name', 'phone_number', 'device_id']
