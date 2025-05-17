import requests

RASA_NLU_URL = "http://localhost:5005/model/parse"

# Frases com linguagem informal, erros de digitação e comunicação limitada
frases = [
    "t ninguem pra fal",
    "to ruimm hj",
    "keria dormi e n acorda",
    "sofro dmais mais ngm ve",
    "pq doi tanto assim",
    "me senti um peso hj",
    "tenho vtd d sumi",
    "meu coraçao ta doendo",
    "axo q to bugado da kbça",
    "ninguem presta atença em mim",
    "so qria algeum pra ouvi",
    "nd fz sentido mds",
    "cansadao da vida viu",
    "ta td estranho dentro d mim",
    "ja nem sei oq q sinto mas"
]

print("\n🧪 Testando frases com erros e linguagem informal:\n")

for frase in frases:
    response = requests.post(RASA_NLU_URL, json={"text": frase})
    if response.status_code == 200:
        resultado = response.json()
        intent_detectada = resultado.get("intent", {}).get("name")
        confianca = resultado.get("intent", {}).get("confidence", 0)
        print(f"  ↪ '{frase}' → {intent_detectada} (confiança: {confianca:.2f})")
    else:
        print(f"  ⚠ Erro ao enviar frase: '{frase}'")
