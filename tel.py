import telebot
from telebot import types
import json
import os
import main
if not os.path.exists(os.path.join(os.getcwd(), 'kurs.json')):
    with open(os.path.join(os.getcwd(), 'kurs.json.json'),'w'):
        main.putdatetofilekurs(main.kurs)
if not os.path.exists(os.path.join(os.getcwd(), 'users.json')):
    with open(os.path.join(os.getcwd(), 'users.json'),'w'):
        pass
user_file = os.path.join(os.getcwd(), 'users.json')
curs_file = os.path.join(os.getcwd(), 'kurs.json')
m={}
bot=telebot.TeleBot('5343945393:AAHa9fg3dyQBC624pPjQppRUiSPpNXgj1js')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kurs_start = types.KeyboardButton('Відслідковувати зміну курсу')
    kurs_now = types.KeyboardButton('Теперешній курс')
    markup.add(kurs_start,kurs_now)
    bot.send_message(message.chat.id,'Вітаю вас!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_activate(message):
    if message.chat.type == 'private':
        if message.text == 'Відслідковувати зміну курсу':
            m[message.chat.id]=True
            with open(user_file, 'w') as f:
                json.dump(m, f)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kurs_stop = types.KeyboardButton('Перестати відслідковувати зміну курсу')
            kurs_now = types.KeyboardButton('Теперешній курс')
            markup.add(kurs_stop, kurs_now)
            bot.send_message(message.chat.id, 'Тепер ви слідкуєте за курсом', reply_markup=markup)
        elif message.text == 'Перестати відслідковувати зміну курсу':
            m[message.chat.id]=False
            with open(user_file, 'w') as f:
                json.dump(m, f)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kurs_start = types.KeyboardButton('Відслідковувати зміну курсу')
            kurs_now = types.KeyboardButton('Теперешній курс')
            markup.add(kurs_start, kurs_now)
            bot.send_message(message.chat.id, 'Ви перестали слідкувати за курсом', reply_markup=markup)
        elif message.text == 'Теперешній курс':
            if main.main()==True:
                bot.send_message(message.chat.id, main.send_to_tel, parse_mode='html')
            else:
                with open(curs_file) as f:
                    kurs=json.load(f)
                vivod=[]
                send_to_tel=''
                for bank in kurs:
                    for val in kurs[bank]:
                        for sell_buy in kurs[bank][val]:
                            vivod.append(str(kurs[bank][val][sell_buy]))
                    send_to_tel += main.message(vivod, main.kirilitsia(bank))
                    vivod = []
                bot.send_message(message.chat.id, send_to_tel,parse_mode='html')
bot.polling(none_stop=True)
