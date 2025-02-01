from fastapi import FastAPI, Request, HTTPException
import google.generativeai as genai
import os
import logging

app = FastAPI()

# APIキーの設定（環境変数から取得）
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.post("/assistant_ai")
async def assistant_ai(request: Request):
    try:
        data = await request.json()
    except Exception as e:
        logging.error(f"JSONのパースエラー: {e}")
        raise HTTPException(status_code=400, detail="無効な JSON です")

    user_input = data.get("query")
    if not user_input:
        raise HTTPException(status_code=400, detail="JSONに 'query' フィールドがありません")

    try:
        # GenerativeModel クラスを使ってモデルを作成
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # 1回の応答を取得する場合
        response = model.generate_content(user_input)
        
        # または、チャット形式のセッションを利用する場合（オプション）
        # chat = model.start_chat()
        # response = chat.send_message(user_input)

    except Exception as e:
        logging.error(f"Gemini API 呼び出しエラー: {e}")
        raise HTTPException(status_code=500, detail="Gemini API の呼び出しに失敗しました")

    # APIのレスポンスからテキストを取得
    ai_response = response.text if hasattr(response, "text") else None
    if not ai_response:
        raise HTTPException(status_code=500, detail="Gemini API から応答がありません")

    return {"fulfillmentText": ai_response}
