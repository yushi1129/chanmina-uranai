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
        }
    )
    return "OK"

def get_uranai(birthday, seiza, blood_type):
    try:
        print(f"[DEBUG] 呼び出し開始：{birthday}, {seiza}, {blood_type}")
        messages = [
            {"role": "system", "content": "あなたはちゃんみな風の占い師です。"},
            {"role": "user", "content": f"{birthday}生まれ、{seiza}、{blood_type}の私の今日の運勢を占って。\n"
                                        "・総合運\n・恋愛運\n・金運\n・仕事運\n・ラッキーカラー\n・ラッキーアイテム\n"
                                        "すべてちゃんみな風で。"}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[GPTエラー] {e}")  # ← これが出ないと原因が見えない！
        return "⚠️ 占い中に問題が発生しちゃった…またあとで来てね！"


# 🔽 これがないとRenderで公開されない
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
