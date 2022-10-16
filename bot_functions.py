import logging
import csv_functions as csvf
from config import TOKEN
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import stickers as st

logging.basicConfig(filename='log.txt',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)

WELCOME_MENU, MAIN_MENU, CHOICE, VIEW, ADD_TASK, ADD_DATE, DONE, DELETE = range(
    8)


def start(update, context):
    reply_keyboard = [['НАЧАТЬ', 'ВЫХОД']]
    markup_key = ReplyKeyboardMarkup(
        reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_sticker(update.message.chat.id, st.hello)
    context.bot.send_message(update.effective_chat.id,
                             f'Добро пожаловать в список задач, {update.effective_user.first_name}!\n'
                             'Для начала работы со списком нажмите кнопку <НАЧАТЬ>\n'
                             'Для выхода нажмите кнопку <ВЫХОД>', reply_markup=markup_key)

    return WELCOME_MENU


def welcome_menu(update, context):
    button = update.message.text
    button = str(button)
    if button == 'НАЧАТЬ':
        return main_menu(update, context)
    if button == 'ВЫХОД':
        return cancel(update, context)
    else:
        reply_keyboard = [['НАЧАТЬ', 'ВЫХОД']]
        markup_key = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(
            "Вы ввели что-то не то. Попробуйте еще раз.", reply_markup=markup_key)
        return WELCOME_MENU


def main_menu(update, context):
    reply_keyboard = [
        ['ВСЕ ЗАДАЧИ', 'ДОБАВИТЬ', 'УДАЛИТЬ', 'ВЫПОЛНЕНО', 'ВЫХОД']]
    markup_key = ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        'Выберите действие с задачами.', reply_markup=markup_key)
    return CHOICE


def choice(update, context):
    choice = update.message.text
    if choice == 'ВСЕ ЗАДАЧИ':
        return view(update, context)
    if choice == 'ДОБАВИТЬ':
        update.message.reply_text("Введите текст задачи:")
        return ADD_TASK
    if choice == 'УДАЛИТЬ':
        update.message.reply_text("Введите какую задачу удалить: ")
        return DELETE
    if choice == 'ВЫПОЛНЕНО':
        update.message.reply_text(
            "Введите какую задачу пометить выполненной: ")
        return DONE
    if choice == 'ВЫХОД':
        return cancel(update, context)


def view(update, context):
    context.bot.send_message(update.effective_chat.id,
                             f'Ваш список дел ниже.')
    user_tasks = csvf.read_csv()
    message_tasks = csvf.view_tasks(user_tasks)
    update.message.reply_text(message_tasks)
    context.bot.send_sticker(update.message.chat.id, st.complete)
    update.message.reply_text(
        "Выберите дайльнейшее действие. Или нажмите /cancel для завершения работы.")
    return MAIN_MENU


def add_task(update, context):
    context.bot.send_sticker(update.message.chat.id, st.listen)
    task = update.message.text
    task = task.lower()
    context.user_data['task'] = task
    update.message.reply_text(
        "Напишите дату задачи(н-р сегодня или в формате дд/мм/гг): ")
    return ADD_DATE


def add_date(update, context):
    date = update.message.text
    date = date.lower()
    context.user_data['date'] = date
    task = context.user_data.get('task')
    record = {}
    user_tasks = csvf.read_csv()
    record['задача'] = task
    record['дата'] = date
    csvf.write_csv(record)
    context.bot.send_sticker(update.message.chat.id, st.complete)
    update.message.reply_text(
        "Готово! Выберите дайльнейшее действие или нажмите /cancel для завершения работы.")
    return MAIN_MENU


def delete(update, context):
    task_to_del = update.message.text
    status = csvf.delete_csv(task_to_del)
    update.message.reply_text(status)
    update.message.reply_text(
        "Выберите дайльнейшее действие. Или нажмите /cancel для завершения работы.")
    return MAIN_MENU


def done(update, context):
    task_to_mark = update.message.text
    status = csvf.mark_csv(task_to_mark)
    update.message.reply_text(status)
    update.message.reply_text(
        "Выберите дайльнейшее действие. Или нажмите /cancel для завершения работы.")
    return MAIN_MENU


def cancel(update, context):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    # Отвечаем на отказ поговорить
    context.bot.send_sticker(update.message.chat.id, st.goodbye)
    context.bot.send_message(update.effective_chat.id,
                             f'До встречи!'
                             'Для начала работы нажмите /start')
    return ConversationHandler.END
