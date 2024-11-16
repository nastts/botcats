import telebot
from model import get_class

bot = telebot.TeleBot('token')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """привет!!!""")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id, "нет картинки")
    
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]

    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    result = get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=file_name)
    bot.send_message(message.chat.id, result)

bot.polling()
