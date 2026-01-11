import time
from users import users
from engine import analyze

def start(app):
    """Auto alert engine running every 30 mins"""
    while True:
        for chat_id, data in users.items():
            if data["alerts"]:
                res = analyze(data["asset"], data["risk"])
                if res["signal"] != "OBSERVE":
                    app.bot.send_message(
                        chat_id=int(chat_id),
                        text=(
                            f"🚨 AUTO ALERT\n"
                            f"{data['asset']}\n"
                            f"Price: {res['price']}\n"
                            f"Signal: {res['signal']}\n"
                            f"Score: {res['score']}/7\n\n"
                            "⚠️ Educational only"
                        )
                    )
        time.sleep(1800)  # 30 minutes
