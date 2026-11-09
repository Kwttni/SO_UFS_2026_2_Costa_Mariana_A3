import sys
import time
import resource

def executar_carga(quant_trabalho):
    tempo_inicio_real = time.time()
    tempo_inicio_cpu = time.process_time()

    # Determinismo: calcula o quadrado de cada número e soma tudo
    soma_total = sum(i * i for i in range(quant_trabalho))

    tempo_fim_cpu = time.process_time()
    tempo_fim_real = time.time()

    tempo_real = tempo_fim_real - tempo_inicio_real
    tempo_cpu = tempo_fim_cpu - tempo_inicio_cpu

    velocidade = quant_trabalho / tempo_real if tempo_cpu > 0 else 0

    # Captura do pico de memória RAM (RSS) do próprio processo (em KB no Linux)
    ram_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    print(f"Status: Concluido")
    print(f"Trabalho: {quant_trabalho}")
    print(f"Checksum: {soma_total}")
    print(f"Wall_time_s: {tempo_real:.4f}")
    print(f"CPU_time_s: {tempo_cpu:.4f}")
    print(f"Trabalho_por_s: {velocidade:.2f}")
    print(f"Process_RSS_kb: {ram_kb}")

if __name__ == '__main__':
    quant = int(sys.argv[1]) if len(sys.argv) > 1 else 20000000
    executar_carga(quant)