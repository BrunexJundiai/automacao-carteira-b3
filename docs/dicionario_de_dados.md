# 📖 Dicionário de Dados e Regras de Negócio

Este documento detalha a estrutura de dados e a inteligência aplicada nos três motores do ecossistema **Smart Portfolio Tracker**.

---

## 1. Tabela Transacional (Google Sheets - Input)
*A base de dados primária onde o usuário registra suas movimentações.*

| Coluna | Descrição | Regra de Limpeza |
| :--- | :--- | :--- |
| **Data** | Data da operação. | Convertida para padrão ISO. |
| **Ativo** | Ticker da ação (Ex: BBAS3). | Normalizado para uppercase e adicionado sufixo `.SA`. |
| **Tipo** | Operação: COMPRA ou VENDA. | Convertida para uppercase para evitar erros de leitura. |
| **Qtd** | Quantidade de cotas. | Cast para Float. |
| **Preco_Unitario**| Preço pago por cota. | Remoção de 'R$' e tratamento de vírgula por ponto. |
| **Target_%** | Meta de alocação desejada. | Usado no motor de Rebalanceamento. |

---

## 2. Motor de Rebalanceamento e Aportes (`df`)
*Lógica aplicada para manter a estratégia de risco da carteira.*

| Coluna | Regra de Negócio | Objetivo |
| :--- | :--- | :--- |
| **Seu PM** | `Soma(Qtd * Preco) / Soma(Qtd Total)` | Cálculo de Preço Médio Ponderado Dinâmico. |
| **Peso Atual (%)**| `(Valor Ativo / Patrimônio Total) * 100` | Exposição real do ativo no momento. |
| **Distância Meta**| `Peso Atual (%) - Target_%` | Identificar desvios na estratégia de alocação. |
| **Ação** | **Regra:** Distância < -2% = **Forte Compra**; < 0 = **Marginal**; > 0 = **Aguardar**. | Automatizar a decisão de aporte mensal. |

---

## 3. Módulo Analítico e Preditivo (`df_resultado`)
*Inteligência de mercado e projeções de fluxo de caixa.*

| Coluna | Lógica de Cálculo / Modelo | Descrição |
| :--- | :--- | :--- |
| **Lucro/Perda** | `(Preço Atual - PM) * Qtd` | Resultado nominal (DRE) não-realizado. |
| **Estimativa Div.**| `Média(Div_12m) * Qtd Atual` | Projeção de renda baseada no histórico de 1 ano. |
| **Projeção 30d** | `Regressão Linear (Numpy polyfit)` | Tendência de preço baseada nos últimos 6 meses de histórico. |
| **Viés Tendência**| `IF(Projeção > Preço Atual, 🟢, 🔴)` | Indicador visual de momento de mercado. |

---

## 4. Radar de Oportunidades (Alertas Telegram)
*Análise técnica tática para otimização de entradas e saídas.*

| Indicador | Parâmetro de Regra | Ação Resultante |
| :--- | :--- | :--- |
| **RSI (IFR)** | Período de 14 dias. | Mede a força do movimento de preço. |
| **Sinal COMPRA** | `Preço < PM` **E** `RSI <= 35` | Alerta de ativo subvalorizado (Oportunidade de baixar PM). |
| **Sinal VENDA** | `Preço > (PM * 1.10)` **E** `RSI >= 70` | Alerta de ativo sobrecomprado (Oportunidade de lucro). |
