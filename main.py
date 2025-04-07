from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Telegram údaje (Render > Environment Variables)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# URL pre posielanie správ
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    # Ak správa nie je validná
    if not data:
        return "No data received", 400

    # Očakávame formát: {"text": "BUY"} alebo {"message": "SELL"}
    message = data.get("text") or data.get("message")

    if message:
        payload = {
            'chat_id': CHAT_ID,
            'text': message
        }
        response = requests.post(TELEGRAM_URL, data=payload)

        if response.status_code == 200:
            return "Message sent to Telegram", 200
        else:
            return f"Failed to send message. Error: {response.text}", 500
    else:
        return "No 'text' or 'message' field in JSON", 400

@app.route('/', methods=['GET'])
def home():
    return "Telegram RSI Alert bot is running!", 200

if __name__ == '__main__':
    app.run()



