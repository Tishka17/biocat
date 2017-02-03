#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import configparser
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import wiki2txt

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

config = configparser.RawConfigParser()
config.read('config.cnf')
updater = Updater(token=config.get("bot", "TOKEN"))
dispatcher = updater.dispatcher


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def wiki_parse(args):
    if len(args):
        n = wiki2txt.CorrectWord(args)
        url = wiki2txt.RuWiki(n)
        s = wiki2txt.GetWiki(url)
        if not len(s):
            return u'Статья не найдена. Попробуйте поискать другую'
        txt = wiki2txt.Wiki2Text(s)
        if len(txt):
            return txt
        else:
            return u'Статья пустая. Попробуйте почитать другую.'
    else:
        return u'Укажите, пожалуйста, название статьи после команды'


def wiki(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text=wiki_parse(" ".join(args))[:340])


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('wiki', wiki, pass_args=True))
dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
