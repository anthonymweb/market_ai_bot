from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from users import set_user, get_user, toggle_alert
from engine import analyze
from config import TOKEN
import os

# ----------------- BOT COMMANDS -----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Advanced Market Bot\n\n"
        "Commands:\n"
        "/setup BTCUSDT low\n"
        "/signal\n"
        "/alerts_on\n"
        "/alerts_off"
    )

async def setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /setup SYMBOL RISK(low/medium/high)")
    asset = context.args[0].upper()
    risk = context.args[1].lower()
    set_user(update.effective_chat.id, asset, risk)
    await update.message.reply_text(f"✅ Profile saved: {asset}, Risk: {risk}")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_chat.id)
    if not user:
        return await update.message.reply_text("❌ Please setup your profile first: /setup SYMBOL RISK")
    res = analyze(user["asset"], user["risk"])
    msg = (
        f"📊 {user['asset']} Market Update\n"
        f"Price: {res['price']}\n"
        f"RSI: {res['rsi']}\n"
        f"MACD: {res['macd']}\n"
        f"Score: {res['score']}/7\n"
        f"Recommendation: {res['signal']}\n\n"
        "⚠️ Educational only"
    )
    await update.message.reply_text(msg)

async def alerts_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    toggle_alert(update.effective_chat.id, True)
    await update.message.reply_text("🔔 Alerts ON")

async def alerts_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    toggle_alert(update.effective_chat.id, False)
    await update.message.reply_text("🔕 Alerts OFF")

# ----------------- BOT SETUP -----------------

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setup", setup))
app.add_handler(CommandHandler("signal", signal))
app.add_handler(CommandHandler("alerts_on", alerts_on))
app.add_handler(CommandHandler("alerts_off", alerts_off))

# ----------------- WEBHOOK SETUP -----------------

# Replit provides a public URL
REPL_URL = os.environ.get("https://marketaibot--AnthonylMwebaza.replit.app")  # e.g., https://your-repl-name.username.repl.co
PORT = int(os.environ.get("PORT", 3000))  # Replit sets PORT automatically

if REPL_URL:
    WEBHOOK_URL = f"{REPL_URL}/{TOKEN}"
    print(f"Setting webhook to {WEBHOOK_URL}")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )
else:
    print("REPL_URL not set. Running with polling (testing only).")
    app.run_polling()
