import os
import openai
import requests
from flask import Flask, request

# Flaskアプリの初期化
app = Flask(__name__)

# OpenAIクライアントの初期化
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

# ルート確認用（ヘルスチェック）
@app.route("/")
def home():
    return "LINE占いBot 稼働中！"

# Webhookエンドポイント
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    print(f"[DEBUG] 受信body: {body}", flush=True)

    try:
        event = body["events"][0]
        if "message" not in event or "text" not in event["message"]:
            print("[DEBUG] textメッセージではありません", flush=True)
            return "OK"

        user_text = event["message"]["text"]
        reply_token = event["replyToken"]

        print(f"[DEBUG] ユーザー入力（repr）: {repr(user_text)}", flush=True)

        parts = user_text.strip().split(maxsplit=2)
        print(f"[DEBUG] 分割結果: {parts}", flush=True)

        if len(parts) != 3:
            raise ValueError("入力形式エラー")

        birthday, seiza, blood = parts
        print(f"[DEBUG] 呼び出し開始: {birthday}, {seiza}, {blood}", flush=True)

        reply = get_uranai(birthday, seiza, blood)

    except Exception as e:
        print(f"[DEBUG] 例外発生: {e}", flush=True)
        reply = "⚠️ 入力形式が正しくないよ！\n例：1995-01-01 おうし座 A型"

    # LINEへ返信
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

# GPTを使った占い関数
def get_uranai(birthday, seiza, blood_type):
    try:
        messages = [
            {"role": "system", "content": "あなたはちゃんみな風の占い師です。"},
            {"role": "user", "content": f"{birthday}生まれ、{seiza}、{blood_type}の私の今日の運勢を占って。\n・総合運\n・恋愛運\n・金運\n・仕事運\n・ラッキーカラー\n・ラッキーアイテム\nすべてちゃんみな風で。"}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"[GPTエラー] {e}", flush=True)
        return "⚠️ 占い中に問題が発生しちゃった…またあとで来てね！"

# Renderでの起動設定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Renderでの起動設定
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
