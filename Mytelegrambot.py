import telebot
from config import keys, TOKEN
from extensions import ConvertionException, get_price

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text =  f"Дорообо, {message.chat.username} \n чтобы начать работу с ботом введите команду в формате: \n <имя валюты> <валюта перевода> <сумма> \n список доступных валют /values"
    bot.reply_to(message, text)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['values', ])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n' .join((text, key, ))
    bot.reply_to(message, text)

# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

# Обрабатывается все голосовые сообщения
@bot.message_handler(content_types=['voice', ])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'ага это ты так думаешь, друг')

@bot.message_handler(content_types=['photo', 'video'])
def send_welcome(message):
    bot.reply_to(message, f"Смешной мем, {message.chat.username}")

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        # исключение если слов больше трёх
        if len(values) != 3:
            raise ConvertionException(f'Слишком много параметров.')

        quote, base, amount = values
        total_base = get_price.convert(quote, base, amount)
        total_cost = get_price.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        # total_cost = int(amount) * int(total_base) # перенес в extensions
        text = f'Цена {amount} {quote} в {base} = {total_cost}'
        bot.send_message(message.chat.id, text)

bot.polling()