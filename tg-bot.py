import telebot
import sqlite3
import datetime
import logging
# import traceback2 as traceback

API_TOKEN = '7474722669:AAFbf97qqh_hRzZP9e2fuVL8bHKRc6YiQtU'

bot = telebot.TeleBot(API_TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    logging.info(f"Received /start command from {message.chat.id}")
    bot.reply_to(message, "发送一个 url 我就可以将它存入数据库！")

@bot.message_handler(content_types=['text'])
def save_url(message):
    url = message.text
    try:
        now = datetime.datetime.now()
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS urls
             (id INTEGER PRIMARY KEY, url TEXT, created_at DATETIME)''')
        c.execute("INSERT INTO urls (url, created_at) VALUES (?, ?)", (url, now.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        logging.info(f"Saved URL '{url}' to the database")
        bot.reply_to(message, f"已成功将 {url} 存入数据库,创建时间为 {now.strftime('%Y-%m-%d %H:%M:%S')}!")
    except Exception as e:
        # traceback.print_exc()
        logging.error(f"Failed to save URL '{url}' to the database")
        bot.reply_to(message, "抱歉，无法处理该 URL.")

logging.info("Bot started listening for messages")
bot.infinity_polling()