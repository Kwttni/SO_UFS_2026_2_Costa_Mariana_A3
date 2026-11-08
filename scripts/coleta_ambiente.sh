#!/bin/bash

#Script de coleta de dados do ambiente e Docker
mkdir -p dados-de-execucao
ARQV_SAIDA_AMB='dados-de-execucao/ambiente.txt'
ARQV_SAIDA_DK='dados-de-execucao/docker.txt'

echo "Iniciando a Parte A - Ambiente e contêiner"
> "$ARQV_SAIDA_AMB"
> "$ARQV_SAIDA_DK"

echo "Coletando dados do ambiente..."
# Coleta dados do host (kernel, distribuição e CPUs lógicas)
{
    echo "Informações do kernel (uname -a):"
    uname -a
    echo -e "\nSistema operacional (/etc/os-release):"
    cat /etc/os-release
    echo -e "\nCPUs lógicas (nproc):"
    nproc
} > "$ARQV_SAIDA_AMB"

echo "Coletando dados do Docker..."
# Coleta versão do Docker e configuração de cgroups
{
    echo "Versão do Docker:"
    docker version
    echo -e "\nInformações de cgroup (driver e versão):"
    docker info --format 'Cgroup={{.CgroupVersion}} Driver={{.CgroupDriver}}'
} > "$ARQV_SAIDA_DK"

echo "Coleta concluída. Arquivos salvos em '$ARQV_SAIDA_AMB' e '$ARQV_SAIDA_DK'."