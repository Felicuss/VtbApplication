from http.client import responses

from django.template.context_processors import request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Contact
from .serializers import ContactSerializer
from django.http import JsonResponse, HttpResponse
import json


# Я попросил chatgpt описать этот класс
class ContactListCreate(generics.ListCreateAPIView):
    """
    Представление ContactListCreate предоставляет API для работы со списком контактов:
    - Метод GET возвращает список всех контактов.
    - Метод POST позволяет создать новый контакт.

    Атрибуты:
        - queryset: базовый набор данных, представляющий все объекты модели Contact.
        - serializer_class: указывает на сериализатор, используемый для преобразования данных модели.

    Методы:
        - create: переопределяет стандартный метод для создания контакта с дополнительной логикой.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        """
        Метод create выполняет логику создания контакта.

        Действия метода:
        1. Извлекает параметр `device_id` из строки запроса.
        2. Проверяет, существуют ли уже контакты для указанного `device_id`.
           - Если контакты уже были сохранены, выбрасывается ошибка `ValidationError`.
        3. Копирует данные запроса и добавляет `device_id` к ним.
        4. Валидирует данные с помощью сериализатора.
        5. Сохраняет контакт в базе данных, если данные валидны.

        Возвращаемое значение:
            - Успешно созданный объект контакта в формате JSON.

        Исключения:
            - ValidationError: если контакты для указанного устройства уже существуют.
        """
        device_id = request.query_params.get('device_id')

        # Проверка на существование контактов для данного устройства
        if Contact.objects.filter(device_id=device_id).exists():
            raise ValidationError("Контакты для этого устройства уже были сохранены.")  # Ошибка отобразится в логах

        # Подготовка данных для сериализации
        data = request.data.copy()
        data['device_id'] = device_id

        # Валидация и создание объекта
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Возвращает JSON-ответ с созданным объектом
        return Response(serializer.data)


from django.http import JsonResponse
import json

def yandex_handler(request):
    if request.method == 'POST':
        event = json.loads(request.body)
        user_text = event['request']['nlu']['tokens']
        user_text = ' '.join(user_text)
        response_text = 'pupupuupu'
        response = {
            "response": {
                "text": response_text,
                "end_session": False
            },
            "version": "1.0"
        }

        return JsonResponse(response, safe=False)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
