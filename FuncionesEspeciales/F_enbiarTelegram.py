from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import asyncio
from telegram import Bot

texto = ""

TOKEN = "8683935378:AAFJz1b281ZuHL4KzP_fptfIWzVJYWzqDd0"
CHAT_ID = "-1003938828142"

async def mensajito():
    # print("se ejecuta esto")
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=f"{texto}")
    print("Se embio")


def Telegram_mensaje(tex):
    # print("llega")
    global texto
    texto = tex
    asyncio.run(mensajito())
    # print("termina")
