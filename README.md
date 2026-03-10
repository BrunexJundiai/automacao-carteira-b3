# 📈 Sniper B3: Ecossistema Master Quantitativo (V3.0)

Um ecossistema avançado de **Engenharia de Dados**, **Decisão Estratégica** e **Automação Quantitativa** construído em Python. O projeto funciona como um motor de *Hedge Fund* particular: automatiza o monitoramento tático de ativos, o rebalanceamento de carteira e utiliza modelos de **Regressão Linear de 180 dias** para projetar tendências de curto prazo na B3.

## 🎯 O Problema
Investidores enfrentam dificuldades em manter a disciplina emocional em mercados voláteis, muitas vezes falhando em identificar o *timing* técnico ideal para aportes, tentando "pegar facas caindo" ou mantendo em carteira ativos que perderam seus fundamentos de tendência. Este projeto resolve essa dor através de algoritmos frios, matemáticos e precisos.

## 💡 A Solução (Arquitetura Master)
Na versão 3.0, o sistema evoluiu de scripts isolados para um **Ecossistema Master Unificado**. Utilizando conceitos sólidos de **ETL (Extract, Transform, Load)** e **Análise Preditiva**, a arquitetura agora opera com *Single Source of Truth* (Fonte Única da Verdade), otimizando o consumo de APIs e garantindo sincronia absoluta:

1. **Extract (Extração Única):** Consumo centralizado de dados via API do Google Sheets (histórico de operações de compra e venda) e YFinance (cotações e histórico de 6 meses) executado apenas uma vez por ciclo, evitando bloqueios de API.
2. **Transform (Matemática e Filtros):** Processamento de Saldo Ajustado (abatendo vendas reais), cálculo de Preço Médio histórico, rentabilidade e modelagem estatística de tendência (Numpy Polyfit).
3. **Load/Analytics (A Tríade Sniper):** O pipeline alimenta três módulos de decisão simultâneos e envia dashboards executivos em PDF e alertas táticos via Telegram.

---

## ⚙️ A Tríade de Decisão (Módulos do Sistema)

### 1. Radar Sniper (Operacional e Tático)
Um robô que avalia o mercado em busca de exaustão de preço.
* **Memória de PM Histórico:** Se um ativo for totalmente vendido (lucro realizado), o sistema guarda o seu último Preço Médio. Se a ação despencar irracionalmente no futuro, ele emite um alerta exclusivo de **🔥 RECOMPRA SNIPER**.
* **Trava de Segurança:** Só sugere vendas táticas para ativos que você *realmente* possui em custódia (Saldo > 0).

### 2. Dashboard Estratégico (Visão Executiva)
Visão consolidada da saúde do patrimônio e projeções de curto prazo.
* **Filtro de Realidade:** Ativos zerados são sumariamente excluídos do cálculo de patrimônio, evitando projeções de dividendos fantasmas.
* **Ranking Preditivo:** Elege o ativo da carteira com o maior potencial de alta (Upside) para os próximos 30 dias.

### 3. Gestão de Fluxo de Caixa (Aportes Mensais)
Inteligência de rebalanceamento cruzada com *Trend Following*.
* **Filtro Mestre (A Trava da Faca Caindo):** O algoritmo de aporte bloqueia sumariamente qualquer compra de ativo que esteja com **Viés Preditivo Negativo**, independentemente de quão longe a ação esteja da sua meta percentual de alocação na carteira. 

---

## 📊 Regras de Negócio e Lógica Analítica

