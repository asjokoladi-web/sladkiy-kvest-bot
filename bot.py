import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

# Простой словарь для состояний
user_step = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'message' not in data:
        return "OK", 200
    
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '').lower().strip()
    
    # Команда /start
    if text == '/start':
        send_message(chat_id, "🍬 Привет! Какая сладость в самой большой упаковке? Подсказка: 16 букв")
        user_step[chat_id] = 1
        return "OK", 200
    
    # Проверка ответа
    if user_step.get(chat_id) == 1:
        if text == "воздушные зефирки":
            send_message(chat_id, "✅ Правильно! https://youtu.be/BDNfNYRaexg")
            user_step[chat_id] = 0
        else:
            send_message(chat_id, "❌ Неправильно, попробуй ещё раз!")
    
    return "OK", 200

@app.route('/healthcheck')
def health():
    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
