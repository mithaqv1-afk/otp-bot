async def extract_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    if not message_text:
        return
    
    # ابحث عن كلمة تدل على الكود متبوعة برقم من 4 إلى 6 منازل، أو التقط الرمز بدقة متناهية
    # هذا النمط يستخرج الأرقام التي تأتي بعد كلمات مفتاحية مثل code, رمز, التحقق، أو يتجنب السنوات
    match = re.search(r'(?:رمز|التحقق|code|verification|otp)[:\s]*(\d{4,6})', message_text, re.IGNORECASE)
    
    if not match:
        # إذا ما لكى كلمة مفتاحية، يبحث عن الأرقام بس يشيل منها السنوات الشائعة مثل 2024, 2025, 2026
        numbers = re.findall(r'\b\d{4,6}\b', message_text)
        valid_numbers = [n for n in numbers if not n.startswith(('202', '203'))]
        if valid_numbers:
            otp_code = valid_numbers[0]
        else:
            return
    else:
        otp_code = match.group(1)
        
    await update.message.reply_text(f"رمز التحقق هو: {otp_code}")
