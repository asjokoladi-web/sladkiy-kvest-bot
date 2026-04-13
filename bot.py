import os
import requests
from flask import Flask, request

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

# Храним этап каждого пользователя
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
        send_message(chat_id, 
            "🍬 Привет, юный исследователь!\n\n"
            "Профессор Сладков забыл, куда положил первый QR-код. Он помнит, что положил его где-то в коробке.\n\n"
            "**Посмотри, какая сладость в самой большой упаковке?**\n"
            "Напиши её название в бот!\n\n"
            "📌 Подсказка: в слове 16 букв")
        user_step[chat_id] = 1
        return "OK", 200
    
    # Проверка ответа на первый вопрос
    if user_step.get(chat_id) == 1:
        if text == "воздушные зефирки":
            send_message(chat_id, 
                "✅ Правильно!\n\n"
                "QR-код с игрой «Сладкий лабиринт» лежит в раскраске на 1 странице.\n"
                "Сканируй код, сыграй в игру. После победы ты получишь кодовое слово — введи его.")
            user_step[chat_id] = 2
        else:
            send_message(chat_id, "❌ Неправильно, попробуй ещё раз!")
        return "OK", 200
    
    # Проверка ответа на второй вопрос (Карамелька)
    if user_step.get(chat_id) == 2:
        if text == "карамелька":
            send_message(chat_id, 
                "✅ Верно! Ты прошёл первое испытание.\n\n"
                "Следующее задание ждёт тебя на второй странице раскраски.\n"
                "Переходи ко второму квесту и напиши секретное слово.")
            user_step[chat_id] = 3
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    # Проверка ответа на третий вопрос (Память)
    if user_step.get(chat_id) == 3:
        if text == "память":
            send_message(chat_id, 
                "✅ Верно!\n\n"
                "Ищи второй QR-код игры под левым клапаном дна коробки.\n"
                "Сканируй его и сыграй в игру «Мемори».\n"
                "После победы получишь секретное слово — введи его.")
            user_step[chat_id] = 4
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    # Проверка ответа на четвёртый вопрос (Конфета)
    if user_step.get(chat_id) == 4:
        if text == "конфета":
            send_message(chat_id, 
                "✅ Верно! Ты прошёл второе испытание.\n\n"
                "Следующее — на третьей странице раскраски.\n"
                "Переходи к третьему квесту и напиши секретное слово.")
            user_step[chat_id] = 5
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    # Проверка ответа на пятый вопрос (Баланс)
    if user_step.get(chat_id) == 5:
        if text == "баланс":
            send_message(chat_id, 
                "✅ Верно!\n\n"
                "Чтобы открыть QR-код следующей игры, загляни за письмо профессора Сладкова.\n"
                "Сканируй код, сыграй в игру «Баланс».\n"
                "После победы введи секретное слово.")
            user_step[chat_id] = 6
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    # Проверка ответа на шестой вопрос (Зефирка)
    if user_step.get(chat_id) == 6:
        if text == "зефирка":
            send_message(chat_id, 
                "✅ Молодец! Ты прошёл третье испытание.\n\n"
                "Следующее ждёт тебя на четвёртой странице раскраски.\n"
                "Переходи к четвёртому квесту, разгадай его и напиши секретное слово.")
            user_step[chat_id] = 7
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    # Проверка ответа на седьмой вопрос (Цвет)
    if user_step.get(chat_id) == 7:
        if text == "цвет":
            send_message(chat_id, 
                "✅ Верно!\n\n"
                "«Закрашивать клетки — это старый шпионский метод!»\n"
                "QR-код следующей игры — в левом боковом клапане коробки.\n"
                "Сканируй его, сыграй в игру «Цветной миксер».\n"
                "После победы введи секретное слово.")
            user_step[chat_id] = 8
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    # Проверка ответа на восьмой вопрос (Мармелад)
    if user_step.get(chat_id) == 8:
        if text == "мармелад":
            send_message(chat_id, 
                "✅ Молодец! Ты прошёл четвёртое испытание.\n\n"
                "Впереди встреча с самим Королём сахарных троллей.\n"
                "Переходи к 5 испытанию! Пройди квест и напиши секретное слово.")
            user_step[chat_id] = 9
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    # Проверка ответа на девятый вопрос (спаси сладкую лабораторию)
    if user_step.get(chat_id) == 9:
        if text == "спаси сладкую лабораторию":
            send_message(chat_id, 
                "✅ Отлично, ты справился и с этим заданием!\n\n"
                "На 6 странице раскраски ты найдёшь QR-код для битвы с Королём сахарных троллей.\n"
                "Желаю лёгкой и быстрой победы!\n"
                "Когда победишь — возвращайся с кодовым словом.")
            user_step[chat_id] = 10
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    # Проверка ответа на десятый вопрос (Победа) + финал
    if user_step.get(chat_id) == 10:
        if text == "победа":
            send_message(chat_id, 
                "🎉 ПОЗДРАВЛЯЮ, МОЙ ЮНЫЙ ДРУГ!\n\n"
                "Ты прогнал Короля сахарных троллей из лаборатории, спас сладости и профессора Сладкова.\n\n"
                "А теперь смотри мультфильм, чтобы узнать, где профессор спрятал главный приз!\n\n"
                "👉 https://youtu.be/BDNfNYRaexg")
            user_step[chat_id] = 0
        else:
            send_message(chat_id, "❌ Неверно, попробуй ещё раз.")
        return "OK", 200
    
    return "OK", 200

@app.route('/healthcheck')
def health():
    return "OK", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
