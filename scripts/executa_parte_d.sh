#!/bin/bash

mkdir -p dados_demo
printf '%s\n' 'Documento sintetico' > dados_demo/texto.txt

mkdir -p dados-de-execucao
ARQV_SAIDA="dados-de-execucao/resultado_parte_d.txt"
> "$ARQV_SAIDA"

echo "Iniciando Experimento - Parte D (Mount e Menor Privilegio)" | tee -a "$ARQV_SAIDA"
echo "Data/Hora: $(date)" | tee -a "$ARQV_SAIDA"
echo "---------------------------------------------" | tee -a "$ARQV_SAIDA"

docker run --rm --name teste_privilegios \
    --user 1000:1000 \
    --cap-drop=ALL \
    --security-opt=no-new-privileges:true \
    -v "$PWD/dados_sinteticos:/dados:ro,Z" \
    python:3.12-slim \
    bash -c "
        echo '* Verificando Identidade (Menor Privilegio):'
        id

        echo -e '\n* Tentativa 1: Leitura (Espera-se SUCESSO):'
        cat /dados/texto_sintetico.txt

        echo -e '\n* Tentativa 2: Escrita (Espera-se FALHA - Read-only file system):'
        touch /dados/novo_arquivo.txt || echo '=> Negação de escrita registrada com sucesso.'

        echo -e '\n* Verificando Capabilities (CapBnd deve ser zerado):'
        grep CapBnd /proc/self/status
    " 2>&1 | tee -a "$ARQV_SAIDA"

echo "---------------------------------------------" | tee -a "$ARQV_SAIDA"
echo "Experimento concluído. Dados salvos em $ARQV_SAIDA"