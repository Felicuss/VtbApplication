from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import YandexUser, UserState
from app.models import UserInfo
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


@csrf_exempt
def alice_handler(request):
    buttons = []
    if request.method == "POST":
        request_data = json.loads(request.body)
        try:
            user_message = request_data['request']['original_utterance']
        except:
            user_message = " ".join(request_data['request']['nlu']['tokens'])
        session = request_data['session']
        version = request_data['version']
        yandex_id = session['user_id']

        user, created = YandexUser.objects.get_or_create(yandex_id=yandex_id)
        user_state, _ = UserState.objects.get_or_create(yandex_user=user)

        if not user.secret_key:
            if user_state.state == "WAITING_FOR_KEY":
                input_secret_key = user_message.strip()
                hashed_input_key = hash_key(input_secret_key)
                user_info_list = UserInfo.objects.all()
                key_found = False

                for user_info in user_info_list:
                    decrypted_key = decrypt_key(user_info.secret_key)
                    if decrypted_key == input_secret_key:
                        user.secret_key = hashed_input_key
                        user.save()
                        user_state.state = "CONNECTED"
                        user_state.save()
                        user_info.has_yandex_2fa = True
                        user_info.save()

                        response_text = "Ваш аккаунт успешно подключён!"
                        key_found = True
                        break

                if not key_found:
                    response_text = "Ошибка: секретный ключ не найден. Пожалуйста, проверьте и повторите попытку."
            else:
                user_state.state = "WAITING_FOR_KEY"
                user_state.save()
                response_text = "Пожалуйста, введите ваш секретный ключ."
        else:
            # Проверка на подтверждение входа
            confirmation_phrases = ["подтвердить вход", "да", "вход подтверждаю", 'войти', 'вход', 'подтверждаю']
            unlink_phrases = ["отвязать аккаунт", "отменить связь", "разъединить", "отключить"]

            if any(phrase in user_message.lower() for phrase in confirmation_phrases):
                user_info_list = UserInfo.objects.all()
                for user_info in user_info_list:
                    decrypted_key = decrypt_key(user_info.secret_key)
                    if decrypted_key == decrypt_key(user.secret_key):
                        user_info.made_2fa = True
                        user_info.save()
                        response_text = "Вход успешно подтверждён!"
                        break
                else:
                    response_text = "Ошибка: не удалось подтвердить вход."
            elif any(phrase in user_message.lower() for phrase in unlink_phrases):
                for user_info in UserInfo.objects.all():
                    decrypted_key = decrypt_key(user_info.secret_key)
                    if decrypted_key == decrypt_key(user.secret_key):
                        user_info.has_yandex_2fa = False
                        user_info.save()
                        break
                user.secret_key = None
                user.save()
                user_state.state = "DISCONNECTED"
                user_state.save()
                response_text = "Ваш аккаунт успешно отвязан."
            else:
                response_text = "Ваш аккаунт уже подключён. Если хотите подтвердить вход, нажмите кнопку ниже."
                buttons = [
                    {
                        "title": "Подтвердить вход",
                        "payload": {},
                        "hide": True
                    },
                    {
                        "title": "Отвязать аккаунт",
                        "payload": {},
                        "hide": True
                    }
                ]

        if buttons:
            response_data = {
                "response": {
                    "text": response_text,
                    "end_session": False,
                    "buttons": buttons
                },
                "session": session,
                "version": version
            }
        else:
            response_data = {
                "response": {
                    "text": response_text,
                    "end_session": False,
                },
                "session": session,
                "version": version
            }
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Недопустимый метод запроса"}, status=405)
