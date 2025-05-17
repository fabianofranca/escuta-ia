import requests

# Endpoint da NLU do Rasa
RASA_NLU_URL = "http://localhost:5005/model/parse"

# Frases divididas por intenção esperada (para conferência manual)
testes = {
    "relato_solidao": [
        "ninguém liga pra mim de verdade",
        "tô sempre sobrando",
        "todo mundo tem alguém, menos eu",
        "me sinto um nada, sério",
        "ninguém me chama pra nada, acho que nem lembram que existo"
    ],
    "relato_crise": [
        "acho que tô pirando",
        "minha mente tá um caos",
        "não consigo respirar direito, parece que vou explodir",
        "tô surtando e ninguém percebe",
        "minha cabeça não para e eu não sei o que fazer"
    ],
    "ideacao_suicida": [
        "já pensei em sumir e nunca mais voltar",
        "se eu desaparecesse, ninguém ia notar",
        "às vezes queria dormir pra sempre",
        "cansei de fingir que tá tudo bem",
        "tenho pensado em acabar com tudo, de verdade"
    ],
    "relato_tristeza": [
        "tô mal e nem sei explicar",
        "nada mais tem graça",
        "eu tô me sentindo vazio",
        "parece que nada importa",
        "tô triste o tempo todo, até quando rio"
    ],
    "autolesao": [
        "me machuquei de novo, mas ninguém vê",
        "às vezes me corto pra aliviar",
        "só sinto alguma coisa quando me machuco",
        "bati em mim mesmo hoje",
        "me arranhei todo sem nem pensar"
    ]
}

print("\n🧪 Testando frases com o modelo NLU (modo adolescente):\n")

for intencao, frases in testes.items():
    print(f"### Esperado: {intencao}")
    for frase in frases:
        response = requests.post(RASA_NLU_URL, json={"text": frase})
        if response.status_code == 200:
            resultado = response.json()
            intent_detectada = resultado.get("intent", {}).get("name")
            confianca = resultado.get("intent", {}).get("confidence", 0)
            print(f"  ↪ '{frase}' → {intent_detectada} (confiança: {confianca:.2f})")
        else:
            print(f"  ⚠ Erro ao enviar frase: '{frase}'")
    print()
