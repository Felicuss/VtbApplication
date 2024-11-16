# Описание проекта
Этот проект представляет собой решение, разработанное для хакатона VTB-API. Он позволяет пользователям подключать свои аккаунты к яндекс алисе и использовать её как способ 2fa. Проект использует Django в качестве веб-фреймворка и включает в себя шифрование данных для обеспечения безопасности.

### Функциональные возможности
- Подключение аккаунта: Пользователи могут подключать свои аккаунты, вводя секретный ключ.
- Подтверждение входа: После подключения пользователи могут подтвердить свой вход с помощью простых команд.
- Отвязывание аккаунта: Пользователи могут отвязать свои аккаунты, если они больше не хотят использовать сервис.
- Машина состояний: Проект использует машину состояний для управления состоянием пользователя (ожидание ключа, подключение, отключение).
### Технологии
- Django: Веб-фреймворк для разработки серверной части приложения.
- Cryptography: Библиотека для шифрования и дешифрования секретных ключей.
- JSON: Формат обмена данными между клиентом и сервером.

![mojarung12345](https://github.com/user-attachments/assets/c32f515d-2242-4d4f-b35d-afc05ddf42d4)
