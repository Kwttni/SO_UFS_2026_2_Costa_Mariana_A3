import re
import csv
import statistics
import os
import matplotlib.pyplot as plt

TEXTO = "dados-de-execucao/resultados_completos.txt"
TABELA = "dados-de-execucao/tabela_resultados.csv"
GRAFICO = "dados-de-execucao/grafico_desempenho.png"


def extrair_dados_do_texto():
    resultados = []

    with open(TEXTO, "r") as arqv:
        texto = arqv.read()

    blocos = texto.split("---------------------------------------------")[1:]

    for bloco in blocos:
        encontrado = re.search(r"Cenário (C[12]) - Repetição (\d)", bloco)
        if not encontrado:
            continue

        cenario, repeticao = encontrado.groups()

        def buscar_valor(padrao_busca, texto, valor_padrao="N/A"):
            res_busca = re.search(padrao_busca, texto)
            return res_busca.group(1) if res_busca else valor_padrao

        velocidade = float(buscar_valor(r"Trabalho_por_s: ([\d\.]+)", bloco, 0))
        tempo_real = float(buscar_valor(r"Wall_time_s: ([\d\.]+)", bloco, 0))
        tempo_cpu = float(buscar_valor(r"CPU_time_s: ([\d\.]+)", bloco, 0))

        uso_antes = int(buscar_valor(r"antes_usage_usec (\d+)", bloco, 0))
        uso_depois = int(buscar_valor(r"depois_usage_usec (\d+)", bloco, 0))
        cortes_antes = int(buscar_valor(r"antes_nr_throttled (\d+)", bloco, 0))
        cortes_depois = int(buscar_valor(r"depois_nr_throttled (\d+)", bloco, 0))
        tempo_corte_antes = int(buscar_valor(r"antes_throttled_usec (\d+)", bloco, 0))
        tempo_corte_depois = int(buscar_valor(r"depois_throttled_usec (\d+)", bloco, 0))

        total_cpu = uso_depois - uso_antes
        total_cortes = cortes_depois - cortes_antes
        tempo_total_cortado = tempo_corte_depois - tempo_corte_antes

        limite_cpu = buscar_valor(r"cpu.max: (.+)", bloco)
        ram_processo = buscar_valor(r"Process_RSS_kb: (\d+)", bloco)
        mem_atual = buscar_valor(r"memory.current: (\d+)", bloco)
        pico_mem = buscar_valor(r"memory.peak: (\d+)", bloco)

        resultados.append({
            "Cenario": cenario,
            "Repeticao": int(repeticao),
            "Tempo_Relogio(s)": tempo_real,
            "Tempo_CPU(s)": tempo_cpu,
            "Velocidade(Trab/s)": velocidade,
            "Limite_CPU": limite_cpu,
            "Uso_Extra_CPU": total_cpu,
            "Cortes_CPU(qtd)": total_cortes,
            "Tempo_Cortado_CPU": tempo_total_cortado,
            "RAM_Processo(KB)": ram_processo,
            "Memoria_Atual(bytes)": mem_atual,
            "Pico_Memoria(bytes)": pico_mem
        })
    return resultados

    return resultados


def main():
    if not os.path.exists(TEXTO):
        print(f"Erro: O arquivo {TEXTO} não foi encontrado.")
        return

    dados_consolidados = extrair_dados_do_texto()

    if dados_consolidados:
        with open(TABELA, "w", newline='') as arq_csv:
            w_csv = csv.DictWriter(arq_csv, fieldnames=dados_consolidados[0].keys())
            w_csv.writeheader()
            w_csv.writerows(dados_consolidados)
        print(f"Tabela salva em: {TABELA}")

    print("\nResumo - Velocidade (Mediana e Variação):")

    cenarios = ["C1", "C2"]
    medianas = []

    for cenario in cenarios:
        velocidades = [linha["Velocidade(Trab/s)"] for linha in dados_consolidados if linha["Cenario"] == cenario]

        if velocidades:
            mediana = statistics.median(velocidades)
            valor_max = max(velocidades)
            valor_min = min(velocidades)
            variacao = valor_max - valor_min

            medianas.append(mediana)

            print(f"Cenário {cenario}: Mediana = {mediana:.2f} Trabalhos/s | Variação = {variacao:.2f} Trabalhos/s")

    # Gráfico comparativo
    if len(medianas) == 2:
        fig, ax = plt.subplots(figsize=(10, 6))

        # Cálculo das margens de erro para C1 e C2
        margem_erro = [
            [
                medianas[i] - min(
                    linha["Velocidade(Trab/s)"]
                    for linha in dados_consolidados
                    if linha["Cenario"] == cenarios[i]
                ),
                max(
                    linha["Velocidade(Trab/s)"]
                    for linha in dados_consolidados
                    if linha["Cenario"] == cenarios[i]
                ) - medianas[i]
            ]
            for i in range(2)
        ]
        margem_erro = list(map(list, zip(*margem_erro)))

        # Configuração visual
        cores = ["#4776A8", "#269B80"]
        largura_barra = 0.55
        posicoes = range(len(cenarios))

        barras = ax.bar(
            posicoes,
            medianas,
            width=largura_barra,
            color=cores,
            alpha=0.9,
            zorder=3
        )

        # Títulos e eixos
        ax.set_title(
            "Desempenho de CPU por Cenário",
            fontsize=17,
            fontweight="bold",
            color="#263445",
            pad=20
        )

        ax.text(
            0.5, 1.02,
            "Mediana da velocidade e variação entre as repetições",
            transform=ax.transAxes,
            ha="center",
            fontsize=10,
            color="#737D89"
        )

        ax.set_ylabel(
            "Velocidade (Trabalhos por Segundo)",
            fontsize=11,
            labelpad=12,
            color="#404A56"
        )

        ax.set_xticks(list(posicoes))
        ax.set_xticklabels(
            cenarios,
            fontsize=11,
            fontweight="bold",
            color="#404A56"
        )

        # Grade e aparência dos eixos
        ax.grid(
            axis="y",
            linestyle="--",
            linewidth=0.8,
            alpha=0.35,
            color="#AAB3BD",
            zorder=0
        )

        ax.set_axisbelow(True)
        ax.set_facecolor("#FFFFFF")
        fig.patch.set_facecolor("#FFFFFF")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_color("#D9DEE5")

        ax.tick_params(axis="y", length=0, labelcolor="#596575")
        ax.tick_params(axis="x", length=0, pad=12)

        # Ajuste do limite superior
        maior_valor = max(
            medianas[i] + margem_erro[1][i]
            for i in range(2)
        )
        ax.set_ylim(0, maior_valor * 1.20)

        # Valores das medianas
        for barra, valor in zip(barras, medianas):
            altura = barra.get_height()

            ax.text(
                barra.get_x() + barra.get_width() / 2,
                altura * 0.5,
                f"{valor:,.0f}".replace(",", "."),
                ha="center",
                va="center",
                fontsize=13,
                fontweight="bold",
                color="white"
            )

        # Identificação da quantidade de repetições
        ax.text(
            0.99, 0.98,
            "3 repetições por cenário",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=9,
            color="#737D89"
        )

        plt.tight_layout()
        plt.savefig(GRAFICO, dpi=300, bbox_inches="tight", facecolor="white")
        plt.close()

        print(f"Gráfico salvo em: {GRAFICO}")


if __name__ == "__main__":
    main()