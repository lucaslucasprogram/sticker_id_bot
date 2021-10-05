import os
from constants import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler, CallbackQueryHandler


def handle_sticker_message(update, context):
    print("Dentro de bot handle_sticker_message")
    file_id = update.message.sticker.file_id
    file_unique_id = update.message.sticker.file_unique_id
    user_language = update.effective_user['language_code']
    if user_language == 'es':
        mensaje = f"Aqui tienes el <b>file_id</b>:" \
                  f"\n\n<code>{file_id}</code>" \
                  f"\n\nY por las dudas el file_unique_id:" \
                  f"\n\n<code>{file_unique_id}</code>"
        button = f"Probarlo!"

    else:
        mensaje = f"Here is the file_id" \
                  f"\n\n<code>{file_id}</code>" \
                  f"\n\nAnd just in case, there is the file_unique_id:" \
                  f"\n\n<code>{file_unique_id}</code>"
        button = f"Test it!"

    update.message.reply_text(
        reply_to_message_id=update.message.message_id,
        parse_mode="html",
        text=mensaje,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=button, callback_data='send_sticker')],
        ])
    )


def send_sticker(update, context):
    user_id = update.effective_message.chat_id
    print(update.effective_message)
    context.bot.send_sticker(
        chat_id=user_id,
        sticker=update.effective_message.reply_to_message.sticker.file_id
    )


def handle_start(update, context):
    print("Dentro de handle_start")
    user_first_name = update.effective_user['first_name']

    user_language = update.effective_user['language_code']
    if user_language == 'es':
        mensaje = (f'Hola {user_first_name}! para usarme, solo tienes que enviarme un sticker y yo te voy a devolver '
                   'el <i>file_id</i> para que puedas usar ese sticker en tu bot.'
                   '\nTambién voy a devolverte el file_unique_id <b>por las dudas</b>')
    else:
        mensaje = (f"Hi {user_first_name}! To use me, you just have to send me a sticker and I will return the "
                   f"<i> file_id </i> so you can use that sticker in your bot."
                   f"\nI'll also give you the file_unique_id <b> just in case </b>")

    update.message.reply_text(
        text=mensaje,
        parse_mode="html"
    )


def handle_donaciones(update, context):
    print("Dentro de donaciones")
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']
    if user_language == 'es':
        mensaje = (f"{user_first_name}! Si el bot te fue de utilidad y te ahorro tiempo, considera hacer una "
                   f"donación al desarrollador."
                   f"\nPuedes hacerlo desde ko-fi (botón aquí abajo)"
                   f"\nó enviar un mail: stickers-id-dev@telegmail.com")
        button = f"Comprale un Ko-Fi ☕"
    else:
        mensaje = (f"{user_first_name}! If the bot was useful and saved you time, consider making a donation "
                   f"to the developer."
                   f"\nYou can do it from ko-fi (button below)"
                   f"\nor contact him by mail: stickers-id-dev@telegmail.com")
        button = f"Buy a Ko-Fi ☕"

    update.message.reply_text(
        text=mensaje,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=button, url='https://ko-fi.com/lucasdeveloper')],
        ])
    )


def handle_message(update, context):
    print("Dentro de handle_messages")
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']
    text = update.message.text.lower().strip()
    if text in HOLA_MSGS:
        if user_language == 'es':
            hola_response = (f"Hola {user_first_name}!")
        else:
            hola_response = (f"Hi {user_first_name}!")

        update.message.reply_text(
            text=hola_response,
            parse_mode="html"
        )
    else:
        pass


def handle_ver_codigo(update, context):
    print("Dentro de handle_messages")
    user_first_name = update.effective_user['first_name']
    user_language = update.effective_user['language_code']
    if user_language == 'es':
        response = (f"Hola {user_first_name}! Puedes ver el codigo en GitHub usando el botón de abajo!"
                    f"<i>De paso seguime ;)</i>")
        button = f"Ver el codigo en GitHub"
    else:
        response = (f"Hi {user_first_name}! You can see the code on GitHub using the button below!"
                    f"\n<i>By the way, follow me!</i>")
        button = f"See the code on GitHub"

    update.message.reply_text(
        text=response,
        parse_mode="html",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=button, url='https://github.com/lucaslucasprogram/sticker_id_bot')],
        ])
    )


if __name__ == '__main__':
    updater = Updater(token=os.environ['TOKEN'], use_context=True)
    dp = updater.dispatcher
    dp.add_handler(
        CommandHandler('start', handle_start)
    )
    dp.add_handler(MessageHandler(Filters.sticker, handle_sticker_message))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(
        CommandHandler('ver_codigo', handle_ver_codigo)
    )
    dp.add_handler(
        CommandHandler('donaciones', handle_donaciones)
    )
    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern='send_sticker', callback=send_sticker)
        ],
        states={},
        fallbacks=[]
    ))
    updater.start_polling()
    print('Bot esta más vivo que vivin')
    updater.idle()
