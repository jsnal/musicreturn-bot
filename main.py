#!/usr/bin/env python3

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl
import os

def return_music(update, context):
    url = update.message.text
    cid = update.message.chat_id

    try:
        result = ydl.extract_info(
            url,
            download=True
        )
        output = f"{os.path.splitext(ydl.prepare_filename(result))[0]}.mp3"
        update.message.reply_audio(open(output, "rb"))
    except Exception as e:
        print(e)
        update.message.reply_text(f"Errors were encountered for {url}")



def help_cmd(update, context):
    update.message.reply_text("Paste in a Youtube URL. Playlists are supported.")

def main():
    updater = Updater("136820376:AAFgZ66FHblXImb0m-QyHj5i4gZAQ-5sN_c", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(CommandHandler("help", help_cmd))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, return_music))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'cache/%(title)s.%(ext)s',
        'download_archive': 'downloaded_songs.txt',
        'restrictfilenames': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)

    # Start the telegram event loop
    main()