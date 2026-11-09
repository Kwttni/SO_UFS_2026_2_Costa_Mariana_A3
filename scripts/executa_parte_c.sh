#!/bin/bash

mkdir -p dados-de-execucao
ARQV="dados-de-execucao/resultados_completos.txt"
> "$ARQV"
export QUANT_TRABALHO=${QUANT_TRABALHO:-20000000}

echo "Iniciando Experimentos (C1 e C2 intercalados) com $QUANT_TRABALHO iteracoes..." | tee -a "$ARQV"
echo "Data/Hora: $(date)" >> "$ARQV"

for REPETICAO in 1 2 3; do
    for CENARIO in "C1" "C2"; do
        if [ "$CENARIO" == "C1" ]; then
            LIMITE_CPU="0.5" # C1 recebe meia CPU
        else
            LIMITE_CPU="1.0" # C2 recebe uma CPU inteira
        fi

        echo -e "\n---------------------------------------------" | tee -a "$ARQV"
        echo "Execução: Cenário $CENARIO - Repetição $REPETICAO" | tee -a "$ARQV"

        docker run --rm --name "teste_cpu_${CENARIO}_${REPETICAO}" \
            --cpus="${LIMITE_CPU}" \
            --memory="256m" --memory-swap="256m" \
            --pids-limit="64" \
            -v "$PWD/scripts:/app:Z" -w /app \
            python:3.12-slim \
            bash -c "
                echo '* Limites cgroup efetuados'
                cat /sys/fs/cgroup/cpu.max | awk '{print \"cpu.max: \" \$0}'
                cat /sys/fs/cgroup/memory.max | awk '{print \"memory.max: \" \$0}'
                cat /sys/fs/cgroup/pids.max | awk '{print \"pids.max: \" \$0}'

                echo -e '\n* Metricas do Cgroup antes do processamento'
                cat /sys/fs/cgroup/cpu.stat | grep -E 'usage_usec|nr_throttled|throttled_usec' | awk '{print \"antes_\" \$1 \" \" \$2}'

                echo -e '\n* Processamento'
                python carga_cpu.py $QUANT_TRABALHO

                echo -e '\n* Metricas do Cgroup depois do processamento'
                cat /sys/fs/cgroup/cpu.stat | grep -E 'usage_usec|nr_throttled|throttled_usec' | awk '{print \"depois_\" \$1 \" \" \$2}'
                cat /sys/fs/cgroup/memory.current | awk '{print \"memory.current: \" \$0}'
                cat /sys/fs/cgroup/memory.peak 2>/dev/null | awk '{print \"memory.peak: \" \$0}' || echo 'memory.peak: nao_suportado'
            " 2>&1 | tee -a "$ARQV"

        sleep 2
    done
done

echo -e "\nExecucoes concluidas. Dados salvos em $ARQV."