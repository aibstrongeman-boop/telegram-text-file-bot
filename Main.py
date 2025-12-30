from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os, random, string

TOKEN = os.environ.get("BOT_TOKEN")

ALLOWED_EXT = ["txt", "py", "md", "json"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Text to File Bot\n\n"
        "/file <ext> <name> <text>\n"
        "/password <length>\n"
        "/otp\n\n"
        "مثال:\n"
        "/file txt note هذا نص\n"
        "/file py test print('Hello')"
    )

async def create_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("❌ الصيغة: /file <ext> <name> <text>")
        return

    ext, name = context.args[0].lower(), context.args[1]
    content = " ".join(context.args[2:])

    if ext not in ALLOWED_EXT:
        await update.message.reply_text("❌ صيغة غير مدعومة")
        return

    filename = f"{name}.{ext}"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    await update.message.reply_document(open(filename, "rb"))
    os.remove(filename)

async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    length = int(context.args[0]) if context.args else 12
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = ''.join(random.choice(chars) for _ in range(length))
    await update.message.reply_text(f"🔐 {pwd}")

async def otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🛡️ OTP: {random.randint(100000,999999)}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("file", create_file))
app.add_handler(CommandHandler("password", password))
app.add_handler(CommandHandler("otp", otp))

app.run_polling()
