import os
from flask import Flask, request
import openai
import requests

app = Flask(__name__)

# 🔐 安全な方法：環境変数から取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def get_uranai(birthday, seiza, blood_type):
    messages = [
        {"role": "system", "content": "あなたはちゃんみな風の占い師です。情熱的に励ます口調で話してください。"},
        {"role": "user", "content": f"{birthday}生まれ、{seiza}、{blood_type}の私の今日の運勢を占ってください。\n"
                                    "・総合運\n・恋愛運\n・金運\n・仕事運\n・ラッキーカラー\n・ラッキーアイテム\nすべてちゃんみな風で。"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response["choices"][0]["message"]["content"]

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    reply_token = body["events"][0]["replyToken"]
    user_text = body["events"][0]["message"]["text"]

    if user_text.lower() in ["こんにちは", "start", "占い", "うらない", "hello"]:
        reply_message = (
            "🔮 ちゃんみな占いへようこそ 🔮\n\n"
            "以下のように情報を送ってね：\n"
            "📅 生年月日（例：1995-03-07）\n"
            "♈ 星座（例：おひつじ座）\n"
            "🩸 血液型（例：A型）\n\n"
            "👉 例）1995-03-07 おひつじ座 A型"
        )
    else:
        try:
            parts = user_text.strip().split()
            birthday, seiza, blood_type = parts[0], parts[1], parts[2]
            reply_message = get_uranai(birthday, seiza, blood_type)
        except Exception:
            reply_message = (
                "⚠️ 入力形式が正しくないみたい。\n\n"
                "例：1995-03-07 おうし座 A型\n"
                "3つをスペースで区切って送ってね。"
            )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": reply_message}]
    }
    requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, json=body)
    return "OK"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderでは PORT 環境変数を使う
    app.run(host="0.0.0.0", port=port)