| Gatilho / Módulo | Regra Matemática Aplicada | Objetivo Estratégico |
| :--- | :--- | :--- |
| **Proteção de Horário** | `Hora < 10h` ou `Hora >= 18h` = Bloqueado | Isolar o sistema da volatilidade de leilões de abertura/fechamento da B3. |
| **Compra Sniper** | `Preço < (PM * 0.85)` & `RSI <= 25` | Capturar pânico irracional do mercado com uma margem de segurança de 15%. |
| **Venda Tática** | `RSI >= 75` ou (`Lucro > 5%` & `Viés < -10%`) | Realizar lucro na euforia ou proteger capital em caso de inversão estrutural de tendência. |
| **Aporte Seguro** | `Viés > 0` & `Distância Meta < -2.0%` | Garantir que o capital novo só compre ativos descontados que estejam em tendência de alta. |
| **Bloqueio de Aporte** | `Viés Preditivo < 0` | Marcar a ação como **BLOQUEADO - FACA CAINDO**. Proteger o fluxo de caixa. |
| **Viés Preditivo (30d)** | Regressão Linear Simples (Últimos 180 dias) | Projetar a tendência estatística eliminando o "ruído" diário do mercado. |

---

## 🖥️ Evidências e Relatórios Gerados

### 1. Radar Sniper (Alertas Intraday)
Monitoramento em tempo real com disparo de sinais de entrada, realização de lucro e status do servidor.
| Compra / Recompra | Realização de Lucro | Zona Neutra |
| :---: | :---: | :---: |
| ![Compra](img/alerta_compra.png) | ![Venda](img/alerta_venda.png) | ![Neutro](img/alerta_neutro.png) |

### 2. Dashboard Estratégico (Visão de Patrimônio)
Consolidação do ecossistema com foco em performance, dividendos projetados e regressão linear.
| Insight Preditivo (Telegram) | Relatório Executivo (PDF) |
| :---: | :---: |
| ![Reporte Preditivo](img/reporte_preditivo.png) | ![Gráficos 1 e 2](img/graficos_1_2.png)<br><br>![Gráficos 3 e 4](img/graficos_3_4.png) |

### 3. Aportes Mensais (Fluxo de Caixa)
Cruzamento da distância da meta de alocação com o viés preditivo de tendência.
| Direcionamento (Telegram) | DRE Analítico e Alocação (PDF) |
| :---: | :---: |
| ![Reporte Mensal](img/reporte_mensal.png) | ![Estratégia de Alocação](img/estrategia_alocacao.png)<br><br>![Distância da Meta](img/distancia_meta_aporte.png)<br><br>![DRE Analítico](img/DRE_analitico.png) |

> 💡 **Insight:** A nova arquitetura garante que a meta engessada de portfólio (ex: 10% por ação) seja apenas um critério de desempate. O modelo quantitativo, focado em dados de tendência, é sempre soberano.

---

## 🛠 Tecnologias Utilizadas

* **Python / Pandas / Numpy:** Motor central para limpeza de dados (ETL) e cálculos preditivos.
* **YFinance:** Consumo do histórico de preços e indicadores de dividendos das companhias.
* **Matplotlib / Seaborn / PdfPages:** Geração e formatação visual dos dashboards em PDF.
* **Gspread:** Integração com banco de dados em nuvem (Google Sheets).
* **Telegram Bot API:** Interface de mensageria para entrega de relatórios e sinais *intraday*.
* **PyInstaller & Agendador de Tarefas (Windows):** Compilação do ecossistema em um executável único para orquestração e execução autônoma durante o pregão.

---

## 🚀 Como Utilizar

1. Clone o repositório.
2. Configure as **Variáveis de Ambiente / Credenciais** no seu sistema (Caminho do JSON do Google Cloud, `ID_PLANILHA`, `BOT_TOKEN` e `CHAT_ID`).
3. Certifique-se de que o arquivo `.gitignore` está configurado para não subir suas credenciais locais para o repositório.
4. Para a automação completa, compile o script `Ecossistema_Sniper_Master.py` em um executável e aponte o Agendador de Tarefas (Task Scheduler) do Windows para rodá-lo de hora em hora.

---
*Projeto desenvolvido por Bruno Felipe de Almeida (BrunexJundiai) - 2026*