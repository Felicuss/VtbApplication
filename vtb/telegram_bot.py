import telebot
import sqlite3

TOKEN = '7450582156:AAFXpRn7I3V-ZvvKsWwYwVJCq11Sw9wSO34'
bot = telebot.TeleBot(TOKEN)


def save_user_to_db(username, user_id):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM telegram_users WHERE user_id = ?', (user_id,))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO telegram_users (username, user_id) VALUES (?, ?)', (username, user_id))
        conn.commit()

    conn.close()


@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.username
    user_id = message.from_user.id
    save_user_to_db(username, user_id)
    text = f"Привет, {username}! Ты зарегистрирован👍"
    photo_url = 'https://sun9-45.userapi.com/impg/-avgFJEDR9SUSzleMhU3eM5UOs_tg2CvMYmLaQ/L3kNTQ4QEh0.jpg?size=1200x1000&quality=95&sign=9c3a23b2c08c77e5a30b56a756f11272&type=album'
    bot.send_photo(message.chat.id, photo_url, caption=text)


bot.infinity_polling()
