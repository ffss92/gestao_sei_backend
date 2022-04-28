#!/bin/bash

# Executa as migrações no banco de dados
echo "[INFO] Executando migrações no banco de dados"
alembic upgrade head

# Insere dados iniciais no banco de dados
echo "[INFO] Executando scripts de pré-inicialização"
python pre_start.py


# Inicia o App
echo "[INFO] Iniciando o servidor"
if [ "$ENVIRONMENT" == "production" ];
then
  uvicorn api.main:app --host 0.0.0.0 --port "${SERVICE_PORT}"
else
  uvicorn api.main:app --host 0.0.0.0 --port "${SERVICE_PORT}" --reload
fi