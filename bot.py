import os
import re
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CopyTextButton,
)
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TOKEN = os.environ.get("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "أهلاً بك! البوت يعمل بنجاح وجاهز لاستخراج رموز التحقق."
    )


async def extract_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message:
        return

    # قراءة النص أو الـ Caption
    message_text = message.text or message.caption

    if not message_text:
        return

    # استخراج الأرقام الإنجليزية والعربية
    numbers = re.findall(
        r"(?<![\d٠-٩])[\d٠-٩]{4,6}(?![\d٠-٩])",
        message_text
    )

    if not numbers:
        return

    for number in numbers:

        # تحويل الأرقام العربية إلى إنجليزية
        arabic_to_english = str.maketrans(
            "٠١٢٣٤٥٦٧٨٩",
            "0123456789"
        )

        otp_code = number.translate(arabic_to_english)

        # تجاهل سنة 2026
        if otp_code == "2026":
            continue

        # إنشاء زر النسخ
        copy_button = InlineKeyboardButton(
            text="📋 نسخ الرمز",
            copy_text=CopyTextButton(
                text=otp_code
            )
        )

        keyboard = InlineKeyboardMarkup([
            [copy_button]
        ])

        # إرسال الرمز مع زر النسخ
        await message.chat.send_message(
            text=otp_code,
            reply_markup=keyboard
        )

        # نأخذ أول رمز فقط
        break


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(
        "حدث خطأ أثناء تشغيل البوت:",
        exc_info=context.error
    )


def main():

    if not TOKEN:
        raise ValueError(
            "لم يتم العثور على TOKEN في متغيرات البيئة."
        )

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            extract_otp
        )
    )

    app.add_error_handler(error_handler)

    print("Bot is running...")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
