#### 9. Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada neste projeto para revisar e melhorar a organização e a escrita dos textos do relatório. Também foi utilizada para esclarecer dúvidas sobre os conceitos abordados na atividade, auxiliar na compreensão de erros apresentados no terminal e apoiar a criação do roteiro de apresentação e dos slides.

O ChatGPT foi utilizado para a revisão dos textos e a elaboração do roteiro de apresentação. Já o Gemini foi utilizado para esclarecer dúvidas sobre os conceitos, auxiliar na resolução de erros e orientar a organização da estrutura do repositório.

**Prompt 1:**

> Verifique o que está gerando erro de execução:
>
> Código `scripts/carga_cpu.py`:
>
> **[Código]**
>
> Código `scripts/executa_parte_c.sh`:
>
> **[Código]**
>
> Código `scripts/resumo.py`:
>
> **[Código]**

**Problemas identificados:**

Os erros encontrados estavam relacionados a variáveis com nomes incorretos, tamanhos diferentes dos limitadores e problemas na lógica de separação dos blocos no arquivo `resumo.py`.

Todos os problemas estavam no script `resumo.py` e foram corrigidos com base nas orientações fornecidas pela IA.

**Prompt 2:**

> Analise o relatório anexado e verifique se atende a todos os requisitos solicitados no PDF da atividade. Caso esteja adequado, gere um README conforme o pedido na atividade, utilizando o roteiro e os seguintes comandos de execução:
>
> **Parte A – Ambiente e contêiner:**
>
> Gerados via scripts:
>
> ```bash
> chmod +x scripts/coleta_ambiente.sh
> ./scripts/coleta_ambiente.sh
> ```
>
> Os dados gerados podem ser verificados em:
>
> - `dados-de-execucao/ambiente.txt`
> - `dados-de-execucao/docker.txt`
>
> **Parte B – Evidências de namespaces:**
>
> Gerados via script:
>
> ```bash
> chmod +x scripts/coleta_namespaces.sh
> ./scripts/coleta_namespaces.sh
> ```
>
> Os dados gerados podem ser verificados em:
>
> - `dados-de-execucao/namespaces_brutos.txt`
>
> **Parte C – Experimento de cgroups:**
>
> Gerados via scripts:
>
> ```bash
> chmod +x scripts/executa_parte_c.sh
> ./scripts/executa_parte_c.sh
> python scripts/resumo.py
> ```
>
> Os dados gerados podem ser verificados em:
>
> - `dados-de-execucao/grafico_desempenho.png`
> - `dados-de-execucao/resultados_completos.txt`
> - `dados-de-execucao/tabela_resultados.txt`
>
> **Parte D – Mount e menor privilégio:**
>
> Gerados via scripts:
>
> ```bash
> chmod +x scripts/executa_parte_d.sh
> ./scripts/executa_parte_d.sh
> ```
>
> Os dados gerados podem ser verificados em:
>
> - `dados-de-execucao/resultado_parte_d.txt`
> - `dados_demo/texto.txt`

**Prompt 3:**

> Com base no relatório em anexo, estruture uma apresentação que atenda aos requisitos informados e apresente as informações necessárias. O foco principal deve ser os experimentos e seus resultados. As imagens e tabelas utilizadas na apresentação serão as mesmas presentes no relatório. Não gere o arquivo de apresentação, apenas os tópicos e o que deve ser abordado em cada um deles.