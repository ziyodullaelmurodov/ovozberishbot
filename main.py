from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Ovozlar saqlash uchun lug'at
votes = {}
user_votes = {}  # Har bir foydalanuvchi uchun ovoz bergan holatni saqlash

# Kanal tekshiruvi uchun
channel_username = "@tatusfyoshlarittifoqi"  # Bu yerda o'zingizning kanal ismingizni kiriting

async def start(update: Update, context):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Kanalga a'zo bo'lish", url=f"https://t.me/tatusfyoshlarittifoqi")],
        [InlineKeyboardButton("Obuna bo'ldim✔️", callback_data='check_subscription')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Assalomu alaykum {user.first_name}! Kanalga a'zo bo'lishingizni so'rayman!",
        reply_markup=reply_markup
    )

async def check_subscription_callback(update: Update, context):
    query = update.callback_query
    user_id = query.from_user.id

    chat_member = await context.bot.get_chat_member(chat_id=channel_username, user_id=user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        await query.answer("Obuna tekshirilmoqda...", show_alert=False)
        await query.message.reply_text("Kanalga obuna bo'lganingizdan xursandman!😊")
        keyboard = [[InlineKeyboardButton("📢 Ovoz berish 📢", callback_data='vote')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Ovoz berish tugmasini tanlang:⬇️", reply_markup=reply_markup)
    else:
        await query.answer("Iltimos, avval kanalga obuna bo'ling!", show_alert=True)

async def vote(update: Update, context):
    query = update.callback_query
    await query.answer()

    # Nomzodlar ro'yxati va ovozlar
    candidates = ["Kaxramonov Xudoyberdi Shuxrat o‘g‘li", "Marupov Sharifjon Laziz o‘g‘li", "Shakarov Sarvar Quvondiq o‘g‘li", "Sherqulova Rayxona Zarif qizi", "Qilichboyev Asadbek Yolqin o`g`li", "Safarov Asilbek Jahongir o‘g‘li", "Ismatillayev Azizjon Raxmatulloyevich", "Normo‘minova Shahnoza Abdulla qizi", "Rajabova Hulkaroy Zoir qizi", "Pak Dina Konstantinovna", "Baxriddinova Durdona Fazliddinovna", "Ibodov Ilhom Salim o‘g‘li", "Butayev Zavqidin Shuxrat o‘g‘li", "Alxamjonova Muxayyo Alisherovna", "Jo‘raboyeva Shaxlo Farxod qizi", "Volkov Mixail Pavlovich", "Otaqulov Faxriddin Asliddin o‘g‘li", "Ablonberdiyev Javohir Zohid o‘g‘li", "Keldiyorov Quvonchbek Odiljon o‘g‘li", "Axtamov Safar Solejonovich ", "Norpulatov Asilbek Zokirjon o‘g‘li", "Abduraxmonov Og‘abek Juma o‘g‘li", "Xakimov Ulug‘bekjon Otabek o‘g‘li", "Majidov Husan Abdijalil o‘g‘li", "Ashurov Shohruz Zohir o‘g‘li", "Ibragimov Habib Abduvosi o‘g‘li", "Abdurashidov Fayoz Zafar o‘g‘li", "Qilichova Orzigul Yorqin qizi", "Adashov Umar Soleyevich", "Xabibov Dilmurod Lutfilloyevich", "Murtozayev Sanjarbek Mirzohid o‘g‘li", "Akmalova Diyora Ikromovna", "Boltayev Otabek Husan o‘g‘li", "Erkinov G‘olibjon Xusniddin o‘g‘li", "Sharofiddinov Husan Sirojiddin o‘g‘li"]

    # Klaviatura yaratishda ovozlar sonini qo'shamiz
    keyboard = [
        [InlineKeyboardButton(f"{name} ({votes.get(name, 0)} ta ovoz)", callback_data=f"vote_{name}")]
        for name in candidates
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("Ovoz bering!", reply_markup=reply_markup)

async def process_vote(update: Update, context):
    query = update.callback_query
    user_id = query.from_user.id
    candidate = query.data.split('_')[1]

    # Agar foydalanuvchi ovoz bergan bo'lsa, qayta ruxsat bermaymiz
    if user_id in user_votes:
        await query.answer("Siz allaqachon ovoz bergansiz!", show_alert=True)
        return

    # Foydalanuvchining ovozini qayd qilish
    user_votes[user_id] = candidate
    votes[candidate] = votes.get(candidate, 0) + 1

    await query.answer("Ovozingiz qabul qilindi!✔️", show_alert=False)

    # Nomzodlar ro'yxatini yangilash
    candidates = ["Kaxramonov Xudoyberdi Shuxrat o‘g‘li", "Marupov Sharifjon Laziz o‘g‘li", "Shakarov Sarvar Quvondiq o‘g‘li", "Sherqulova Rayxona Zarif qizi", "Qilichboyev Asadbek Yolqin o`g`li", "Safarov Asilbek Jahongir o‘g‘li", "Ismatillayev Azizjon Raxmatulloyevich", "Normo‘minova Shahnoza Abdulla qizi", "Rajabova Hulkaroy Zoir qizi", "Pak Dina Konstantinovna", "Baxriddinova Durdona Fazliddinovna", "Ibodov Ilhom Salim o‘g‘li", "Butayev Zavqidin Shuxrat o‘g‘li", "Alxamjonova Muxayyo Alisherovna", "Jo‘raboyeva Shaxlo Farxod qizi", "Volkov Mixail Pavlovich", "Otaqulov Faxriddin Asliddin o‘g‘li", "Ablonberdiyev Javohir Zohid o‘g‘li", "Keldiyorov Quvonchbek Odiljon o‘g‘li", "Axtamov Safar Solejonovich ", "Norpulatov Asilbek Zokirjon o‘g‘li", "Abduraxmonov Og‘abek Juma o‘g‘li", "Xakimov Ulug‘bekjon Otabek o‘g‘li", "Majidov Husan Abdijalil o‘g‘li", "Ashurov Shohruz Zohir o‘g‘li", "Ibragimov Habib Abduvosi o‘g‘li", "Abdurashidov Fayoz Zafar o‘g‘li", "Qilichova Orzigul Yorqin qizi", "Adashov Umar Soleyevich", "Xabibov Dilmurod Lutfilloyevich", "Murtozayev Sanjarbek Mirzohid o‘g‘li", "Akmalova Diyora Ikromovna", "Boltayev Otabek Husan o‘g‘li", "Erkinov G‘olibjon Xusniddin o‘g‘li", "Sharofiddinov Husan Sirojiddin o‘g‘li"]
    keyboard = [
        [InlineKeyboardButton(f"{name} ({votes.get(name, 0)} ta ovoz)", callback_data=f"vote_{name}")]
        for name in candidates
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Ovoz bering!", reply_markup=reply_markup)

async def show_results(update: Update, context):
    if not votes:
        await update.message.reply_text("Hozircha ovoz berilmagan.")
        return

    results = "\n".join([f"{candidate}: {count} ta ovoz" for candidate, count in votes.items()])
    await update.message.reply_text(f"Ovoz berish natijalari:\n{results}")

def main():
    token = "7945191211:AAGfV1V3irGLSfvvkHs42OrARkP3In_rwSc"  # Bu yerga bot tokeningizni kiriting
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subscription_callback, pattern='^check_subscription$'))
    app.add_handler(CallbackQueryHandler(vote, pattern='^vote$'))
    app.add_handler(CallbackQueryHandler(process_vote, pattern='^vote_'))
    app.add_handler(CommandHandler("natija", show_results))

    print("Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
