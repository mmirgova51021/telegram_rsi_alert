from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Čítanie z environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    print("Telegram odpoveď:", response.status_code, response.text)  # DEBUG výpis
    return response.json()

@app.route('/', methods=['POST'])
def receive_alert():
    data = request.get_json()
    message = data.get('message', 'RSI otočka signál bez správy.')
    send_telegram_message(message)
    return {'status': 'ok'}, 200

# Spustenie servera
app.run(host='0.0.0.0', port=8080)

