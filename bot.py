# _*_ coding: utf-8 _*_
# jetDm code
import dbWorker
from botSetting import bot
from telebot import types


# Ответ на приветствие
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую! Я бот-хранитель библиотеки!')


# Обработка команды КАТЕГОРИИ
@bot.message_handler(commands=['category'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    cat = dbWorker.get_category()
    for i in cat:
        btn_my_site = types.InlineKeyboardButton(text=cat[i], callback_data=cat[i])
        markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Выберите категорию", reply_markup=markup)


# Обработка callback вызова
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    category_list = dbWorker.get_category()
    for i in category_list:
        if call.data == category_list[i]:
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text=category_list[i])


# Обработка простого текста
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, dbWorker.get_category())
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'прикольно':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')


if __name__ == '__main__':
    bot.polling(none_stop=True)
