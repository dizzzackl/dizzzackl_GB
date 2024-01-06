import sqlite3
import telebot

TOKEN = '6457775557:AAHmuj6O42eDdxCQGhZ8UFvHlSmY3zdcTFQ'

# Функция для обработки команды /start
def start(message):
    bot.reply_to(message, 'Привет! Чем я могу тебе помочь?'
                 "\nPS:'Пробив только по определённому городу и ещё бот в разработке'")
    bot.reply_to(message, text="Кидай ФИО, номер, TG ID")

# Функция для обработки введенных сообщений пользователей
def analyze_message(message):
    try:
        user_input = message.text
        # Подключение к базе данных в каждом потоке
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Поиск в базе данных по запросу пользователя
        cursor.execute('''
            SELECT * FROM users WHERE
            full_name LIKE ? OR
            phone_number LIKE ? OR
            distance LIKE ?
        ''', ('%' + user_input + '%', '%' + user_input + '%', '%' + user_input + '%'))
        results = cursor.fetchall()

        conn.close()

        if results:
            reply = ''
            for row in results:
                reply += f"Telegram ID: {row[1]}\n"
                reply += f"Full Name: {row[3]}\n"
                reply += f"Phone Number: {row[2]}\n"
                reply += f"Distance: {row[4]}\n"
                reply += "\n"
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, 'Информация не найдена')

    except Exception as e:
        error_message = f'Произошла ошибка: {str(e)}'
        bot.reply_to(message, error_message)

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    start(message)

# Обработка введенных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    analyze_message(message)

# Запуск бота
while True:
    try:
        bot.polling()
    except Exception as e:
        print(f'Произошла ошибка: {str(e)}')
        continue
