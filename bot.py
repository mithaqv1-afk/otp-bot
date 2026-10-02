import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! البوت يعمل بنجاح وجاهز لاستخراج رموز التحقق.")

async def extract_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    if not message_text:
        return
    
    # استخراج كل الأرقام التي تتكون من 4 إلى 6 منازل
    numbers = re.findall(r'\b\d{4,6}\b', message_text)
    
    # تصفية الأرقام لاستبعاد السنوات (التي تبدأ بـ 202 أو 203)
    valid_numbers = [n for n in numbers if not n.startswith(('202', '203'))]
    
    if valid_numbers:
        otp_code = valid_numbers[0]
        await update.message.reply_text(f"رمز التحقق هو: {otp_code}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, extract_otp))
    
    app.run_polling()

if __name__ == '__main__':
    main()
