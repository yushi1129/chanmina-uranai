import os
import openai

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_uranai(birthday, seiza, blood_type):
    try:
        messages = [
            {"role": "system", "content": "あなたはちゃんみな風の占い師です。情熱的に励ます口調で。"},
            {"role": "user", "content": f"{birthday}生まれ、{seiza}、{blood_type}の私の今日の運勢を占ってください。\n"
                                        "・総合運\n・恋愛運\n・金運\n・仕事運\n・ラッキーカラー\n・ラッキーアイテム\n"
                                        "すべてちゃんみな風で。"}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"[GPTエラー] {e}")
        return "⚠️ 占い中に問題が発生しちゃった…時間をおいてまた来てね！"
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderが渡してくるPORTを使用
    app.run(host="0.0.0.0", port=port)
