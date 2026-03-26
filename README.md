# 📈 Sniper B3: Ecossistema Master Quantitativo (V3.0)

Um ecossistema avançado de **Engenharia de Dados**, **Decisão Estratégica** e **Automação Quantitativa** construído em Python. O projeto funciona como um motor de *Hedge Fund* particular: automatiza o monitoramento tático de ativos (B3 e Criptomoedas), o rebalanceamento de carteira e utiliza modelos de **Regressão Linear de 180 dias** e **Trend Following** para projetar tendências e proteger o capital.

## 🎯 O Problema
Investidores enfrentam dificuldades em manter a disciplina emocional em mercados voláteis, muitas vezes falhando em identificar o *timing* técnico ideal para aportes, tentando "pegar facas caindo" ou mantendo em carteira ativos que perderam seus fundamentos de tendência. Além disso, gerenciar planilhas de diferentes classes de ativos (Ações vs. Cripto) gera ruído e distorce o fluxo de caixa. Este projeto resolve essa dor através de algoritmos frios, matemáticos e precisos.

## 💡 A Solução (Arquitetura Master)
Na versão 3.0, o sistema evoluiu para um **Ecossistema Master Unificado** com estratégia **Core-Satellite** (Ações como núcleo estrutural e Criptomoedas como satélite de assimetria). Utilizando conceitos sólidos de **ETL (Extract, Transform, Load)** e **Containerização**, a arquitetura opera com *Single Source of Truth* (Fonte Única da Verdade):

1. **Extract (Extração Blindada):** Consumo centralizado via API do Google Sheets utilizando `UNFORMATTED_VALUE` (para ignorar formatações visuais de moeda/milhares que causam bugs) e YFinance (histórico de 6 meses). Executado apenas uma vez por ciclo para evitar bloqueios de API.
2. **Transform (Cotação Sintética e Matemática):** Processamento de Saldo Ajustado, cálculo de Preço Médio inteligente e modelagem estatística. Para contornar remoções abruptas de pares de moedas BRL na API, o sistema cria uma **Cotação Sintética** matemática para o Bitcoin (`BTC-USD * USDBRL=X`).
3. **Load/Analytics (A Tríade Sniper):** O pipeline alimenta três módulos de decisão simultâneos e envia dashboards executivos *multi-page* em PDF e alertas táticos via Telegram.

---

## ⚙️ A Tríade de Decisão (Módulos do Sistema)

### 1. Radar Sniper (Operacional e Tático)
Um robô que avalia o mercado em busca de exaustão de preço.
* **Memória de PM Histórico:** Se um ativo for totalmente vendido (lucro realizado), o sistema guarda o seu último Preço Médio. Se a ação despencar irracionalmente no futuro, ele emite um alerta exclusivo de **🔥 RECOMPRA SNIPER**.
* **Trava de Segurança (Cripto):** O ecossistema silencia o Bitcoin fora do horário comercial da B3, deixando o monitoramento 24/7 de alta volatilidade a cargo da corretora, focando puramente na visão analítica diária no PDF.

### 2. Dashboard Estratégico (Visão Executiva Core-Satellite)
Visão consolidada da saúde do patrimônio separada em Lâminas.
* **Página 1 (Core B3):** Focada em *Value Investing*. Exibe Composição do Patrimônio, Cronograma de Dividendos futuros projetados pela média dos últimos 12 meses e Regressão Linear.
* **Página 2 (Satélite Cripto):** Focada em *Trend Following*. Isola os ativos alternativos, cruzando o preço de fechamento com uma Média Móvel Simples (SMA) de 30 dias para identificar visualmente tendências de alta ou correções severas, além de uma tabela de KPIs exclusiva.

### 3. Gestão de Fluxo de Caixa (Aportes Mensais)
Inteligência de rebalanceamento cruzada com tendência e *Momentum*.
* **Filtro Mestre (A Trava da Faca Caindo):** Bloqueia sumariamente qualquer compra de ativo com **Viés Preditivo Negativo**, independentemente de quão descontada a ação pareça estar.
* **Isolamento de Alocação:** Criptomoedas são configuradas com Target 0% e blindadas pelo algoritmo para não sugarem o fluxo de caixa mensal destinado à construção de renda passiva (B3).
* **🔥 Caçador de Assimetrias:** Em caso de múltiplos ativos com sinal de compra, o algoritmo atua como um *Momentum Trader*, priorizando matematicamente o ativo com o **Maior Viés Preditivo (Upside)** em vez de apenas preencher lacunas percentuais na carteira.

---

## 📊 Regras de Negócio e Lógica Analítica

