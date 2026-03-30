# ⚙️ Regras de Negócio e Lógica Quantitativa - Sniper B3 (V4.0 Master AI)

O Cérebro Quantitativo do ecossistema processa regras rigorosas sequencialmente para eliminar o viés emocional das decisões de investimento, integrando matemática estatística e Inteligência Artificial.

## 1. Trava Sistêmica (Isolamento de Ruído e Custo)
* **Condição de Bloqueio:** `dia_semana > 4` (Sábado/Domingo) OU `hora_atual < 10` OU `hora_atual >= 18`.
* **Objetivo:** Impedir que o robô tome decisões baseadas em leilões de abertura/fechamento ou dados estáticos de fim de semana, economizando também a cota da API da IA (Groq). Criptomoedas são monitoradas visualmente nos PDFs, mantendo as operações 24/7 a cargo da corretora.

---

## 2. Motor Preditivo e Indicadores Técnicos
* **Viés Preditivo (Upside 30d):** Regressão Linear Simples via `numpy.polyfit(x, y, 1)`. Usa os últimos 180 dias de fechamento para projetar a inclinação da reta de tendência para o próximo mês, minimizando o ruído diário.
* **RSI (Índice de Força Relativa):** Calculado com janela de 14 períodos para identificar sobrecompra (>75) ou sobrevenda (<25).
* **MACD (Moving Average Convergence Divergence):** Calculado com EMAs de 12 e 26 períodos, e sinal de 9 períodos. O MACD Histograma é extraído para identificar força e reversão de tendência.
* **Bandas de Bollinger:** Média Móvel Simples de 20 períodos com 2 desvios padrões (para cima e para baixo), servindo como limites dinâmicos de preço para o Agente de IA avaliar suporte e resistência.

---

## 3. Módulo Tático (Radar Sniper - Alertas Intraday)
Avalia o mercado buscando exaustão de preço para execução tática de curto prazo.
* **🔥 COMPRA SNIPER:** Ativado quando `RSI <= 25` e `Preço Atual < (PM_Real * 0.85)`. (Captura pânico extremo com 15% de desconto em relação ao próprio Preço Médio).
* **🔥 RECOMPRA SNIPER:** Ativada para ativos com posição zerada (`Qtd_Total == 0`). O sistema usa o `PM_Historico` como âncora para avisar a hora de voltar para o papel após uma queda irracional.
* **💰 VENDA (Exaustão):** Ativado quando a posição está ativa (`Qtd_Total > 0`), `RSI >= 75` e `Lucro > 15%`. Realização de lucro na euforia.
* **💰 VENDA (Proteção/Inversão):** Ativado quando a posição está ativa, `Lucro > 5%` e `Vies_Preditivo < -10%`. Protege o capital de uma mudança estrutural de tendência.

---

## 4. Módulo Estratégico (Filtro Mestre de Aportes B3)
Direcionamento inteligente do fluxo de caixa mensal da carteira "Core" (Equities).
* **🚫 BLOQUEADO (Faca Caindo):** Se `Vies_Preditivo < 0`. Proíbe sumariamente a compra, protegendo o capital de perdas estruturais contínuas.
* **🎯 FORTE COMPRA:** Se `Vies_Preditivo > 0` E `Distancia Meta < -2.0%`. (Tendência de alta aliada a forte déficit de alocação percentual).
* **🟢 COMPRA:** Se `Vies_Preditivo > 0` E `Distancia Meta < 0%`.
* **⏳ AGUARDAR:** Ativos que bateram a meta de alocação, ativos satélites (Target 0%) ou sem margem de segurança.
* **🔥 Caçador de Assimetrias (Desempate):** Em caso de múltiplos ativos com sinal de compra, o algoritmo prioriza matematicamente o ativo com o **Maior Viés Preditivo (Upside projetado)**. Foco no *Momentum* e no tamanho da oportunidade de curto prazo em vez do rebalanceamento percentual cego.

---

## 5. Conselho de IA (Multi-Agent RAG)
Filtro qualitativo final aplicado *apenas* sobre o ativo selecionado pelo "Caçador de Assimetrias".
* **Agente Quantitativo:** Analisa os indicadores (RSI, Bandas de Bollinger e MACD Histograma) do alvo para validar se o *timing* de suporte matemático faz sentido para *Value Investing*.
* **Agente Fundamentalista (RAG):** Faz *scraping* das 3 últimas notícias da empresa (Yahoo Finance) e analisa o impacto dos fundamentos recentes.
* **O Veredito:** Um grafo de estado (`LangGraph`) consolida as visões quantitativa e qualitativa e gera um dossiê executivo, aprovando ou recusando o aporte de forma autônoma.