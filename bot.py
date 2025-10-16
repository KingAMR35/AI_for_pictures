import telebot
from dotenv import load_dotenv
import os
from api_service import FusionBrainAPI


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет {message.chat.first_name}! Напиши мне какую-нибудь фразу и я сгенерирую её.')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    bot.send_message(message.chat.id, "Подождите, идёт загрузка🔄")

    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', os.getenv('FB_API_KEY'), os.getenv('FB_SECRET_KEY'))
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)
    
    api.save_image(files[0], 'result.png')
    with open('result.png', 'rb') as file:
        bot.send_photo(message.chat.id, file)


bot.infinity_polling()
