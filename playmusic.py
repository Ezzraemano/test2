import os
import telegram
import urllib.request
from pydub import AudioSegment
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from youtube_dl import YoutubeDL

TOKEN = 'masukkan_token_bot_anda_disini'
bot = telegram.Bot(token=TOKEN)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Halo! Silakan kirim perintah /play <link musik YouTube> untuk memutar musik pada obrolan suara.")

def play_music(update, context):
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    music_url = context.args[0]

    # Unduh thumbnail video dari link YouTube
    ydl_opts = {'outtmpl': 'thumbnail.jpg'}
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(music_url, download=False)
        thumbnail_url = info_dict['thumbnail']
        urllib.request.urlretrieve(thumbnail_url, 'thumbnail.jpg')

    # Unduh file musik dari link YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([music_url])

    # Konversi file musik ke format obrolan suara
    sound = AudioSegment.from_file('
