from fastapi import FastAPI
from pydantic import BaseModel
from nlu import nlu
from llm import llm
import json

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

previous_response = {}

@app.post("/message")
async def handle_message(data: ChatRequest):
    global previous_response

    intent, confidence = await nlu.parse(data.message)

    user_content = (
        f"Resumo anterior: {previous_response.get('resume') or 'Ainda não tem resumo' }\n"
        f"intent: {intent}\n"
        f"confidence: {confidence}\n"
        f"Última mensagem: {previous_response.get('message') or 'Não há mensagem anterior'}\n"
        f"Nova mensagem: {data.message}"
    )

    messages = [
            {"role": "system", "content": llm.context(intent, confidence)},
            {"role": "user", "content": user_content}
        ]

    raw = await llm.response(messages)

    payload = json.loads(raw.strip().removeprefix("```json").removesuffix("```").strip())

    previous_response = {
        "response": payload["response"],
        "message": payload["message"],
        "intent": payload["intent"],
        "confidence": payload["confidence"],
        "resume": payload["resume"]
    }

    return previous_response

@app.get("/health")
async def health_check():
    return {"status": "ok"}