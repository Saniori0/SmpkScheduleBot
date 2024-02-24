import json

import telebot

from config import redis, TELEGRAM_BOT_TOKEN
from modules import parser

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

redis.delete("groups")


def extractArgs(arg) -> list:
    return arg.split()[1:]

@bot.message_handler(commands=['groups'])
def commandGroups(message):

    groups = parser.getGroups()

    bot.send_message(message.chat.id, """✌️ Привет! Это бот для просмотра расписания СМПК. Выберите группу:""")

@bot.message_handler(commands=['group'])
def commandGroup(message):

    groupName = " ".join(extractArgs(message.text))
    group = parser.getGroup(groupName)

    bot.send_message(message.chat.id, f"""Группа {groupName}: {json.dumps(group)}""")

bot.infinity_polling()
