#!/bin/bash

mkdir -p dados-de-execucao
ARQV_SAIDA="dados-de-execucao/namespaces_brutos.txt"

echo "Iniciando a Parte B - Coleta de namespaces"
> "$ARQV_SAIDA"

# Inicia dois contêineres independentes
echo "Iniciando contêineres..."
docker run -d --name cont_A python:3.12-slim sleep infinity > /dev/null
docker run -d --name cont_B python:3.12-slim sleep infinity > /dev/null

sleep 2

# Coleta PIDs e Handles
for NOME in cont_A cont_B; do
    echo "Coletando dados do contêiner: $NOME" | tee -a "$ARQV_SAIDA"

    echo -n "PID no host (docker inspect): " | tee -a "$ARQV_SAIDA"
    docker inspect --format '{{.State.Pid}}' $NOME | tee -a "$ARQV_SAIDA"

    echo -n "Processo PID 1 interno: " | tee -a "$ARQV_SAIDA"
    docker exec $NOME sh -c 'cat /proc/1/comm' | tee -a "$ARQV_SAIDA"

    echo -n "Handle NS PID: " | tee -a "$ARQV_SAIDA"
    docker exec $NOME readlink /proc/1/ns/pid | tee -a "$ARQV_SAIDA"

    echo -n "Handle NS MNT: " | tee -a "$ARQV_SAIDA"
    docker exec $NOME readlink /proc/1/ns/mnt | tee -a "$ARQV_SAIDA"

    echo -n "Handle NS NET: " | tee -a "$ARQV_SAIDA"
    docker exec $NOME readlink /proc/1/ns/net | tee -a "$ARQV_SAIDA"

    echo "" | tee -a "$ARQV_SAIDA"
done

# Limpa o ambiente
echo "Encerrando e removendo os contêineres..."
docker stop cont_A cont_B > /dev/null
docker rm cont_A cont_B > /dev/null

echo "Coleta concluída. Evidências salvas em '$ARQV_SAIDA'."