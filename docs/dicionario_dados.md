# 📖 Documentação Técnica e de Negócio - Sniper B3 (V3.0 Master)

Este documento descreve a arquitetura de dados, o dicionário de variáveis do fluxo ETL (Extract, Transform, Load) e as regras de negócio rigorosas implementadas no motor unificado do Ecossistema Sniper B3, contemplando Equities (B3) e Ativos Alternativos (Criptomoedas).

---

## 1. Dicionário de Dados e Pipeline (ETL)

**Fonte (Extract):** Google Sheets (Planilha `ControleAcoes`) e API do Yahoo Finance.
*Nota de Engenharia:* A extração via API do Google Sheets utiliza o parâmetro `UNFORMATTED_VALUE` para garantir a ingestão do dado numérico puro (máquina), prevenindo bugs de tipagem causados por formatações visuais de moeda local (ex: R$ e pontos de milhar).

### A. Dados Brutos (Raw Data)
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| **Ativo** | String | Ticker da ação. Tickers brasileiros recebem o sufixo `.SA`. Criptoativos (com hífen, ex: `BTC-BRL`) mantêm a string original. |
| **Tipo** | String | Direção da operação (COMPRA ou VENDA). |
| **Qtd** | Float | Quantidade negociada (aceita frações até 8 casas decimais para Cripto). |
| **Preco_Unitario** | Float | Valor financeiro unitário da transação. |
| **Target_%** | Float | Meta percentual ideal de alocação. Para Criptomoedas, utiliza-se `0%` para isolar o ativo do algoritmo de aportes da B3. |

### B. Variáveis Transformadas (Transform - Matemática Analítica)
| Variável Interna | Tipo | Lógica de Cálculo (Python) |
| :--- | :--- | :--- |
| **Qtd_Ajustada** | Float | Transforma operações de VENDA em valores negativos para abater o saldo. |
| **Investido_Liquido** | Float | Volume financeiro ajustado (`Qtd_Ajustada * Preco_Unitario`). |
| **Qtd_Total** | Float | Somatório da `Qtd_Ajustada` agrupado por Ativo (Saldo Real em Custódia). |
| **PM_Historico** | Float | Preço médio calculado *apenas* sobre as operações de COMPRA. |
| **PM_Real** | Float | `Investido_Liquido / Qtd_Total` (se Qtd > 0). Se Qtd = 0, herda o `PM_Historico`. |
| **Cotação_Sintética**| Float | (Exclusivo Cripto) Contorna o delisting de pares BRL gerando o valor real via `BTC-USD * USDBRL=X`. |
| **Vies_Preditivo_%**| Float | Projeção percentual de Upside/Downside em 30 dias (Numpy Polyfit). |

---

## 2. Regras de Negócio (O Cérebro Quantitativo)

As regras abaixo são processadas sequencialmente pelo script Master para eliminar o viés emocional das decisões de investimento.

### A. Trava Sistêmica (Isolamento de Ruído)
* **Condição de Bloqueio:** `dia_semana > 4` (Sábado/Domingo) OU `hora_atual < 10` OU `hora_atual >= 18`.
* **Objetivo:** Impedir que o robô tome decisões baseadas em leilões de abertura/fechamento ou dados estáticos de fim de semana (horário comercial B3).

### B. Módulo Tático (Radar Sniper)
Avalia o mercado buscando exaustão de preço para execução intraday.
* **🔥 COMPRA SNIPER:** Ativado quando `RSI <= 25` e `Preço Atual < (PM_Real * 0.85)`. (Captura pânico extremo com 15% de desconto).
* **🔥 RECOMPRA SNIPER:** Mesma regra da Compra Sniper, mas ativada para ativos com `Qtd_Total == 0`. O sistema usa o `PM_Historico` como âncora para avisar a hora de voltar para o papel.
* **💰 VENDA (Exaustão):** Ativado quando `Qtd_Total > 0`, `RSI >= 75` e `Lucro > 15%`.
* **💰 VENDA (Proteção/Inversão):** Ativado quando `Qtd_Total > 0`, `Lucro > 5%` e `Vies_Preditivo < -10%`. Protege o capital de uma mudança estrutural de tendência.

### C. Módulo Estratégico B3 (Filtro Mestre de Aportes)
Cálculo mensal para direcionamento inteligente de fluxo de caixa da carteira "Core" (Ações).
* **🚫 BLOQUEADO (Faca Caindo):** Se `Vies_Preditivo < 0`. Proíbe a compra, protegendo o capital de perdas estruturais.
* **🎯 FORTE COMPRA:** Se `Vies_Preditivo > 0` E `Distancia < -2.0%`. (Tendência de alta aliada a déficit de alocação).
* **🟢 COMPRA:** Se `Vies_Preditivo > 0` E `Distancia < 0%`.
* **⏳ AGUARDAR:** Ativos que bateram a meta, criptoativos (Target 0) ou sem margem de segurança.
* **🔥 Caçador de Assimetrias (Desempate):** Em caso de múltiplos ativos com selo de compra, o algoritmo prioriza matematicamente o ativo com o **Maior Viés Preditivo (Upside projetado)**, focando no *Momentum* e no tamanho da oportunidade de curto prazo em vez de focar apenas no rebalanceamento percentual cego da carteira.

### D. Módulo de Ativos Alternativos (Estratégia Cripto)
Gerenciamento apartado (Carteira Satélite) para absorção de altíssima volatilidade.
* **Trend Following (SMA 30):** Monitoramento visual da Média Móvel Simples de 30 dias sobre o histórico de 180 dias.
* **Isolamento de Alocação:** Criptomoedas são ocultadas da recomendação de aportes mensais para não distorcer o fluxo de caixa de dividendos, funcionando puramente como rastreador de assimetria de capital.

### E. Módulo Preditivo (Machine Learning Light)
* **Algoritmo:** Regressão Linear Simples via `numpy.polyfit(x, y, 1)`.
* **Janela de Dados:** Últimos 180 dias de fechamento (minimiza o ruído diário).
* **Output:** Inclinação da reta de tendência projetada para os próximos 30 dias.

---

## 3. Arquitetura e Automação (Single Source of Truth)

Na Versão 3.0, os três submódulos (Radar, Dashboard e Aportes) foram consolidados em um único arquivo mestre para garantir eficiência computacional.

* **Pipeline Otimizado:** O download do histórico de 180 dias de cotações (`yf.download`) é feito **apenas uma vez** por ciclo, distribuindo os dados na memória (RAM) para os três módulos. Isso elimina a redundância de rede e previne bloqueios de IP (*Rate Limit*).
* **Separação Institucional:** O motor gera PDFs *Multi-Page*, separando a Lâmina Analítica de Ações (Core) da Lâmina de Criptoativos (Satélite), aplicando indicadores customizados para cada classe de ativo.
* **Executável Único:** O código `Ecosistema_Sniper_Master.py` é compilado via `PyInstaller` (`--onefile --console --clean`), gerando um executável autônomo sem dependência de ambientes Python locais.
* **Orquestração:** Agendador de Tarefas (Windows Task Scheduler) configurado para executar o arquivo `.exe` **a cada meia hora**, processando o ecossistema completo e enviando os 3 relatórios sequenciais via Telegram API.