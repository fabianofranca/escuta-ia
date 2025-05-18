from fastapi import FastAPI
from pydantic import BaseModel
from together import Together
import requests
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("escuta-ia")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

resume = ""
cvv = False

@app.post("/message")
async def handle_message(data: ChatRequest):
    global resume
    global cvv

    intent, confidence = await nlu(data.message)

    if intent is None:
        return {
            "message": "Desculpe, estou com dificuldade para entender agora. Você pode tentar novamente?"
        }

    messages = [
            {"role": "system", "content": Llm.get(intent, confidence, resume, cvv)},
            {"role": "user", "content": f"{data.message}[intent: {intent}][confidence: {confidence}]" }
            ]

    raw_response = llm_api(messages)

    fallback = "Desculpa, acho que tive uma pequena dificuldade para entender ou responder agora. Mas estou aqui com você, e quero muito continuar essa conversa. Se puder, me diga um pouco mais sobre o que está sentindo?"

    if "-[Resumo]-" in raw_response:
        parts = raw_response.split("-[Resumo]-")
        response = parts[0].strip() or fallback
        resume = parts[1].strip()
    else:
        response = raw_response.strip() or fallback

    if "CVV" in response:
        cvv = True

    return {
        "response": response,
        "intent": intent,
        "confidence": confidence,
        "resume": resume
    }

async def nlu(message: str):
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
        return None, None

    nlu_data = response.json()
    intent = nlu_data.get("intent", {}).get("name", "nlu_fallback")
    confidence = nlu_data.get("intent", {}).get("confidence", 0.0)
    return intent, confidence

