import requests
import os
from logger import logger
from together import Together
from textresources import TextResources

texts = TextResources()

class Llm:
    def context(self, intent, confidence):
        critical = ["ideacao_suicida", "autolesao", "relato_crise"]
        serious = ["relato_perda", "relato_tristeza", "relato_solidao"]

        if intent == "nlu_fallback":
            context = (
                texts.get("context", "nluFallbackHighConfidence") if confidence >= 0.85 else
                texts.get("context", "nluFallbackMediumConfidence") if 0.7 <= confidence < 0.85 else
                texts.get("context", "nluFallbackLowConfidence")
            )
        elif intent in critical:
            context = (
                texts.get("context", "criticalHighConfidence") if confidence >= 0.5 else
                texts.get("context", "criticalLowConfidence")
            )
        elif intent in serious:
            context = (
                texts.get("context", "seriousHighConfidence") if confidence >= 0.5 else
                texts.get("context", "seriousLowConfidence")
            )
            print(context)
        else:
            context = (
                texts.get("context", "highConfidence") if confidence >= 0.9 else
                texts.get("context", "mediumConfidence") if 0.7 <= confidence < 0.9 else
                texts.get("context", "lowConfidence") if 0.4 <= confidence < 0.7 else
                texts.get("context", "uncomprehended")
            )
            
        return (
            f"{texts.get('context', 'default')}\n"
            f"Baseado na mensagem do usuário siga essas orientações: {context}\n"
        )

    async def response(self, messages):
        if os.environ.get("LLM_API", "TOGETHER").upper() == "TOGETHER":
            return await self.together_api(messages)
        else:
            return await self.open_api(messages)

    async def open_api(self, messages):
        try:
            headers = {
                "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "gpt-4o",
                "messages": messages,
                "max_tokens": 450,
                "temperature": 0.7
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.info(f"OpenAI error: {str(e)}")
            return texts.get("fallback", "llm")

        return response.json()["choices"][0]["message"]["content"] or texts.get("fallback", "llm")

    async def together_api(self, messages):
        try:
            client = Together()

            response = client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
                messages= messages
            )
        except Exception as e:
            logger.info(f"Together API error: {str(e)}")
            return texts.get("fallback", "llm")

        return response.choices[0].message.content or texts.get("fallback", "llm")

llm = Llm()
