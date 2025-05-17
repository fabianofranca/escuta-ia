#!/bin/bash

# Ativa o ambiente virtual (ajuste o caminho se necessário)
echo "[1/4] Ativando ambiente virtual..."
source .venv/bin/activate || source .venv/Scripts/activate

# Treina o modelo
echo "[2/4] Treinando modelo com NLU + config.yml..."
rasa train --debug

# Executa testes NLU (validação das intenções)
echo "[3/4] Testando modelo com dados de teste..."
rasa test nlu --out results/nlu

# Exibe resultado resumido dos testes
echo "[4/4] Resultados resumidos:"
cat results/nlu/intent_report.json | jq

# Dica final
echo "/nPronto! Para testar interativamente, use:/n  rasa shell --nlu"