class Llm:
    NLU_FALLBACK_HIGH_CONFIDENCE = "A detecção de fallback pode ter sido incorreta. Aja como se fosse uma mensagem legítima, acolhendo com escuta e continuidade. Evite repetir palavras ou expressões já usadas em respostas anteriores. Use linguagem acolhedora com variação natural."
    NLU_FALLBACK_MEDIUM_CONFIDENCE = "O usuário enviou uma mensagem possivelmente sensível, cuja intenção ainda não pôde ser classificada com confiança. Responda com acolhimento e cuidado, sem tentar interpretar diretamente. Varie sua linguagem para soar acolhedor e humano, evitando repetições."
    NLU_FALLBACK_LOW_CONFIDENCE = "O usuário enviou uma mensagem que não foi compreendida com segurança. Evite interpretar o conteúdo. Apenas acolha com gentileza e incentive o usuário a tentar se expressar novamente, sem forçar. Varie a forma de acolher para evitar repetições."
    CRITICAL_HIGH_CONFIDENCE = "O usuário expressou algo que pode indicar sofrimento grave. O grau de confiança indica risco emocional significativo. Aja com escuta empática, acolha com cuidado, e se apropriado, oriente o usuário a buscar ajuda humana, como o CVV (telefone 188). Não seja insistente. Mencione a existência do apoio com gentileza, sem julgamento, reforçando que ele não está sozinho. Evite dar conselhos ou interpretações. Apenas esteja presente. Evite repetir estruturas usadas anteriormente. Exemplo: Usuário: Eu só queria desaparecer… Assistente: Imagino o quanto deve estar difícil carregar isso. Saiba que não está sozinho. Existe apoio, como o CVV, se um dia quiser conversar com alguém."
    CRITICAL_LOW_CONFIDENCE = "O sistema tentou detectar a intenção da fala, e uma possibilidade é que se trate de uma crise emocional, mas a confiança nessa interpretação é baixa. Não reforce essa hipótese diretamente. Aja com escuta ativa, acolha com empatia, e convide o usuário a se expressar mais para que você compreenda melhor. Evite mencionar diretamente temas como suicídio ou autolesão. Priorize acolher e manter o espaço seguro e aberto. Use linguagem variada."
    SERIOUS_HIGH_CONFIDENCE = "O usuário compartilhou uma mensagem que parece refletir sofrimento emocional. Aja com empatia e escuta ativa. Convide o usuário, com delicadeza, a continuar se expressando, validando o que ele sente. Se sentir apropriado, mencione a possibilidade de procurar ajuda humana como o CVV (188), mas apenas como apoio complementar, sem pressão. Evite interpretações, conselhos ou minimizações. Mantenha um tom respeitoso e presente. Use variações para demonstrar escuta sensível e humana."
    SERIOUS_LOW_CONFIDENCE = "O sistema tentou interpretar a intenção como possível relato de tristeza, perda ou solidão, mas a confiança nessa classificação é baixa. Não afirme ou sugira interpretações. Acolha com cuidado e convide o usuário a falar mais, mantendo um espaço seguro, respeitoso e receptivo. Evite sugerir ajuda externa nesse momento. Seu papel é manter a escuta e permitir que o usuário se abra sem julgamentos. Evite repetir frases padrão."
    HIGH_CONFIDENCE = "Acolha com empatia e sem julgamentos. Mantenha uma escuta sensível e convide o usuário a continuar. Use formas variadas de demonstrar presença e acolhimento."
    MEDIUM_CONFIDENCE = "Não tenha certeza absoluta sobre a intenção. Aja com empatia, acolha, e convide o usuário a se expressar mais. Evite dar respostas fechadas. Varie o vocabulário para manter um tom humano e natural."
    LOW_CONFIDENCE = "A intenção do que foi dito não está clara. Ajude a manter a conversa fluindo, acolhendo com escuta ativa e empática. Evite pressa para interpretar. Convide o usuário a continuar se expressando. Evite repetir estruturas anteriores."
    UNCOMPREHENDED = "O usuário enviou uma mensagem que não foi compreendida com segurança. Evite interpretar o conteúdo. Apenas acolha com gentileza e incentive o usuário a tentar se expressar novamente, sem forçar. Busque expressar empatia com variedade de linguagem."

    @staticmethod
    def get(intent, confidence, resume, cvv):
        critical = ["ideacao_suicida", "autolesao", "relato_crise"]
        serious = ["relato_perda", "relato_tristeza", "relato_solidao"]

        if intent == "nlu_fallback":
            context = (
            Llm.NLU_FALLBACK_HIGH_CONFIDENCE if confidence >= 0.85 else
            Llm.NLU_FALLBACK_MEDIUM_CONFIDENCE if 0.7 <= confidence < 0.85 else
            Llm.NLU_FALLBACK_LOW_CONFIDENCE
            )
        elif intent in critical:
            context = (
            Llm.CRITICAL_HIGH_CONFIDENCE if confidence >= 0.5 else
            Llm.CRITICAL_LOW_CONFIDENCE
            )
            force_cvv = True
        elif intent in serious:
            context = (
            Llm.SERIOUS_HIGH_CONFIDENCE if confidence >= 0.5 and not cvv else
            Llm.SERIOUS_LOW_CONFIDENCE
            )
            print(context)
        else:
            context = (
            Llm.HIGH_CONFIDENCE if confidence >= 0.9 else
            Llm.MEDIUM_CONFIDENCE if 0.7 <= confidence < 0.9 else
            Llm.LOW_CONFIDENCE if 0.4 <= confidence < 0.7 else
            Llm.UNCOMPREHENDED
            )

        resume_context = """
Depois da resposta, gere um novo resumo da conversa até agora. Use o seguinte formato:-[Resumo]-[resumo atualizado]

Esse resumo deve:
- Ser emocional, não técnico;
- Evitar repetições de sentimentos já descritos;
- Acrescentar novas nuances, se surgirem;
- Mencionar o efeito da resposta do assistente (sem citar frases);
- Indicar se o usuário sinaliza melhora, recuo, cansaço ou desejo de encerrar.

Exemplo:
-[Resumo]-O usuário demonstrou sensação de invisibilidade e tristeza profunda. Expressou desejo de desaparecer por um tempo. O assistente acolheu com calma e validou o cansaço emocional, o que parece ter trazido um leve alívio.

Se não houver novas emoções ou mudanças, mantenha o resumo anterior.

Se você sugeriu ajuda externa, como o CVV, e o usuário aceitou, mencione isso no resumo. Se o usuário não aceitou a sugestão de ajuda externa, não mencione isso no resumo.	

Caso contrário, mantenha o acolhimento sem repetir a sugestão de ajuda externa.

Lembre-se: escuta é mais importante que resposta.
"""
            
        return (
            f"Você é um atendente emocional de uma ONG que oferece apoio emocional gratuito e sigiloso para pessoas em sofrimento, principalmente com pensamentos suicidas.\n"
            f"Sempre responda em português do Brasil.\n"
            f"A intenção detectada que você vai utilizar para gerar a mensagem para o usuário é {intent}, com confiança de {confidence:.2f}.\n"
            #f"{'Não cite a CVV nessa mensagem' if cvv and not force_cvv else ''}"            
            f"Use esse resumo para evitar repetições na mensagem enviado para o usuário e elaborar mensagens mais conectadas com o que foi dito: {resume or 'nenhuma informação ainda.'}\n"
            f"{context}\n"
            f"{resume_context}\n"
        )

def llm_api(messages):
    if os.environ.get("LLM_API", "TOGETHER").upper() == "TOGETHER":
        return together_api(messages)
    else:
        return open_api(messages)

def open_api(messages):
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return response.json()["choices"][0]["message"]["content"]

def together_api(messages):
    client = Together()

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages= messages
    )

    return response.choices[0].message.content
    

@app.get("/health")
async def health_check():
    return {"status": "ok"}