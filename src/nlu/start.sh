#!/bin/bash

# Garante permissão de execução
chmod +x start.sh

# Inicia apenas o servidor NLU
rasa run --enable-api --model models --port 10000