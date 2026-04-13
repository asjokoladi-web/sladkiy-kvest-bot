import os
import requests
from flask import Flask, request

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

user_step = {}

# ============ ПРАВИЛЬНАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ ============

STEP_1_QUESTION = """🍬 **Привет, юный исследователь!**

Профессор Сладков забыл, куда положил первый QR-код. Он помнит, что положил его где-то в коробке.

**Посмотри, какая сладость в самой большой упаковке? Напиши её название в бот!**

📌 *Подсказка: в слове 16 букв*"""

STEP_1_SUCCESS = """✅ **Правильно! Воздушные Зефирки!**

QR-код с игрой **«Сладкий лабиринт»** лежит в раскраске на **1 странице**.

Сканируй код и сыграй в игру. После победы ты получишь кодовое слово.

**Введи его сюда:**"""

STEP_2_QUESTION = "🔐 **Введи кодовое слово из игры «Сладкий лабиринт»:**"
STEP_2_SUCCESS = """✅ **Верно! Карамелька!**

Ты прошёл первое испытание.

Следующее испытание ждёт тебя на **второй странице раскраски**. Переходи ко второму квесту!

**Напиши секретное слово:**"""

STEP_3_QUESTION = "📝 **Напиши секретное слово со второй страницы раскраски:**"
STEP_3_SUCCESS = """✅ **Верно! Память!**

Ищи второй QR-код игры **под левым клапаном дна коробки**.

Сканируй его и сыграй в игру **«Мемори»**. После победы ты получишь секретное слово.

**Введи его сюда:**"""

STEP_4_QUESTION = "🎴 **Введи секретное слово из игры «Мемори»:**"
STEP_4_SUCCESS = """✅ **Верно! Конфета!**

Ты прошёл второе испытание.

Следующее испытание ждёт тебя на **третьей странице раскраски**. Переходи к третьему квесту!

**Напиши секретное слово:**"""

STEP_5_QUESTION = "📝 **Напиши секретное слово с третьей страницы раскраски:**"
STEP_5_SUCCESS = """✅ **Верно! Баланс!**

Чтобы открыть QR-код следующей игры, **загляни за письмо профессора Сладкова**.

Сканируй его и сыграй в игру **«Баланс»**. После победы ты получишь секретное слово.

**Введи его сюда:**"""

STEP_6_QUESTION = "🎮 **Введи секретное слово из игры «Баланс»:**"
STEP_6_SUCCESS = """✅ **Молодец! Зефирка!**

Ты прошёл третье испытание.

Следующее ждёт тебя на **четвёртой странице раскраски**. Переходи к четвёртому квесту!

**Напиши секретное слово:**"""

STEP_7_QUESTION = "📝 **Напиши секретное слово с четвёртой страницы раскраски:**"
STEP_7_SUCCESS = """✅ **Верно! Цвет!**

«Закрашивать клетки — это старый шпионский метод!»

Чтобы открыть QR-код следующей игры, **загляни в левый боковой клапан коробки**.

Сканируй его и сыграй в игру **«Цветной миксер»**. После победы ты получишь секретное слово.

**Введи его сюда:**"""

STEP_8_QUESTION = "🎨 **Введи секретное слово из игры «Цветной миксер»:**"
STEP_8_SUCCESS = """✅ **Молодец! Мармелад!**

Ты прошёл четвёртое испытание.

Впереди встреча с самим **Королём сахарных троллей**. Переходи к **5 испытанию**!

Пройди квест и **напиши секретное слово:**"""

STEP_9_QUESTION = "👑 **Введи секретное слово из пятого квеста:**"
STEP_9_SUCCESS = """✅ **Отлично, ты справился и с этим заданием!**

На **6 странице раскраски** ты найдёшь QR-код для битвы с Королём сахарных троллей.

Желаю тебе лёгкой и быстрой победы!

Когда победишь — **возвращайся с кодовым словом**, чтобы узнать, где находится главный приз!"""

STEP_10_QUESTION = "⚔️ **Введи кодовое слово после победы над Королём троллей:**"
STEP_10_SUCCESS = """🎉 **ПОЗДРАВЛЯЮ, МОЙ ЮНЫЙ ДРУГ!** 🎉

Ты прогнал Короля сахарных троллей из лаборатории, тем спас сладости и профессора Сладкова.

А теперь усаживайся поудобнее и смотри мультфильм, чтобы узнать, где профессор спрятал главный приз!

🎬 https://youtu.be/BDNfNYRaexg"""

STEPS = {
    1: {"question": STEP_1_QUESTION, "answer": "воздушные зефирки", "success": STEP_1_SUCCESS, "next": 2},
    2: {"question": STEP_2_QUESTION, "answer": "карамелька", "success": STEP_2_SUCCESS, "next": 3},
    3: {"question": STEP_3_QUESTION, "answer": "память", "success": STEP_3_SUCCESS, "next": 4},
    4: {"question": STEP_4_QUESTION, "answer": "конфета", "success": STEP_4_SUCCESS, "next": 5},
    5: {"question": STEP_5_QUESTION, "answer": "баланс", "success": STEP_5_SUCCESS, "next": 6},
    6: {"question": STEP_6_QUESTION, "answer": "зефирка", "success": STEP_6_SUCCESS, "next": 7},
    7: {"question": STEP_7_QUESTION, "answer": "цвет", "success": STEP_7_SUCCESS, "next": 8},
    8: {"question": STEP_8_QUESTION, "answer": "мармелад", "success": STEP_8_SUCCESS, "next": 9},
    9: {"question": STEP_9_QUESTION, "answer": "спаси сладкую лабораторию", "success": STEP_9_SUCCESS, "next": 10},
    10: {"question": STEP_10_QUESTION, "answer": "победа", "success": STEP_10_SUCCESS, "next": 0}
}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
    except Exception as e:
        print(e)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'message' not in data:
        return "OK", 200
    
    chat_id = data['message']['chat']['id']
    text = data['message'].get('text', '').lower().strip()
    
    if text == '/start':
        user_step[chat_id] = 1
        send_message(chat_id, STEPS[1]["question"])
        return "OK", 200
    
    step = user_step.get(chat_id, 0)
    
    if step == 0:
        send_message(chat_id, "Напиши /start, чтобы начать квест!")
        return "OK", 200
    
    if text == STEPS[step]["answer"]:
        send_message(chat_id, STEPS[step]["success"])
        next_step = STEPS[step]["next"]
        if next_step == 0:
            user_step[chat_id] = 0
        else:
            user_step[chat_id] = next_step
    else:
        send_message(chat_id, "❌ Неправильно, попробуй ещё раз!")
    
    return "OK", 200

@app.route('/healthcheck')
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if render_url:
        webhook_url = f"{render_url}/webhook"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/setWebhook", json={"url": webhook_url})
        print(f"Webhook: {webhook_url}")
    app.run(host='0.0.0.0', port=port)
