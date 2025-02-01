from fastapi import FastAPI, Request, HTTPException
import google.generativeai as genai
import logging

app = FastAPI()

# Gemini API の API キーを設定（実際のキーに置き換えてください）
genai.configure(api_key="AIzaSyDua3pkDq9HfGP1Ea_FICVXI0yASKw9SvI")

@app.post("/assistant_ai")
async def assistant_ai(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        logging.error(f"JSON parse error: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    user_input = data.get("query")
    if not user_input:
        raise HTTPException(status_code=400, detail="Missing 'query' field in JSON")

    try:
        # 正しいメソッド名に変更（例：ChatCompletion.create を使用）
        response = genai.ChatCompletion.create(
            model="gemini-1.5",  # ※実際に利用するモデル名を確認してください
            messages=[{"role": "user", "content": user_input}]
        )
    except Exception as e:
        logging.error(f"Gemini API call error: {e}")
        raise HTTPException(status_code=500, detail="Error calling Gemini API")

    # API のレスポンス形式に応じて応答を抽出（例：下記は仮の例です）
    # もしレスポンスが { "candidates": [ {"output": "応答文" }, ... ] } の形式なら：
    try:
        ai_response = response["candidates"][0]["output"]
    except Exception as e:
        logging.error(f"Response parsing error: {e}")
        raise HTTPException(status_code=500, detail="Error parsing Gemini API response")

    return {"fulfillmentText": ai_response}
