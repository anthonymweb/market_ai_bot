import json

FILE = "users.json"

# Load users or create empty dict
try:
    users = json.load(open(FILE))
except:
    users = {}

def save():
    with open(FILE, "w") as f:
        json.dump(users, f)

def set_user(chat_id, asset, risk):
    users[str(chat_id)] = {
        "asset": asset,
        "risk": risk,
        "alerts": False
    }
    save()

def get_user(chat_id):
    return users.get(str(chat_id))

def toggle_alert(chat_id, state):
    if str(chat_id) in users:
        users[str(chat_id)]["alerts"] = state
        save()
