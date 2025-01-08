import asyncio
import logging.config
import sys
import threading
import time
import traceback
import sched
from datetime import datetime

import aiogram

from config import BOT_API_TOKEN
from db_worker import (create_tables, insert_into_users, if_exists_in_users,
                       select_from_users, del_into_users, select_from_users_username, update_users_chat_id,
                       update_users_activate,
                       update_users_admin, select_all_from_users, update_users_times)
from keyboard import keyboard_first_menu, keyboard_select_country, keyboard_thr_menu
from sms_hub_API import get_Ballance, get_phone, chancel_phone, confirm_code, get_status

create_tables()

bot = aiogram.Bot(token=BOT_API_TOKEN,
                  parse_mode=aiogram.types.ParseMode.HTML)
loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)
dp = aiogram.Dispatcher(bot, loop=loop)

name_log = f'./logs/{datetime.now().strftime(("%Y.%m.%d_%H-%M-%S"))}.log'

dictLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "myFormatter",
            "filename": name_log
        },
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "formatter": "myFormatter",
            "stream": sys.stdout
        },
    },
    "loggers": {
        "SmsHub_Bot": {
            "handlers": ["fileHandler", "consoleHandler"],
            "level": "INFO",
        }
    },
    "formatters": {
        "myFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}

logging.config.dictConfig(dictLogConfig)
module_logger = logging.getLogger("SmsHub_Bot")


@dp.message_handler(commands=['start'])
async def start_message_command(message: aiogram.types.Message):
    logger = logging.getLogger("SmsHub_Bot.main.start")
    if message.chat.mention:
        if if_exists_in_users(message.chat.mention):
            update_users_chat_id(f'{message.chat.id}', message.chat.mention)
            user = select_from_users_username(message.chat.mention)

            if user.ADMIN:
                await bot.send_message(message.chat.id,
                                       'Здравствуйте! Вы являетесь администратором. Вам доступны такие команды:\n /menu, /append, /ban')
            else:
                await bot.send_message(message.chat.id, "Здравствуйте! Этот бот предназначен для получения смс из фб.",
                                       reply_markup=keyboard_first_menu)
    return


@dp.message_handler(commands=['menu'])
async def get_menu_message_command(message: aiogram.types.Message):
    logger = logging.getLogger("SmsHub_Bot.main.get_menu_message_command")
    if message.chat.mention:
        if if_exists_in_users(message.chat.mention):
            update_users_chat_id(f'{message.chat.id}', message.chat.mention)
            await bot.send_message(message.chat.id,
                                   f"Здравствуйте! Этот бот предназначен для получения смс из фб.\n Баланс: {get_Ballance()}",
                                   reply_markup=keyboard_first_menu)


@dp.message_handler(commands=['addadmin'])
async def add_admin(message: aiogram.types.Message):
    username = message.text.replace('/addadmin', '').replace(" ", "")
    insert_into_users(username)
    update_users_admin(username)


@dp.message_handler(commands=['append'])
async def append_users(message: aiogram.types.Message):
    user = select_from_users_username(message.chat.mention)
    if user.ADMIN:
        usernames = message.text.replace('/append', '').replace(" ", "").split(',')
        for username in usernames:
            insert_into_users(username)
    else:
        pass


@dp.message_handler(commands=['ban'])
async def ban_users(message: aiogram.types.Message):
    user = select_from_users_username(message.chat.mention)
    if user.ADMIN:
        usernames = message.text.replace('/ban', '').replace(" ", "").split(',')
        for username in usernames:
            del_into_users(username)
    else:
        pass


@dp.callback_query_handler(lambda call: call.data == "button_get_num")
async def select_country(call: aiogram.types.CallbackQuery):
    logger = logging.getLogger("SmsHub_Bot.main.select_country")
    if call.message.chat.mention:
        if if_exists_in_users(call.message.chat.mention):
            try:
                await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, "Выберите страну",
                                                    reply_markup=keyboard_select_country)
            except:
                logger.exception(traceback.format_exc())


