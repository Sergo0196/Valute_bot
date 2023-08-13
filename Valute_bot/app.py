import telebot
import traceback
from extensions import APIException, Convert
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
        text = "Приветствуем Вас, меня зовут Сергей,\n я Вам расскажу о стоимости валют. \n Для получения справочной информации \
воспользуйтесь командой /help \n Для получения информации о доступных валютах воспользуйтесь командой: /values"
        bot.reply_to(message, text)

@bot.message_handler(commands=['help', ])
def help(message:telebot.types.Message):
        text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты, цену которой он хочет узнать> \n <имя валюты, \
в которой надо узнать цену первой валюты> \n<количество первой валюты>'
        bot.reply_to(message, text)

@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
        text = 'Доступные валюты: '
        for key in keys.keys():
                text = '\n'.join((text, key))
        bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException("Проверьте правильность заполнения инструкции")


        answer = Convert.get_price(*values)

    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n {e}")

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка:\n {e}')

    else:
        bot.reply_to(message, answer)





bot.polling()