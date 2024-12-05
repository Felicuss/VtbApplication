import requests
from ..models import Telegram

TELEGRAM_BOT_TOKEN = '7450582156:AAFXpRn7I3V-ZvvKsWwYwVJCq11Sw9wSO34'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_message_to_user(username, message):
    try:
        user = Telegram.objects.get(username=username)
        response = requests.post(TELEGRAM_API_URL, json={
            'chat_id': user.chat_id[1:],
            'text': message
        })
        response.raise_for_status()
        return response.json()
    except Telegram.DoesNotExist:
        return {'error': 'Пользователь не найден в базе данных.'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
