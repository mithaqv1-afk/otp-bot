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
    
    # استخراج الأرقام من 4 إلى 6 منازل واستبعاد السنوات
    numbers = re.findall(r'\b\d{4,6}\b', message_text)
    valid_numbers = [n for n in numbers if not n.startswith(('2026'))]
    
    if valid_numbers:
        otp_code = valid_numbers[0]
        # إرسال الكود وحده صافي بدون أي كلام إضافي
        await update.message.reply_text(otp_code)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, extract_otp))
    
    app.run_polling()

if __name__ == '__main__':
    main()
