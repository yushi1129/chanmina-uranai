import os
import openai
import requests
from flask import Flask, request

app = Flask(__name__)  # ← 必須！

# OpenAI APIクライアント
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

@app.route("/")
def home():
    return "LINE占いBot 稼働中！"

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    user_text = body["events"][0]["message"]["text"]
    reply_token = body["events"][0]["replyToken"]

    try:
        parts = user_text.strip().split()
        if len(parts) != 3:
            raise ValueError("入力形式エラー")
        birthday, seiza, blood = parts
        reply = get_uranai(birthday, seiza, blood)
    except Exception:
        reply = "⚠️ 入力形式が正しくないよ！\n例：1995-01-01 おひつじ座 A型"

    requests.post(
        'https://api.line.me/v2/bot/message/reply',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
        },
        json={
            'replyToken': reply_token,
            'messages': [{'type': 'text', 'text': reply}]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderが渡してくるPORTを使用
    app.run(host="0.0.0.0", port=port)
