# 📖 Dicionário de Dados - Sniper B3 (V4.0 Master AI)

Este documento descreve os metadados, as tipagens e as transformações matemáticas aplicadas no motor unificado do Ecossistema Sniper B3, contemplando Equities (B3) e Ativos Alternativos (Criptomoedas).

## 1. Fonte de Dados (Extract)
* **Google Sheets:** Planilha de `ControleAcoes`. A extração utiliza a API oficial do Google com o parâmetro `UNFORMATTED_VALUE` para garantir a ingestão do dado numérico puro, prevenindo bugs de tipagem causados por formatações visuais de moeda (ex: R$ e pontos de milhar).
* **Yahoo Finance API (yfinance):** Histórico de preços (180 dias) e dados de *News* (para RAG). O download é feito de forma sequencial (`threads=False`) e utiliza cache local (SQLite) para otimizar requisições e evitar *Rate Limits*.

---

## 2. Dados Brutos (Raw Data)
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| **Ativo** | String | Ticker do papel. Tickers brasileiros recebem o sufixo `.SA` dinamicamente. Criptoativos (com hífen, ex: `BTC-BRL`) mantêm a string original. |
| **Tipo** | String | Direção da operação (COMPRA ou VENDA). |
| **Qtd** | Float | Quantidade negociada (aceita frações até 8 casas decimais para Cripto). |
| **Preco_Unitario** | Float | Valor financeiro unitário da transação original. |
| **Target_%** | Float | Meta percentual ideal de alocação no portfólio. Para ativos satélites (Cripto), utiliza-se `0%` para isolá-los do algoritmo de aportes regulares. |

---

## 3. Variáveis Transformadas (Transform - Matemática Vetorial)
| Variável Interna | Tipo | Lógica de Cálculo (Pandas/Numpy) |
| :--- | :--- | :--- |
| **Qtd_Ajustada** | Float | Inversão de sinal: Transforma operações de VENDA em valores negativos para abater o saldo. |
| **Investido_Liquido** | Float | Volume financeiro ajustado (`Qtd_Ajustada * Preco_Unitario`). |
| **Qtd_Total** | Float | Somatório da `Qtd_Ajustada` agrupado por Ativo (Saldo Real em Custódia). |
| **PM_Historico** | Float | Preço Médio calculado *apenas* sobre as operações de COMPRA (memória do robô). |
| **PM_Real** | Float | `Investido_Liquido / Qtd_Total` (se Qtd > 0). Se Qtd = 0 (posição zerada), herda o `PM_Historico`. |
| **Cotação_Sintética**| Float | (Exclusivo Cripto) Contorna o *delisting* de pares BRL gerando o valor real via conversão cambial simultânea (`BTC-USD * USDBRL=X`). |
| **Lucro_RS** | Float | `(Qtd_Total * Cotação Atual) - Investido_Liquido`. Retorno absoluto da posição. |
| **Estimativa_Div** | Float | Projeção de dividendos calculada pela média dos proventos pagos nos últimos 12 meses multiplicada pela `Qtd_Total`. |