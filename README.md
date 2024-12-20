# Описание проекта 🎉

Этот проект представляет собой решение, разработанное для хакатона VTB-API. Он позволяет пользователям подключать свои аккаунты к Яндекс Алисе и использовать её как способ двухфакторной аутентификации (2FA). Проект использует Django в качестве веб-фреймворка и включает в себя шифрование данных для обеспечения безопасности 🔒.

## Функциональные возможности 🚀
- **Подключение аккаунта**: Пользователи могут подключать свои аккаунты, вводя секретный ключ 🔑.
- **Подтверждение входа**: После подключения пользователи могут подтвердить свой вход с помощью простых команд, что делает процесс безопасным и удобным 👍.
- **Отвязывание аккаунта**: Пользователи могут отвязать свои аккаунты, если они больше не хотят использовать сервис, обеспечивая гибкость и контроль над своими данными ✂️.
- **Машина состояний**: Проект использует машину состояний для управления состоянием пользователя (ожидание ключа, подключение, отключение), что позволяет эффективно отслеживать и управлять процессами 🔄.

## Технологии 🛠️

- **Django**: Веб-фреймворк для разработки серверной части приложения, который обеспечивает быструю и удобную разработку 🌐. Django позволяет легко управлять базами данных и предоставляет мощные инструменты для создания RESTful API.

- **Cryptography**: Библиотека для шифрования и дешифрования секретных ключей, что гарантирует безопасность данных пользователей 🔐. Она обеспечивает надежное хранение и передачу конфиденциальной информации.

- **JSON**: Формат обмена данными между клиентом и сервером, который обеспечивает легкость и удобство в работе с данными 📊. JSON позволяет легко сериализовать и десериализовать данные, что делает взаимодействие между фронтендом и бэкендом более эффективным.

- **HTML/CSS/JavaScript**: Основные технологии для создания пользовательского интерфейса. HTML используется для разметки страниц, CSS — для стилизации, а JavaScript — для динамического взаимодействия с пользователем. 

  - **HTML**: Структурирует контент на веб-странице, позволяя пользователям вводить свои данные, такие как секретный ключ для подключения аккаунта.
  
  - **CSS**: Обеспечивает стиль и оформление интерфейса, делая его более привлекательным и удобным для пользователей. Например, можно использовать Flexbox и Grid для создания адаптивного дизайна, который будет хорошо выглядеть на любых устройствах 📱💻.
  
  - **JavaScript**: Используется для отправки асинхронных запросов к бэкенду. Это позволяет пользователям подключать свои аккаунты и подтверждать вход без перезагрузки страницы.

Эти технологии в совокупности создают мощное и безопасное приложение, которое обеспечивает удобный и интуитивно понятный интерфейс для пользователей. Мы стремимся к тому, чтобы сделать процесс аутентификации максимально простым и безопасным! 🌟

## Установка и запуск ⚙️
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Felicuss/VtbApplication.git
   ```
2. Перейдите в директорию проекта:
   ```bash
   cd VtbApplication
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

Теперь вы можете подключить свой аккаунт к Яндекс Алисе и наслаждаться безопасным входом! 🎊

## Лицензия 📄
Этот проект лицензирован под MIT License. Вы можете свободно использовать и изменять его в соответствии с условиями лицензии.

Спасибо за внимание! Надеемся, вам понравится наш проект! 😊



![screen1](https://github.com/user-attachments/assets/2a243b5a-18cd-4648-b5bf-412525c595a1)
![screen_tg](https://github.com/user-attachments/assets/cc7edcaf-ed6e-44ed-abbd-f35945fb277b)
![screen_alice](https://github.com/user-attachments/assets/cf7ec3e8-1926-43f1-86a9-6bd26e20ee82)
![image](https://github.com/user-attachments/assets/74b6709d-b738-4998-a483-9a0e7e016bf1)
https://t.me/mojarung
