# Модуль отвечающий за работу с базой данных
# The module responsible for working with the database
import logging

import traceback

from peewee import (MySQLDatabase, Model, CharField, IntegerField, TextField, BooleanField)

module_logger = logging.getLogger("NutritionBot.db_worker")

db = MySQLDatabase(
    host='127.0.0.1',
    user='root',
    passwd='',
    database='smsHub_bot_db',
    port=3306
)


class Users(Model):
    CHATID = CharField(32)
    USERNAME = CharField(32)
    MENU = TextField()
    ADMIN = BooleanField()
    ACTIVATE_ID = TextField(default='0')
    TIMES = IntegerField()

    class Meta:
        database = db


def create_tables():
    logger = logging.getLogger("SmsHub_Bot.db_worker.create_tables")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        db.create_tables([Users])
    except:
        logger.exception(traceback.format_exc())
    else:
        db.commit()
        db.close()


def insert_into_users(username):
    logger = logging.getLogger("SmsHub_Bot.db_worker.insert_into_users")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        Users.create(USERNAME=username,
                     MENU='0', ADMIN=0)
    except:
        logger.exception(traceback.format_exc())
    else:
        db.commit()
        db.close()


def if_exists_in_users(username):
    logger = logging.getLogger("SmsHub_Bot.db_worker.if_exists_in_users")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        if Users.select().where(Users.USERNAME == username).exists():
            db.close()
            return True
        else:
            db.close()
            return False
    except:
        logger.exception(traceback.format_exc())


def select_all_from_users():
    logger = logging.getLogger("SmsHub_Bot.db_worker.select_all_from_users")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        users = Users.select()
        db.close()
        return users
    except:
        db.close()
        logger.exception(traceback.format_exc())


def select_from_users(chat_id):
    logger = logging.getLogger("SmsHub_Bot.db_worker.select_from_users")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        users = Users.select()
        for user in users:
            if user.CHATID == chat_id:
                db.close()
                return user
        db.close()
        return user
    except:
        db.close()
        logger.exception(traceback.format_exc())


def select_from_users_username(username):
    logger = logging.getLogger("SmsHub_Bot.db_worker.select_from_users_username")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        users = Users.select()
        for user in users:
            if user.USERNAME == username:
                db.close()
                return user
        db.close()

    except:
        db.close()
        logger.exception(traceback.format_exc())


def update_users_menu(chat_id, menu):
    logger = logging.getLogger("SmsHub_Bot.db_worker.update_users_menu")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        Users.update({Users.MESSAGE_ID: menu}).where(Users.MESSAGE_ID == chat_id).execute()
    except:
        db.close()
        logger.exception(traceback.format_exc())
    else:
        db.commit()
        db.close()


def update_users_activate(chat_id, activate):
    logger = logging.getLogger("SmsHub_Bot.db_worker.update_users_activate")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        Users.update({Users.ACTIVATE_ID: activate}).where(Users.CHATID == chat_id).execute()
    except:
        db.close()
        logger.exception(traceback.format_exc())
    else:
        db.commit()
        db.close()


def update_users_chat_id(chat_id, username):
    logger = logging.getLogger("SmsHub_Bot.db_worker.update_users_chat_id")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        Users.update({Users.CHATID: chat_id}).where(Users.USERNAME == username).execute()
    except:
        db.close()
        logger.exception(traceback.format_exc())
    else:
        db.commit()
        db.close()


def update_users_times(chat_id, times):
    logger = logging.getLogger("SmsHub_Bot.db_worker.update_users_times")
    try:
        if times > 15:
            _times = -1
        else:
            _times = times + 1
        if not db.is_closed():
            db.close()
        db.connect()
        Users.update({Users.TIMES: _times}).where(Users.CHATID == chat_id).execute()
    except:
        db.close()
        logger.exception(traceback.format_exc())
    else:
        db.commit()
        db.close()


def update_users_admin(username):
    logger = logging.getLogger("SmsHub_Bot.db_worker.update_users_admin")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        Users.update({Users.ADMIN: 1}).where(Users.USERNAME == username).execute()
    except:
        db.close()
        logger.exception(traceback.format_exc())
    else:
        db.commit()
        db.close()


def del_into_users(username):
    logger = logging.getLogger("SmsHub_Bot.db_worker.del_into_users")
    try:
        if not db.is_closed():
            db.close()
        db.connect()
        Users.delete().where(Users.USERNAME == username).execute()
    except:
        logger.exception(traceback.format_exc())
    else:
        db.commit()
        db.close()
