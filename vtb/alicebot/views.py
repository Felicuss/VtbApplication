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
    card = None  # To include an image card in the response
    if request.method == "POST":
        request_data = json.loads(request.body)
        print(request_data)
        try:
            user_message = request_data['request']['original_utterance']
        except:
            user_message = " ".join(request_data['request']['nlu']['tokens'])
            if user_message == '' or user_message == ' ' or user_message == '  ':
                user_message = ("".join(request_data['request']['payload']['text'])).strip()
        session = request_data['session']
        version = request_data['version']
        yandex_id = session['user_id']

        user, created = YandexUser.objects.get_or_create(yandex_id=yandex_id)
        user_state, _ = UserState.objects.get_or_create(yandex_user=user)
        if not user_message:
            response_text = (
                "Привет! 👋 Я помогу вам управлять двухфакторной аутентификацией. "
                "Для начала введите ваш ключ с нашего сайта или 'Помощь', чтобы узнать, что я умею. 😊"
            )
            buttons = [
                {"title": "Помощь", "payload": {'text': 'помощь'}, "hide": True},
            ]
            card = {
                "type": "BigImage",
                "image_id": "1652229/aef5555b595870d5408d",
                "title": "Привет! 👋",
                "description": response_text,
            }
            response_data = {
                "response": {
                    "text": response_text,
                    "end_session": False,
                    "buttons": buttons,
                    "card": card,
                },
                "session": session,
                "version": version,
            }
            return JsonResponse(response_data)
        # Check for "О навыке" command
        about_phrases = [
            "расскажи о себе", "что ты умеешь", "о навыке", "помощь", "помоги",
            "какие команды", "как работать", "как использовать", "информация о навыке"
        ]

        if any(phrase in user_message.lower() for phrase in about_phrases):
            response_text = (
                "😊 Привет! Я — твой помощник для управления двухфакторной аутентификацией через Яндекс. "
                "Вот что я умею:\n\n"
                "🔑 *Подключение аккаунта* — Скажи или напиши свой секретный ключ, чтобы подключить аккаунт.\n"
                "✅ *Подтверждение входа* — Подтверждай безопасные входы в систему.\n"
                "❌ *Отключение аккаунта* — Если нужно, легко отвяжу твой аккаунт.\n\n"
                "Для работы просто пиши команды, а я все сделаю! 🚀\n"
            )
            card = {
                "type": "BigImage",
                "image_id": "1540737/d1fc457bf0a80bb85d37",
                "title": "О навыке",
                "description": response_text,
            }
            response_data = {
                "response": {
                    "text": response_text,
                    "end_session": False,
                    "buttons": buttons,
                    "card": card
                },
                "session": session,
                "version": version
            }
            return JsonResponse(response_data)


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

                        response_text = "Ваш аккаунт успешно подключён! 🎉"
                        buttons = [
                            {
                                "title": "Подтвердить вход ✅",
                                "payload": {'text': 'подтвердить'},
                                "hide": True
                            },
                            {
                                "title": "Отвязать аккаунт ❌",
                                "payload": {'text': 'отвязать'},
                                "hide": True
                            }
                        ]
                        card = {
                            "type": "BigImage",
                            "image_id": "14236656/be67258622b6c759871a",
                            "title": "Успех! 🎉",
                            "description": "Ваш аккаунт подключён. Используйте кнопки для управления доступом.",
                        }
                        key_found = True
                        break

                if not key_found:
                    response_text = "Ошибка: секретный ключ не найден. Пожалуйста, проверьте и повторите попытку. 🔐"
                    card = {
                        "type": "BigImage",
                        "image_id": "965417/ac589715dc7f76ec3a10",
                        "title": "Ошибка ❌",
                        "description": response_text,
                    }
            else:
                user_state.state = "WAITING_FOR_KEY"
                user_state.save()
                response_text = "Пожалуйста, введите ваш секретный ключ. 🔑"
                card = {
                    "type": "BigImage",
                    "image_id": "965417/55b4c33d215570b38ef9",
                    "title": "Внимание! 🔑",
                    "description": response_text,
                }
                buttons = [
                    {"title": "Помощь", "payload": {'text': 'помощь'}, "hide": True}
                ]

        else:
            confirmation_phrases = ["подтвердить вход", "да", "вход подтверждаю", 'войти', 'вход', 'подтверждаю', 'подтвердить']
            unlink_phrases = ["отвязать аккаунт", "отменить связь", "разъединить", "отключить", 'отвязать']
            if any(phrase in user_message.lower() for phrase in confirmation_phrases):
                user_info_list = UserInfo.objects.all()
                for user_info in user_info_list:
                    decrypted_key = decrypt_key(user_info.secret_key)
                    if decrypted_key == decrypt_key(user.secret_key):
                        user_info.made_2fa = True
                        user_info.save()
                        response_text = "Вход успешно подтверждён! ✅"
                        buttons = [
                            {
                                "title": "Отвязать аккаунт ❌",
                                "payload": {'text': 'отвязать'},
                                "hide": True
                            }
                        ]
                        card = {
                            "type": "BigImage",
                            "image_id": "14236656/be67258622b6c759871a",
                            "title": "Вход подтверждён ✅",
                            "description": "Ваш вход успешно подтверждён. Если хотите отвязать аккаунт, используйте кнопку ниже.",
                        }
                        break
                else:
                    response_text = "Ошибка: не удалось подтвердить вход. ❌"
                    card = {
                        "type": "BigImage",
                        "image_id": "965417/ac589715dc7f76ec3a10",
                        "title": "Ошибка ❌",
                        "description": response_text,
                    }
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
                response_text = "Ваш аккаунт успешно отвязан. ❌"
                card = {
                    "type": "BigImage",
                    "image_id": "965417/30c3fa628c264559ca66",
                    "title": "Успешно ❌",
                    "description": response_text,
                }
            else:
                response_text = "Ваш аккаунт уже подключён. Если хотите подтвердить вход, нажмите кнопку ниже. ✅"
                buttons = [
                    {
                        "title": "Подтвердить вход ✅",
                        "payload": {'text': 'подтвердить'},
                        "hide": True
                    },
                    {
                        "title": "Отвязать аккаунт ❌",
                        "payload": {'text': 'отвязать'},
                        "hide": True
                    }
                ]

        response_data = {
            "response": {
                "text": response_text,
                "end_session": False,
            },
            "session": session,
            "version": version
        }

        if buttons:
            response_data["response"]["buttons"] = buttons

        if card:
            response_data["response"]["card"] = card

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Недопустимый метод запроса"}, status=405)
