import time

from settings import TOKEN
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import requests
import json

url_getFile = "https://api.telegram.org/bot%s/getFile" % TOKEN

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Jestem obserawtorem WW3.")


def get_video(update: Update, context: CallbackContext):
    response = requests.request("POST", url_getFile, json={'file_id': update.message.video.file_id}, headers=headers)
    file_path = json.loads(response.text)['result']['file_path']
    response = requests.get('https://api.telegram.org/file/bot%s/%s' % (TOKEN, file_path))
    filename_data = time.strftime("%d_%m_%H:%M:%S", time.gmtime())
    context.bot.send_message(chat_id=update.effective_chat.id, text='Dodane video: ' + filename_data)
    open('./movies/' + filename_data + '.mp4', 'wb').write(response.content)


def get_image(update: Update, context: CallbackContext):
    response = requests.request("POST", url_getFile, json={'file_id': update.message.photo[-1].file_id}, headers=headers)
    file_path = json.loads(response.text)['result']['file_path']
    response = requests.get('https://api.telegram.org/file/bot%s/%s' % (TOKEN, file_path))
    filename_data = time.strftime("%d_%m_%H:%M:%S", time.gmtime())
    open('./images/' + filename_data + '.jpg', 'wb').write(response.content)


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# 1
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
# photo
photo_handler = MessageHandler(Filters.photo, get_image)
dispatcher.add_handler(photo_handler)
# video
video_handler = MessageHandler(Filters.video, get_video)
dispatcher.add_handler(video_handler)
updater.start_polling()
