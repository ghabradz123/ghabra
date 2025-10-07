import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Chat
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ===== إعدادات عامة =====
TOKEN = "8234553204:AAHt0_NotXPwMOgQsdOfUFRsB4vbv8tgjmI"
logging.basicConfig(level=logging.INFO)

# ===== بيانات المحتوى =====

QURAN_EXCERPTS = [
    ("الفاتحة", "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ"),
    ("الإخلاص", "قُلْ هُوَ اللَّهُ أَحَدٌ"),
    ("الكوثر", "إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ"),
    ("العصر", "وَالْعَصْرِ إِنَّ الْإِنسَانَ لَفِي خُسْرٍ"),
    ("الرحمن", "فَبِأَيِّ آلَاءِ رَبِّكُمَا تُكَذِّبَانِ"),
    ("البقرة", "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ"),
    ("النور", "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ"),
    ("الحديد", "اعْلَمُوا أَنَّ اللَّهَ يُحْيِي الْأَرْضَ بَعْدَ مَوْتِهَا"),
    ("الأنعام", "وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ"),
    ("يوسف", "إِنَّهُ مَن يَتَّقِ وَيَصْبِرْ فَإِنَّ اللَّهَ لَا يُضِيعُ أَجْرَ الْمُحْسِنِينَ"),
    ("الزمر", "قُلْ يَا عِبَادِيَ الَّذِينَ أَسْرَفُوا عَلَى أَنفُسِهِمْ لَا تَقْنَطُوا مِن رَّحْمَةِ اللَّهِ"),
    ("الأحزاب", "إِنَّ اللَّهَ وَمَلَائِكَتَهُ يُصَلُّونَ عَلَى النَّبِيِّ"),
    ("التوبة", "إِنَّ اللَّهَ مَعَ الصَّابِرِينَ"),
    ("الحجر", "فَاصْفَحِ الصَّفْحَ الْجَمِيلَ"),
    ("المزمل", "وَرَتِّلِ الْقُرْآنَ تَرْتِيلًا"),
    ("العنكبوت", "إِنَّ اللَّهَ لَيُدَافِعُ عَنِ الَّذِينَ آمَنُوا"),
    ("الملك", "الَّذِي خَلَقَ الْمَوْتَ وَالْحَيَاةَ"),
    ("النبأ", "عَمَّ يَتَسَاءَلُونَ"),
    ("الضحى", "وَلَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَىٰ"),
    ("الشرح", "فَإِنَّ مَعَ الْعُسْرِ يُسْرًا"),
]

HADITHS = [
    "قال ﷺ: «إنما الأعمال بالنيات»",
    "قال ﷺ: «الدين النصيحة»",
    "قال ﷺ: «المسلم من سلم المسلمون من لسانه ويده»",
    "قال ﷺ: «من لا يَرحم لا يُرحم»",
    "قال ﷺ: «من حسن إسلام المرء تركه ما لا يعنيه»",
    "قال ﷺ: «تبسمك في وجه أخيك صدقة»",
    "قال ﷺ: «اتق الله حيثما كنت»",
    "قال ﷺ: «اقرؤوا القرآن فإنه يأتي شفيعًا لأصحابه»",
    "قال ﷺ: «الرفق لا يكون في شيء إلا زانه»",
    "قال ﷺ: «من سلك طريقًا يلتمس فيه علمًا سهّل الله له به طريقًا إلى الجنة»",
    "قال ﷺ: «من توضأ فأحسن الوضوء خرجت خطاياه من جسده»",
    "قال ﷺ: «المؤمن مرآة أخيه»",
    "قال ﷺ: «خيركم من تعلم القرآن وعلمه»",
    "قال ﷺ: «من قال لا إله إلا الله دخل الجنة»",
    "قال ﷺ: «من صام رمضان إيمانًا واحتسابًا غفر له ما تقدم من ذنبه»",
    "قال ﷺ: «الطهور شطر الإيمان»",
    "قال ﷺ: «إن الله جميل يحب الجمال»",
    "قال ﷺ: «الدعاء هو العبادة»",
    "قال ﷺ: «من كان يؤمن بالله واليوم الآخر فليقل خيرًا أو ليصمت»",
    "قال ﷺ: «أقرب ما يكون العبد من ربه وهو ساجد»",
]

DUAS = [
    "اللهم اجعل القرآن ربيع قلوبنا ونور صدورنا.",
    "اللهم اغفر لنا ذنوبنا وكفّر عنا سيئاتنا.",
    "اللهم ارزقنا حبك وحب من يحبك.",
    "اللهم اجعلنا من المقبولين في الدنيا والآخرة.",
    "اللهم إنا نسألك الجنة ونعوذ بك من النار.",
    "اللهم ارزقنا رزقًا طيبًا واسعًا مباركًا فيه.",
    "اللهم اشف مرضانا ومرضى المسلمين.",
    "اللهم اغفر لوالدينا وارحمهما كما ربيانا صغارًا.",
    "اللهم اجعلنا من الذاكرين الشاكرين.",
    "اللهم اجعلنا من الذين يستمعون القول فيتبعون أحسنه.",
    "اللهم بارك لنا في أعمارنا وأعمالنا.",
    "اللهم اجعلنا من أوليائك الصالحين.",
    "اللهم أصلح شباب المسلمين.",
    "اللهم فرّج همّ المهمومين.",
    "اللهم اجعل آخر كلامنا من الدنيا لا إله إلا الله.",
    "اللهم وفقنا لما تحب وترضى.",
    "اللهم اجعلنا سببًا في هداية الناس.",
    "اللهم اكتب لنا حسن الخاتمة.",
    "اللهم اجعلنا من الصالحين المصلحين.",
    "اللهم ارزقنا توبة نصوحًا قبل الموت.",
]

