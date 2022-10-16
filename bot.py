from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler)
from config import TOKEN
from bot_functions import *

if __name__ == '__main__':
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    todo_conversation_handler = ConversationHandler(
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            WELCOME_MENU: [MessageHandler(Filters.text, welcome_menu)],
            MAIN_MENU: [MessageHandler(~Filters.command, main_menu)],
            CHOICE: [MessageHandler(~Filters.command, choice)],
            VIEW: [MessageHandler(~Filters.command, view)],
            ADD_TASK: [MessageHandler(~Filters.command, add_task)],
            ADD_DATE: [MessageHandler(~Filters.command, add_date)],
            DELETE: [MessageHandler(~Filters.command, delete)],
            DONE: [MessageHandler(~Filters.command, done)]
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(todo_conversation_handler)

    # Запуск
    print('server started')
    updater.start_polling()
    updater.idle()
