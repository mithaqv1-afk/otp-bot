import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")

async def extract_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    if not message_text:
        return
    match = re.search(r'\b\d{4,6}\b', message_text)
    if match:
        otp_code = match.group(0)
        await update.message.reply_text(f"{otp_code}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), extract_otp))
    app.run_polling()

if __name__ == '__main__':
    main()
