from fastapi import FastAPI, Request
import google.generativeai as genai

app = FastAPI()

# Gemini API の API キーを設定（実際のキーに置き換えてください）
genai.configure(api_key="AIzaSyDua3pkDq9HfGP1Ea_FICVXI0yASKw9SvI")

@app.post("/assistant_ai")
async def assistant_ai(request: Request):
    data = await request.json()
    user_input = data.get("query", "こんにちは！")

    # Gemini API を呼び出し、AI 応答を取得
    response = genai.chat(
        model="gemini-1.5",
        messages=[{"role": "user", "content": user_input}]
    )

    ai_response = response.get("text", "すみません、応答が得られませんでした。")
    return {"fulfillmentText": ai_response}
