import logging
import settings
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def main():
    updater = Updater(settings.TOKEN_TELEGRAMM)
    dispatcher = updater.dispatcher

    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text & ~Filters.command, check_website)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который проверяет, заблокирован ли сайт Роскомнадзором. Пожалуйста, отправь мне домен для проверки. Например: vk.com")

def check_website(update, context):
    domain = update.message.text.strip()

    url = f"https://reestr.rublacklist.net/api/v3/domains/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if domain in data:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Сайт заблокирован по требованию правоохранительных органов.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Сайт не заблокирован.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка при выполнении запроса. Пожалуйста, попробуйте позже.")\

if __name__ == '__main__':
    main()
