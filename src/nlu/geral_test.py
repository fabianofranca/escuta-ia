import requests

RASA_NLU_URL = "http://localhost:5005/model/parse"

frases_por_intencao = {
    "saudacao": [
        "oi",
        "tem alguém aí?",
        "bom dia, posso falar?"
    ],
    "pedir_ajuda": [
        "preciso conversar",
        "pode me escutar um pouco?",
        "estou no limite"
    ],
    "relato_tristeza": [
        "me sinto um peso na vida das pessoas",
        "tenho chorado sem parar",
        "tá tudo escuro dentro de mim"
    ],
    "relato_ansiedade": [
        "meu coração não para de acelerar",
        "estou tremendo e não sei por quê",
        "estou em pânico"
    ],
    "relato_perda": [
        "perdi minha mãe esse ano",
        "estou de luto desde que meu pai se foi",
        "desde a morte da minha avó não me recuperei",
        "minha esposa me deixou",
    ],
    "relato_solidao": [
        "me sinto sozinho mesmo rodeado de pessoas",
        "ninguém me procura mais",
        "é como se eu não existisse",
        "ninguém me nota mais",
        "me sinto invisível",
        "estou sozinho mesmo com gente por perto",
        "parece que não faço falta pra ninguém"
    ],
    "relato_crise": [
        "estou surtando",
        "minha cabeça vai explodir",
        "não aguento mais",
        "não estou aguentando mais",
        "estou completamente fora de mim",
        "parece que estou caindo num buraco",
        "estou entrando em colapso"
    ],
    "ideacao_suicida": [
        "pensei em acabar com tudo",
        "só queria dormir e nunca mais acordar",
        "ninguém sentiria minha falta se eu sumisse",
        "queria dormir e nunca mais acordar",
        "pensei em dar fim a tudo",
        "minha vida não tem mais sentido",
        "estou cansado de viver",
        "talvez o mundo fique melhor sem mim"
    ],
    "autolesao": [
        "me machuquei de novo",
        "cortei meu braço ontem",
        "é a única dor que alivia"
    ],
    "informar_nome": [
        "meu nome é João",
        "pode me chamar de Ana",
        "sou o Carlos"
    ],
    "informar_tempo": [
        "isso começou ontem",
        "me sinto assim há duas semanas",
        "desde segunda estou assim"
    ],
    "despedida": [
        "obrigado por me ouvir",
        "vou descansar agora",
        "até logo"
    ]
}

print("\n🧪 Testando frases com linguagem mista, informal e emocional:\n")

for intencao, frases in frases_por_intencao.items():
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
