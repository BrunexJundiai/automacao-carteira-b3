# 🏗️ Arquitetura de Dados e Automação - Sniper B3 (V4.0 Master AI)

O projeto adota uma arquitetura *Single Source of Truth* (Fonte Única da Verdade), consolidando os três módulos independentes (Radar, Dashboard e Aportes) em um fluxo de execução centralizado e altamente performático.

## 1. Pipeline Otimizado (ETL Central)
* **Extração Única (Zero Redundância):** O download do histórico de 180 dias de cotações (`yf.download`) é realizado estritamente **uma única vez** no início do ciclo. Os dados são estruturados em um *DataFrame* massivo e distribuídos na memória (RAM) para os três módulos subsequentes. Isso elimina chamadas de rede redundantes, previne o bloqueio de IP (*Rate Limit*) pelas APIs externas e acelera exponencialmente a execução.
* **Cache Inteligente:** Implementação de trava de concorrência (`threads=False`) no download de múltiplos *tickers* para evitar o erro `OperationalError('database is locked')` no banco SQLite interno gerido pela biblioteca *requests_cache*.

---

## 2. Separação Institucional de Relatórios (PDF Multi-Page)
O motor de visualização gera relatórios estratégicos respeitando a natureza de cada classe de ativo:
* **Lâmina Core (Equities):** Renderiza o Mapa Global de Alocação (*Treemap* via biblioteca `squarify`), gráficos de barras horizontais de rentabilidade (B3) e cronogramas preditivos de dividendos.
* **Lâmina Satélite (Cripto):** Aplica conceitos gráficos de *Trend Following*. Cruza o histórico de preços com uma Média Móvel Simples de 30 dias (SMA30), utilizando preenchimento de área (`fill_between`) vermelho/laranja para evidenciar visualmente o rompimento de suportes e resistências estruturais do Bitcoin, além de isolar os KPIs da operação.
* **Lâmina de Aportes:** Gera o *DRE Analítico* e os gráficos de distância da meta percentual da carteira.

---

## 3. Containerização e Orquestração (Docker)
Na Versão 4.0, a dependência de ambientes locais e do Agendador de Tarefas do Windows foi substituída por uma arquitetura nativa de *Containers*.
* **Isolamento de Ambiente:** Utilização da imagem `python:3.11-slim`, garantindo que dependências complexas de IA (LangChain, Groq) e visualização de dados (Seaborn, Matplotlib) rodem sem conflitos de sistema operacional (Windows/Linux/Mac).
* **Timezone Controlado:** Configuração explícita do fuso horário (`ENV TZ=America/Sao_Paulo`) diretamente no `Dockerfile` para garantir o funcionamento preciso da "Trava Sistêmica" comercial da B3, independente do fuso horário do servidor hospedeiro (Nuvem ou Local).
* **Automação Contínua (Shell Loop):** O container implementa um *Shell Loop* infinito (`while true; do ... sleep 1800; done`) como orquestrador nativo leve. Ele aciona o fluxo Python completo, aguarda 30 minutos em suspensão, e reinicia o ciclo de ETL ininterruptamente, substituindo a necessidade de orquestradores pesados como Apache Airflow para este escopo.