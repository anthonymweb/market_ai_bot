from fastapi import FastAPI
import threading
import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from users import set_user, get_user, toggle_alert
from engine import analyze
from config import TOKEN

# ---------- FastAPI App for health check ----------
api = FastAPI()

@api.get("/")
def root():
    return {"status": "ok"}  # Respond quickly for health checks

# ---------- Telegram Bot ----------

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Advanced Market Bot\n/start /setup /signal /alerts_on /alerts_off")

async def setup(update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /setup SYMBOL RISK")
    asset = context.args[0].upper()
    risk = context.args[1].lower()
    set_user(update.effective_chat.id, asset, risk)
    await update.message.reply_text(f"✅ Profile saved: {asset}, Risk: {risk}")

async def signal(update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_chat.id)
    if not user:
        return await update.message.reply_text("❌ Setup first: /setup SYMBOL RISK")
    res = analyze(user["asset"], user["risk"])
    msg = f"📊 {user['asset']}\nPrice: {res['price']}\nScore: {res['score']}/7\nSignal: {res['signal']}"
    await update.message.reply_text(msg)

async def alerts_on(update, context: ContextTypes.DEFAULT_TYPE):
    toggle_alert(update.effective_chat.id, True)
    await update.message.reply_text("🔔 Alerts ON")

async def alerts_off(update, context: ContextTypes.DEFAULT_TYPE):
    toggle_alert(update.effective_chat.id, False)
    await update.message.reply_text("🔕 Alerts OFF")

# ---------- Telegram Setup ----------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setup", setup))
app.add_handler(CommandHandler("signal", signal))
app.add_handler(CommandHandler("alerts_on", alerts_on))
app.add_handler(CommandHandler("alerts_off", alerts_off))

# ---------- Run Bot in Thread ----------
def run_bot():
    REPL_URL = os.environ.get("https://marketaibot--AnthonylMwebaza.replit.app")
    PORT = int(os.environ.get("PORT", 3000))
    if REPL_URL:
        WEBHOOK_URL = f"{REPL_URL}/{TOKEN}"
        print(f"Webhook URL: {WEBHOOK_URL}")
        app.run_webhook(listen="0.0.0.0", port=PORT, webhook_url=WEBHOOK_URL)
    else:
        app.run_polling()

threading.Thread(target=run_bot, daemon=True).start()
