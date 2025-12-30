# ================== KEEP ALIVE ==================
from flask import Flask
from threading import Thread

web = Flask(__name__)

@web.route("/")
def home():
    return "Bot is alive!"

def run_web():
    web.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run_web).start()

# ================== BOT ==================
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# 🔴 ضع توكن البوت هنا
TOKEN = "8343139529:AAEAb4xFox4ETK1hpQMdonsG0PfQQrh0btY"

# 🔗 رابط GIF أو MP4 من أي موقع (يمكنك تغييره بأي وقت)
MEDIA_URL = "https://imgur.com/a/ukFRrD1"  # ضع الرابط المباشر هنا

# الأزرار للصيغ
FORMATS = [["TXT 📄", "PY 🐍"], ["MD 📝", "JSON 🧩"]]
FORMAT_MAP = {
    "TXT 📄": "txt",
    "PY 🐍": "py",
    "MD 📝": "md",
    "JSON 🧩": "json"
}

# تخزين الحالة لكل مستخدم
user_state = {}

# البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state.clear()
    keyboard = ReplyKeyboardMarkup(FORMATS, resize_keyboard=True)
    await update.message.reply_text(
        "🤖 أهلاً بك في بوت Text-to-File!\n\n"
        "اختر صيغة الملف أولاً 👇",
        reply_markup=keyboard
    )

# التعامل مع الرسائل
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # اختيار الصيغة
    if user_id not in user_state:
        if text in FORMAT_MAP:
            user_state[user_id] = {"ext": FORMAT_MAP[text]}
            await update.message.reply_text(
                "✏️ اكتب اسم الملف (بدون امتداد):",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text("❌ اختر الصيغة من الأزرار")
        return

    # اختيار اسم الملف
    if "name" not in user_state[user_id]:
        user_state[user_id]["name"] = text
        await update.message.reply_text("📝 الآن أرسل النص الذي تريد تحويله إلى ملف:")
        return

    # كتابة المحتوى
    ext = user_state[user_id]["ext"]
    name = user_state[user_id]["name"]
    content = text

    filename = f"{name}.{ext}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    # إرسال الملف
    await update.message.reply_document(open(filename, "rb"))

    # إرسال GIF أو MP4 حسب الرابط
    if MEDIA_URL.endswith(".mp4"):
        await update.message.reply_video(MEDIA_URL)
    else:
        await update.message.reply_animation(MEDIA_URL)

    # حذف الملف من السيرفر
    os.remove(filename)
    user_state.pop(user_id)

    # إعادة الأزرار
    keyboard = ReplyKeyboardMarkup(FORMATS, resize_keyboard=True)
    await update.message.reply_text(
        "✅ تم إنشاء الملف! اختر صيغة ملف جديدة 👇",
        reply_markup=keyboard
    )

# ================== RUN ==================
keep_alive()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

app.run_polling()