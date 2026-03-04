# 📖 Documentação Técnica e de Negócio - Sniper B3

Este documento descreve as fontes de dados, o dicionário de variáveis e as regras de negócio implementadas nos motores de análise.

---

## 1. Dicionário de Dados (Base: ControleAcoes)
Fonte: Google Sheets (Planilha de Transações)

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| **Ativo** | String | Ticker da ação na B3 (ex: PETR4, VALE3). |
| **Tipo** | String | Tipo da operação (COMPRA/VENDA). |
| **Qtd** | Integer | Quantidade de cotas negociadas. |
| **Preco_Unitario** | Float | Valor pago por cada cota na transação. |
| **PM (Calculado)** | Float | Preço Médio Ponderado: `Soma(Vol) / Soma(Qtd)`. |
| **Meta %** | Float | Percentual alvo de alocação definido pelo investidor. |

---

## 2. Regras de Negócio (Lógica do Algoritmo)

### A. Radar Sniper (Operacional Diário)
O motor avalia o mercado buscando exaustão de preço para execução tática.
* **Forte Compra:** Ativado quando `RSI <= 25` e `Preço Atual < (PM * 0.85)`. Indica ativo extremamente descontado.
* **Venda (Lucro):** Ativado quando `RSI >= 75` e `Preço Atual > (PM * 1.20)`. Indica exaustão de compra e lucro acima de 20%.

### B. Smart Allocation (Rebalanceamento Mensal)
Cálculo para diluição de risco e reenquadramento de carteira.
* **Cálculo de Distância:** `Distância = Peso_Atual - Meta_%`.
* **Ação "FORTE COMPRA":** Gerada quando a `Distância` é negativa e significativa (ex: < -5%).
* **Ação "AGUARDAR":** Ativos que já atingiram ou superaram a meta de alocação.

### C. Viés Preditivo (Machine Learning Light)
* **Algoritmo:** Regressão Linear Simples via `Numpy.polyfit`.
* **Janela de Dados:** Últimos 180 dias de fechamento.
* **Output:** Coeficiente angular da reta de tendência para projetar o movimento dos próximos 30 dias.

---

## 3. Controles e Automação
* **Pipeline:** Google Sheets API ➔ Python ETL ➔ YFinance ➔ Telegram API.
* **Executáveis:** Gerados via `PyInstaller` para rodar sem dependência de IDE.
* **Agendamento:** - *Radar:* Diário (10h e 17h).
    - *Reporte Mensal:* Todo dia 01 de cada mês.