#!/bin/bash

# Garante permissão de execução
chmod +x start.sh

# mkdir -p models-empty

# Inicia apenas o servidor NLU
rasa run --enable-api --port 10000