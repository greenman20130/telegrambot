import telebot
from telebot import types
from tgtoken import TOKEN, keys
import requests
import json

counter = 0
btn_generator = [key for key in keys]
page = 0

print(len(btn_generator))
    
bot = telebot.TeleBot(TOKEN)
help_txt = """Этот бот отправяет тебе актуальные валюты"""
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    global page
    bot.send_message(message.chat.id, f"""Привет, {message.chat.username}!\n{help_txt}""", reply_markup=key_board(page))


@bot.message_handler(content_types=["text"])
def txt_handle(message):
    global counter, currency_value, page
    key_board(page)
    if counter == 1:
        try:
            message.text = float(message.text)
        except:
            bot.send_message(message.chat.id, f'Введено не верное количество', reply_markup=key_board(page))
        else:
            counter +=1
            currency_value = message.text
            bot.send_message(message.chat.id, f'Введите валюту в которую нужно перевести', reply_markup=key_board(page))

        
        
        
    elif message.text in keys and counter == 0:
        global base
        counter += 1
        base = message.text
        bot.send_message(message.chat.id, f"Введи колличество {base}", reply_markup=key_board(page))
        
    
    elif message.text in keys and counter == 2:
        counter += 1
        quote = message.text
        take_value = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}")
        text = json.loads(take_value.content)[quote]
        bot.send_message(message.chat.id, f'{currency_value} {base} в {quote} = {float(text*currency_value)}', reply_markup=key_board(page))
        counter = 0
    
    elif message.text == "Следующая страница":
        keyboard = types.ReplyKeyboardRemove()
        page += 5
        print(page)
        bot.reply_to(message, "Оки", reply_markup=keyboard)
        bot.reply_to(message, "Готово", reply_markup=key_board(page))
    
    elif message.text == "Предыдущая страница":
        keyboard = types.ReplyKeyboardRemove()
        page -= 5
        bot.reply_to(message, "Оки", reply_markup=keyboard)
        bot.reply_to(message, "Готово", reply_markup=key_board(page))
    
    
    else:
        bot.send_message(message.chat.id, f"Прости, но я тебя не понимаю", reply_markup=key_board(page))


def key_board(page):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_fake_next_p = types.KeyboardButton("Следующая страница недоступна")
    btn_next_p = types.KeyboardButton("Следующая страница")
    btn_v1 = types.KeyboardButton(btn_generator[page])
    btn_v2 = types.KeyboardButton(btn_generator[page+1])
    btn_v3 = types.KeyboardButton(btn_generator[page+2])
    btn_v4 = types.KeyboardButton(btn_generator[page+3])
    btn_v5 = types.KeyboardButton(btn_generator[page+4])
    btn_prev_p = types.KeyboardButton("Предыдущая страница")
    btn_fake_prev_p =types.KeyboardButton("Предыдущая страница недоступна")
    return markup.add(btn_v1, btn_v2, btn_v3, btn_v4, btn_v5, btn_next_p if page <=40 else btn_fake_next_p, btn_prev_p if page >= 5 else btn_fake_prev_p)
    

bot.polling(none_stop=True)
    
