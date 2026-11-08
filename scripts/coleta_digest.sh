#!/bin/bash

mkdir -p dados-de-execucao
ARQV_SAIDA="dados-de-execucao/digest.txt"

echo "Extraindo o digest da imagem python:3.12-slim..."
> "$ARQV_SAIDA"

export IMAGEM_LAB="$(docker image inspect --format '{{index .RepoDigests 0}}' python:3.12-slim)"

printf '%s\n' "$IMAGEM_LAB" > "$ARQV_SAIDA"

echo "Coleta concluída. Digest salvo em '$ARQV_SAIDA'"