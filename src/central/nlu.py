import requests
import os
from logger import logger

class Nlu:
    async def parse(self, message: str):
        try:
            nlu_host = os.environ.get("NLU_HOST", "http://localhost:5005")
            logger.info(f"Start request to NLU {nlu_host}")

            response = requests.post(
                nlu_host + "/model/parse",
                json={"text": message},
                timeout=5
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.info(f"NLU error: {str(e)}")
            return "nlu_fallback", 0.0

        nlu_data = response.json()
        intent = nlu_data.get("intent", {}).get("name", "nlu_fallback")
        confidence = nlu_data.get("intent", {}).get("confidence", 0.0)
        return intent, confidence
    
nlu = Nlu()