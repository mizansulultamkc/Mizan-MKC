# -*- coding: utf-8 -*-

import os

# Remove proxy env vars that block Telegram connections
for _var in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
    os.environ.pop(_var, None)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.request import HTTPXRequest

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN secret is not set. Please add it in the Secrets tab.")

leaders = {
    "pastor1": {
        "name": "ደረጄ ተስፋዬ",
        "role": "የመሪዎች ሰብሳቢ",
        "phone": "+251911132547",
        "email": "dereje@example.com"
    },
    "pastor2": {
        "name": "በሰዓቱ ባንክስራ",
        "role": "ምክትል ሰብሳቢ",
        "phone": "0910995220",
        "email": ""
    },
    "pastor3": {
        "name": "መጋቢ ሰለሞን ለማ",
        "role": "መጋቢ",
        "phone": "0912476884",
        "email": ""
    },
    "pastor4": {
        "name": "የኔውልኝ ዋሴ",
        "role": "የሒሳብ ሹም",
        "phone": "0913226225",
        "email": ""
    },
    "pastor5": {
        "name": "ማሜ ዴሬሳ",
        "role": "ገንዘብ ያዥ",
        "phone": "0913218145",
        "email": ""
    },
    "pastor6": {
        "name": "ፈይሳ ደበሎ",
        "role": "ተጠባባቂ አባል",
        "phone": "0921181803",
        "email": ""
    }
}


def main_menu():
    keyboard = [
        [InlineKeyboardButton("ደረጄ ተስፋዬ", callback_data="pastor1")],
        [InlineKeyboardButton("በሰዓቱ ባንክስራ", callback_data="pastor2")],
        [InlineKeyboardButton("መጋቢ ሰለሞን ለማ", callback_data="pastor3")],
        [InlineKeyboardButton("የኔውልኝ ዋሴ", callback_data="pastor4")],
        [InlineKeyboardButton("ማሜ ዴሬሳ", callback_data="pastor5")],
        [InlineKeyboardButton("ፈይሳ ደበሎ", callback_data="pastor6")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "የቤተክርስቲያን መሪዎች\n\nአንድ መሪ ይምረጡ:",
        reply_markup=main_menu()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    leader = leaders[query.data]

    text = f"""
 ስም: {leader['name']}

 ሀላፊነት: {leader['role']}

 ስልክ: {leader['phone']}

 ኢሜይል: {leader['email']}
"""

    try:
        await query.message.reply_photo(
            photo=open(f"{query.data}.jpg", "rb"),
            caption=text
        )
    except FileNotFoundError:
        await query.message.reply_text(text)


request = HTTPXRequest(proxy=None)
app = ApplicationBuilder().token(TOKEN).request(request).get_updates_request(request).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot is running...")
app.run_polling()
