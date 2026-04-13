import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Токен бота из переменных окружения
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN не задан!")

# Базовый URL API Telegram
API_URL = f"https://api.telegram.org/bot{TOKEN}"

# Хранилище этапов квеста (в памяти)
user_steps = {}

# Правильные ответы (все в нижнем регистре)
ANSWERS = {
    1: "воздушные зефирки",
    2: "карамелька",
    3: "память",
    4: "конфета",
    5: "баланс",
    6: "зефирка",
    7: "цвет",
    8: "мармелад",
    9: "спаси сладкую лабораторию",
    10: "победа"
}

# Сообщения бота
MESSAGES = {
    0: "🍬 Привет, юный исследователь!\n\nПрофессор Сладков забыл, куда положил первый QR-код. Он помнит, что положил его где-то в коробке.\n\n**Посмотри, какая сладость в самой большой упаковке?**\nНапиши её название в бот!\n\n📌 Подсказка: в слове 16 букв",
    
    1: "✅ Правильно!\n\nQR-код с игрой «Сладкий лабиринт» лежит в раскраске на 1 странице.\nСканируй код, сыграй в игру. После победы ты получишь кодовое слово — введи его.",
    
    2: "✅ Верно! Ты прошёл первое испытание.\n\nСледующее задание ждёт тебя на второй странице раскраски.\nПереходи ко второму квесту и напиши секретное слово.",
    
    3: "✅ Верно!\n\nИщи второй QR-код игры под левым клапаном дна коробки.\nСканируй его и сыграй в игру «Мемори».\nПосле победы получишь секретное слово — введи его.",
    
    4: "✅ Верно! Ты прошёл второе испытание.\n\nСледующее — на третьей странице раскраски.\nПереходи к третьему квесту и напиши секретное слово.",
    
    5: "✅ Верно!\n\nЧтобы открыть QR-код следующей игры, загляни за письмо профессора Сладкова.\nСканируй код, сыграй в игру «Баланс».\nПосле победы введи секретное слово.",
    
    6: "✅ Молодец! Ты прошёл третье испытание.\n\nСледующее ждёт тебя на четвёртой странице раскраски.\nПереходи к четвёртому квесту, разгадай его и напиши секретное слово.",
    
    7: "✅ Верно!\n\n«Закрашивать клетки — это старый шпионский метод!»\nQR-код следующей игры — в левом боковом клапане коробки.\nСканируй его, сыграй в игру «Цветной миксер».\nПосле победы введи секретное слово.",
    
    8: "✅ Молодец! Ты прошёл четвёртое испытание.\n\nВпереди встреча с самим Королём сахарных троллей.\nПереходи к 5 испытанию! Пройди квест и напиши секретное слово.",
    
    9: "✅ Отлично, ты справился и с этим заданием!\n\nНа 6 странице раскраски ты найдёшь QR-код для битвы с Королём сахарных троллей.\nЖелаю лёгкой и быстрой победы!\nКогда победишь — возвращайся с кодовым словом.",
    
    10: "🎉 ПОЗДРАВЛЯЮ, МОЙ ЮНЫЙ ДРУГ!\n\nТы прогнал Короля сахарных троллей из лаборатории, спас сладости и профессора Сладкова.\n\nА теперь смотри мультфильм, чтобы узнать, где профессор спрятал главный приз!\n\n👉 https://youtu.be/BDNfNYRaexg"
}

def send_message(chat_id, text):
    """Отправляет сообщение в Telegram"""
    url = f"{API_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return None

def set_webhook(url):
    """Устанавливает веб-хук"""
    webhook_url = f"{API_URL}/setWebhook"
    data = {"url": url}
    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        print(f"Webhook установлен: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Ошибка установки webhook: {e}")
        return None

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return "OK", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обрабатывает входящие сообщения"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return "OK", 200
        
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '').lower().strip()
        
        print(f"Получено сообщение от {chat_id}: {text}")
        
        # Команда /start - начинаем квест
        if text == '/start':
            user_steps[chat_id] = 1  # Начинаем с первого вопроса
            send_message(chat_id, MESSAGES[0])
            return "OK", 200
        
        # Команда /reset - сброс квеста
        if text == '/reset':
            user_steps[chat_id] = 1
            send_message(chat_id, "🔄 Квест сброшен! Давай начнём заново!\n\n" + MESSAGES[0])
            return "OK", 200
        
        # Получаем текущий этап пользователя
        current_step = user_steps.get(chat_id, 0)
        
        # Если пользователь не в квесте
        if current_step == 0:
            send_message(chat_id, "Напиши /start, чтобы начать квест!")
            return "OK", 200
        
        # Проверяем ответ
        expected_answer = ANSWERS.get(current_step)
        
        if text == expected_answer:
            # Правильный ответ
            send_message(chat_id, MESSAGES[current_step])
            
            if current_step == 10:
                # Квест завершён
                user_steps[chat_id] = 0
            else:
                # Переходим к следующему шагу
                user_steps[chat_id] = current_step + 1
        else:
            # Неправильный ответ
            send_message(chat_id, "❌ Неправильно, попробуй ещё раз!")
        
        return "OK", 200
        
    except Exception as e:
        print(f"Ошибка в webhook: {e}")
        return "OK", 200

@app.route('/', methods=['GET'])
def home():
    return "Бот работает!", 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    
    # Получаем URL от Render
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if render_url:
        webhook_url = f"{render_url}/webhook"
        set_webhook(webhook_url)
    
    print(f"Запуск бота на порту {port}")
    app.run(host='0.0.0.0', port=port)
