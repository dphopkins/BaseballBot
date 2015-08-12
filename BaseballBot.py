import telebot

API_TOKEN = '59094683:AAG5mNV5wOSTFq8VjfdU0OlDETvuHMXdgBM'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am BaseballBot!
Just say anything nice and I'll say the exact same thing to you!\
""")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.polling()

while True:
    pass