| Gatilho / Módulo | Regra Matemática Aplicada | Objetivo Estratégico |
| :--- | :--- | :--- |
| **Proteção de Formatação** | `UNFORMATTED_VALUE` (Google Sheets) | Impedir que pontos de milhar e siglas de moedas quebrem o cálculo de frações (ex: Satoshis). |
| **Cotação Sintética** | `BTC-USD * USDBRL=X` | Garantir o monitoramento de cripto em Reais mesmo se a API principal falhar no pareamento BRL. |
| **Compra Sniper** | `Preço < (PM * 0.85)` & `RSI <= 25` | Capturar pânico irracional do mercado com margem de segurança de 15%. |
| **Venda Tática** | `RSI >= 75` ou (`Lucro > 5%` & `Viés < -10%`) | Realizar lucro na euforia ou proteger capital em caso de inversão estrutural de tendência. |
| **Aporte Seguro** | `Viés > 0` & `Distância Meta < -2.0%` | Garantir que o capital novo só compre ativos descontados em tendência de alta comprovada. |
| **Desempate de Aporte** | `Maior Viés Preditivo (%)` | Caçar assimetrias e focar no *Momentum* de curto prazo, maximizando o potencial de alta. |
| **Trend Following (Cripto)**| `Fechamento vs SMA(30)` | Evidenciar graficamente se o ativo está trabalhando acima ou abaixo da sua média mensal. |

---

## 🖥️ Evidências e Relatórios Gerados

### 1. Radar Sniper (Alertas Intraday via Telegram)
Monitoramento em tempo real com disparo de sinais de entrada, realização de lucro e status do servidor.
| Compra / Recompra | Realização de Lucro | Zona Neutra |
| :---: | :---: | :---: |
| ![Compra](img/alerta_compra.png) | ![Venda](img/alerta_venda.png) | ![Neutro](img/alerta_neutro.png) |

### 2. Dashboard Estratégico (Lâminas em PDF)
O sistema gera um relatório em PDF com múltiplas páginas, respeitando a natureza de cada classe de ativo.

**Lâmina 1: Ações B3 (Equities & Dividendos)**
| Relatório Executivo (B3) |
| :---: |
| ![Gráficos 1 e 2](img/graficos_1_2.png) |
| ![Gráficos 3 e 4](img/graficos_3_4.png) |

**Lâmina 2: Ativos Alternativos (Criptoativos)**
| Trend Following (Evolução Histórica) | KPIs de Posição |
| :---: | :---: |
| ![Estratégia Cripto](img/acompanhamento_cripto.png) | ![DRE Cripto](img/acompanhamento_cripto_dre.png) |

### 3. Aportes Mensais (Fluxo de Caixa Direcionado)
Cruzamento da distância da meta de alocação com o viés preditivo de tendência. Oculta ativos satélites para proteger o caixa.
| Direcionamento (Telegram) | DRE Analítico e Alocação (PDF) |
| :---: | :---: |
| ![Reporte Mensal](img/reporte_mensal.png) | ![Estratégia de Alocação](img/estrategia_alocacao.png) |
| | ![Distância da Meta](img/distancia_meta_aporte.png) |
| | ![DRE Analítico](img/DRE_analitico.png) |

> 💡 **Insight:** A nova arquitetura garante que a meta engessada de portfólio seja apenas um filtro secundário. O modelo quantitativo age como um *Caçador de Assimetrias*, focando soberanamente na Regressão Linear para direcionar o capital ao ativo com maior projeção de alta no momento.

---

## 🛠 Tecnologias Utilizadas

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

* **Python / Pandas / Numpy:** Motor central para limpeza de dados (ETL), junções sintéticas e cálculos preditivos de *Machine Learning Light*.
* **YFinance:** Consumo de histórico de preços, *cross-currency* e indicadores de dividendos.
* **Matplotlib / Seaborn / PdfPages:** Geração e formatação visual avançada dos dashboards *multi-page* em PDF.
* **Gspread:** Integração com banco de dados em nuvem via Google Cloud API.
* **Telegram Bot API:** Interface de mensageria para entrega de relatórios e sinais *intraday*.
* **Docker:** Containerização completa da aplicação, garantindo execução autônoma, resiliente e contínua em ambiente isolado, substituindo orquestradores locais sujeitos a falhas.

---

## 🚀 Como Utilizar

1. Clone o repositório.
2. Configure as **Variáveis de Ambiente / Credenciais** no seu sistema (salvando o arquivo JSON de credenciais do Google Cloud na raiz do projeto e configurando `ID_PLANILHA`, `BOT_TOKEN` e `CHAT_ID` no código principal).
3. Mantenha os seus ativos de B3 e Criptomoedas (usando o sufixo padrão de mercado, ex: `BTC-BRL`) em uma planilha única do Google Sheets.
4. Para automação *hands-off*, construa a imagem e inicie o container via **Docker**:
   ```bash
   docker build -t sniper-bot .
   docker run -d --name meu-sniper-bot --restart unless-stopped sniper-bot