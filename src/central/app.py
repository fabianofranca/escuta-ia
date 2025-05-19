from fastapi import FastAPI
from pydantic import BaseModel
from nlu import nlu
from llm import llm
from logger import logger
from textresources import TextResources
import json
import os

texts = TextResources()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    intent: str
    confidence: float

previous_response = {}

@app.post("/message")
async def handle_message(data: ChatRequest):
    global previous_response

    fallback = {
        "response": texts.get("fallback", "llm"),
        "message": "",
        "intent": "nlu_fallback",
        "confidence": 0.0,
        "resume": ""
    }

    try:

        intent, confidence = await nlu.parse(data.message)

        if intent is None:
            intent = data.intent
            confidence = data.confidence

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

        logger.info(f"Starting request to LLM: {os.environ.get('LLM_API', 'TOGETHER')}")

        raw = await llm.response(messages)

        logger.info(f"LLM Response successfully")

        clean_raw = raw.strip().removeprefix("```json").removesuffix("```").strip()

        logger.info(f"LLM Response:\n{clean_raw}")

        payload = json.loads(clean_raw)

    except Exception as e:
        logger.error(f"Handle message error: {e}")

    previous_response = {
        "response": payload.get("response") or fallback["response"],
        "message": payload.get("message") or fallback["message"],
        "intent": payload.get("intent") or fallback["intent"],
        "confidence": payload.get("confidence") or fallback["confidence"],
        "resume": payload.get("resume") or fallback["resume"]
    }

    return previous_response

@app.get("/health")
async def health_check():
    return {"status": "ok"}