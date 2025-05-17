#!/bin/bash

# Garante permissão de execução
chmod +x start.sh

# Inicia apenas o servidor da central
uvicorn app:app --reload --host 0.0.0.0 --port 8000