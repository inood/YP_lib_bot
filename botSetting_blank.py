# _*_ coding: utf-8 _*_
#jetDm code
import telebot
from telebot import apihelper


bot = telebot.TeleBot('')
apihelper.proxy = {'https': 'socks5://133002375:cKgkWx8p@orbtl.s5.opennetwork.cc:999'}
database = 'db/Lib.db'