@dp.callback_query_handler(lambda call: call.data.startswith("country"))
async def send_sms(call: aiogram.types.CallbackQuery):
    logger = logging.getLogger("SmsHub_Bot.main.send_sms")
    if call.message.chat.mention:
        if if_exists_in_users(call.message.chat.mention):
            try:
                country = call.data.split('_')[1]
                phone_data = get_phone(country)

                if phone_data == 'NO_NUMBERS':
                    try:
                        await bot.edit_message_text("Отсутствуют номера для выбраной страны.\nВыберите страну",
                                                    call.message.chat.id, call.message.message_id,
                                                    reply_markup=keyboard_select_country)

                    except:
                        await bot.send_message(call.message.chat.id,
                                               "Отсутствуют номера для выбраной страны.\nВыберите страну",
                                               reply_markup=keyboard_select_country)
                        logger.exception(traceback.format_exc())
                    return
                status = phone_data.split(":")[0]
                phone = phone_data.split(":")[2]
                activateID = phone_data.split(":")[1]

                update_users_activate(f'{call.message.chat.id}', activateID)

                await bot.edit_message_text(f'Ваш номер: {phone}',
                                            call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard_thr_menu)

            except:
                logger.exception(traceback.format_exc())


async def cancel_phone_act(chat_id, message_id):
    logger = logging.getLogger("SmsHub_Bot.main.cancel_phone")
    try:
        user = select_from_users(chat_id)
        chancel_phone(user.ACTIVATE_ID)
        if message_id == '0':
            await bot.send_message(chat_id, f"Номер отменён\n Баланс: {get_Ballance()}",
                                   reply_markup=keyboard_first_menu)
        else:
            await bot.edit_message_text(f"Номер отменён\n Баланс: {get_Ballance()}",
                                        chat_id, message_id,
                                        reply_markup=keyboard_first_menu)
    except:
        logger.exception(traceback.format_exc())


@dp.callback_query_handler(lambda call: call.data.startswith("button_cancel"))
async def cancel(call: aiogram.types.CallbackQuery):
    if call.message.chat.mention:
        if if_exists_in_users(call.message.chat.mention):
            await cancel_phone_act(f'{call.message.chat.id}', call.message.message_id)


async def getSMScode(chat_id):
    logger = logging.getLogger("SmsHub_Bot.main.getSMScode")
    try:
        user = select_from_users(f'{chat_id}')
        status_info = get_status(user.ACTIVATE_ID)
        if status_info == "STATUS_WAIT_CODE":
            await bot.send_message(chat_id,
                                   f'СМС ещё не пришла. Ожидаем.',
                                   reply_markup=keyboard_thr_menu)
            return
        status = status_info[0]
        code = status_info[1]
        confirm_code(user.ACTIVATE_ID)
        update_users_activate(f'{chat_id}', '0')
        if status_info != 'STATUS_CANCEL':
            await bot.send_message(chat_id,
                                   f'Ваш код: {status_info}',
                                   reply_markup=keyboard_thr_menu)
    except:
        logger.exception(traceback.format_exc())


@dp.callback_query_handler(lambda call: call.data.startswith("button_code"))
async def getCode(call: aiogram.types.CallbackQuery):
    if call.message.chat.mention:
        if if_exists_in_users(call.message.chat.mention):
            await getSMScode(call.message.chat.id)


async def f():
    module_logger.info("f_starter")

    try:
        while True:
            await asyncio.sleep(30)
            users = select_all_from_users()
            if users:
                for user in users:
                    if user.ACTIVATE_ID != '0':
                        await getSMScode(user.CHATID)
                        if user.TIMES == 15:
                            await cancel_phone_act(user.CHATID, '0')
                            update_users_times(user.CHATID, 0)
                        update_users_times(user.CHATID, user.TIMES)

    except:
        module_logger.exception(traceback.format_exc())


if __name__ == "__main__":
    try:
        module_logger.info("Program started")
        loop.create_task(f())
        loop.create_task(aiogram.executor.start_polling(dp, skip_updates=True))
        loop.run_forever()
        module_logger.info("End Program")
        loop.close()
    except:
        module_logger.exception(traceback.format_exc())
