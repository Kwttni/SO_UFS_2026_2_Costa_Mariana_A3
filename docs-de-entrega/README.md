# Atividade 3 – Sistemas Operacionais: Virtualização, Contêineres, Namespaces e Cgroups

**Discente:** Mariana Silva Costa  
**Repositório:** https://github.com/Kwttni/SO_UFS_2026_2_Costa_Mariana_A3
**Vídeo da apresentação:** https://drive.google.com/drive/folders/1D65GEG9HO9WvUHmQ9lEIRy-I1tJOuQ7e?usp=sharing

## Descrição

Este repositório contém os scripts e arquivos de dados utilizados no laboratório sobre isolamento de processos e controle de recursos em contêineres Docker (*namespaces* e *cgroups*).

O objetivo é demonstrar, de forma prática e reprodutível, como o kernel do Linux realiza o isolamento de processos, controla o uso de recursos como CPU e memória e restringe permissões de acesso.

---

## Como executar os experimentos

Os comandos abaixo devem ser executados na raiz do repositório para reproduzir cada etapa do laboratório.

### Parte A – Ambiente e contêiner

Realiza a coleta de informações do sistema Host, incluindo hardware, versão do kernel, versão do Docker e suporte a *cgroups v2*.

**Execução:**

```bash
chmod +x scripts/coleta_ambiente.sh
./scripts/coleta_ambiente.sh
```

**Arquivos gerados:**

- `dados-de-execucao/ambiente.txt`
- `dados-de-execucao/docker.txt`

### Parte B – Evidências de namespaces

Cria dois contêineres e coleta os identificadores dos *namespaces* (`pid`, `mnt` e `net`) para verificar o isolamento de processos, montagens e redes.

**Execução:**

```bash
chmod +x scripts/coleta_namespaces.sh
./scripts/coleta_namespaces.sh
```

**Arquivo gerado:**

- `dados-de-execucao/namespaces_brutos.txt`

### Parte C – Experimento de cgroups

Executa uma carga de trabalho com limites diferentes de CPU (0,5 CPU e 1,0 CPU) e coleta métricas de tempo, uso de CPU, *throttling* e memória.

**Execução:**

```bash
chmod +x scripts/executa_parte_c.sh
./scripts/executa_parte_c.sh
python scripts/resumo.py
```

**Arquivos gerados:**

- `dados-de-execucao/grafico_desempenho.png`
- `dados-de-execucao/resultados_completos.txt`
- `dados-de-execucao/tabela_resultados.txt`

### Parte D – Mount e menor privilégio

Verifica o isolamento do sistema de arquivos e as restrições de acesso por meio da montagem de um volume no modo somente leitura (`:ro`). Também verifica as permissões do usuário, as restrições de *Capabilities* e a execução sem privilégios de administrador (*root*).

**Execução:**

```bash
chmod +x scripts/executa_parte_d.sh
./scripts/executa_parte_d.sh
```

**Arquivos gerados:**

- `dados-de-execucao/resultado_parte_d.txt`
- `dados_demo/texto.txt`