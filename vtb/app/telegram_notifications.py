import requests
from .models import Telegram

TELEGRAM_BOT_TOKEN = '7450582156:AAFXpRn7I3V-ZvvKsWwYwVJCq11Sw9wSO34'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"


def send_message_to_user(username, message):
    try:
        if '@' in username:
            username = username[1:]
        user = Telegram.objects.get(username=username)
        response = requests.post(TELEGRAM_API_URL, json={
            'chat_id': user.chat_id,
            'caption': message,
            'photo': 'https://sun9-58.userapi.com/impg/sl5oIRSXz2A2AALjxn'
                     'zidE1VqouaDaQth3kR9Q/m2ohdUl6-DE.jpg?size=1200x1000&quali'
                     'ty=95&sign=91ad9ff1dc875f39439a37d75fcbad09&type=album',
        })
        response.raise_for_status()
        return response.json()
    except Telegram.DoesNotExist:
        return {'error': 'Пользователь не найден в базе данных.'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
