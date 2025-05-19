def get_uranai(birthday, seiza, blood_type):
    try:
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
    except Exception as e:
        print(f"[ERROR] GPT呼び出しに失敗: {e}")
        return "⚠️ 占い中にエラーが発生しちゃった…時間をおいてもう一度試してみてね。"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderが渡してくるPORTを使用
    app.run(host="0.0.0.0", port=port)