AZKAR = [
    "أستغفر الله العظيم وأتوب إليه.",
    "سبحان الله، والحمد لله، ولا إله إلا الله، والله أكبر.",
    "اللهم صل وسلم على نبينا محمد.",
    "لا حول ولا قوة إلا بالله.",
    "سبحان الله وبحمده، سبحان الله العظيم.",
    "استغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه.",
    "رضيت بالله ربًا، وبالإسلام دينًا، وبمحمد ﷺ نبيًا.",
    "اللهم اجعل يومي هذا خيرًا من أمسي.",
    "اللهم أعني على ذكرك وشكرك وحسن عبادتك.",
    "اللهم إني ظلمت نفسي فاغفر لي.",
    "اللهم اجعلنا من الشاكرين.",
    "اللهم إنا نعوذ بك من الهم والحزن.",
    "اللهم إنا نعوذ بك من الكسل والجبن.",
    "اللهم إنا نعوذ بك من قلب لا يخشع.",
    "اللهم إنا نعوذ بك من علم لا ينفع.",
    "اللهم ذكرنا ما نسينا وعلمنا ما جهلنا.",
    "اللهم اجعلنا من الذاكرين الله كثيرًا والذاكرات.",
    "اللهم اجعلنا من عبادك الصالحين.",
    "اللهم وفقنا لما تحب وترضى.",
    "اللهم اجعل القرآن العظيم لنا إمامًا ونورًا.",
]

# ======= الأزرار =======
def main_menu():
    buttons = [
        [InlineKeyboardButton("📖 آيات من القرآن", callback_data="quran")],
        [InlineKeyboardButton("🕋 أحاديث نبوية", callback_data="hadith")],
        [InlineKeyboardButton("🤲 أدعية", callback_data="dua")],
        [InlineKeyboardButton("🔢 مسبحة", callback_data="tasbih")],
    ]
    return InlineKeyboardMarkup(buttons)

def back_menu():
    return InlineKeyboardMarkup([[InlineKeyboardButton("↩️ الرجوع للقائمة", callback_data="back")]])

def tasbih_keyboard(count: int):
    kb = [
        [
            InlineKeyboardButton(f"تسبيح ✅ ({count})", callback_data="tasbih_inc"),
            InlineKeyboardButton("♻️ إعادة ضبط", callback_data="tasbih_reset"),
        ],
        [InlineKeyboardButton("↩️ الرجوع", callback_data="back")],
    ]
    return InlineKeyboardMarkup(kb)

# ======= عند بدء البوت =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🌿 *مرحبًا بك في البوت الإسلامي!*\n\n"
        "📖 آيات، 🕋 أحاديث، 🤲 أدعية، 🔢 مسبحة\n"
        "كما أرسل الأذكار تلقائيًا في المجموعات 🌙"
    )
    await update.message.reply_text(text, reply_markup=main_menu(), parse_mode="Markdown")

# ======= التعامل مع الأزرار =======
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "quran":
        s, v = random.choice(QURAN_EXCERPTS)
        await query.edit_message_text(f"📖 *{s}*\n\n{v}", parse_mode="Markdown", reply_markup=back_menu())
    elif data == "hadith":
        h = random.choice(HADITHS)
        await query.edit_message_text(f"🕋 حديث:\n\n{h}", reply_markup=back_menu())
    elif data == "dua":
        d = random.choice(DUAS)
        await query.edit_message_text(f"🤲 دعاء:\n\n{d}", reply_markup=back_menu())
    elif data == "tasbih":
        context.user_data["tasbih_count"] = 0
        await query.edit_message_text("🔢 مسبحة تفاعلية", reply_markup=tasbih_keyboard(0))
    elif data == "tasbih_inc":
        count = context.user_data.get("tasbih_count", 0) + 1
        context.user_data["tasbih_count"] = count
        await query.edit_message_reply_markup(reply_markup=tasbih_keyboard(count))
    elif data == "tasbih_reset":
        context.user_data["tasbih_count"] = 0
        await query.edit_message_reply_markup(reply_markup=tasbih_keyboard(0))
    elif data == "back":
        await query.edit_message_text("🌿 الرجوع إلى القائمة:", reply_markup=main_menu())

# ======= عند الإضافة إلى مجموعة =======
async def added_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.message.chat
    if chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        await context.bot.send_message(
            chat_id=chat.id,
            text="🌙 السلام عليكم ورحمة الله وبركاته!\n"
                 "شكراً لإضافة البوت 🤍\n"
                 "سأرسل هنا أدعية وأذكارًا تلقائيًا كل ساعة بإذن الله.",
        )
        context.job_queue.run_repeating(send_auto_zekr, interval=3600, first=10, chat_id=chat.id)

# ======= وظيفة الإرسال التلقائي =======
async def send_auto_zekr(context: ContextTypes.DEFAULT_TYPE):
    zekr = random.choice(DUAS + AZKAR)
    await context.bot.send_message(chat_id=context.job.chat_id, text=f"🕌 {zekr}")

# ======= التشغيل =======
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, added_to_group))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()