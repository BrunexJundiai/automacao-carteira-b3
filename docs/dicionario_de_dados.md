# Dicionário de Dados - Smart Portfolio Tracker

Este documento descreve a estrutura de colunas do painel de Business Intelligence e da tabela transacional.

| Coluna | Origem | Descrição |
| :--- | :--- | :--- |
| **Data** | Manual | Data em que a operação (compra/venda) foi realizada. |
| **Ativo** | Manual | Código da ação na B3 (Ticker). Ex: BBAS3. |
| **Tipo** | Manual | Define se foi uma operação de "Compra" ou "Venda". |
| **Qtd** | Manual | Quantidade de ações negociadas nesta operação. |
| **Preco_Unitario**| Manual | Preço exato pago por cada ação. |
| **Target_%** | Manual | Meta percentual de alocação deste ativo no patrimônio total. |
| **Empresa** | Script (YFinance) | Razão Social ou nome oficial da companhia. |
| **Ramo/Setor** | Script (YFinance) | Setor da economia em que a empresa atua. |
| **Preço Atual** | Script (YFinance) | Cotação da ação em tempo real no mercado. |
| **Seu PM** | Script (Pandas) | Preço Médio ponderado, calculado sobre o histórico de compras. |
| **Rentab. (%)** | Script (Pandas) | Lucro/prejuízo não-realizado da posição. |
| **DY (%)** | Script (YFinance) | *Dividend Yield*. Rendimento de dividendos dos últimos 12 meses. |
| **P/VP** | Script (YFinance) | Preço/Valor Patrimonial. Indicador de desconto da ação. |
| **Peso Atual (%)**| Script (Pandas) | Porcentagem real que esta empresa ocupa no patrimônio total hoje. |
| **Distância Meta**| Script (Pandas) | Diferença entre o Peso Atual e o Target_%. Se negativo, indica defasagem. |
| **Ação** | Script (Regra de Negócio)| Recomendação automática do algoritmo ("Forte Compra", "Aguardar"). |

## Dicionário de Dados - Módulo Preditivo e Analítico (`df_resultado`)

Esta tabela é gerada pelo script de Dashboard Avançado e foca em modelagem preditiva e DRE histórico.

| Coluna | Origem | Descrição |
| :--- | :--- | :--- |
| **Ativo** | Script | Código da ação na B3 (Ticker). |
| **Total Investido (R$)** | Script (Pandas) | Soma de todo o capital já gasto em compras neste ativo (Preço Médio x Qtd). |
| **Valor Atual (R$)** | Script (YFinance) | Valor de mercado da posição hoje (Cotação Atual x Qtd). |
| **Lucro/Perda (R$)** | Script (Matemática) | Diferença absoluta entre o Valor Atual e o Total Investido (Ganho Não-Realizado). |
| **Lucro (%)** | Script (Matemática) | Representação percentual do lucro ou prejuízo da posição. |
| **Div. Últimos 12m/Ação (R$)**| Script (YFinance) | Soma de dividendos pagos por **uma única ação** desta empresa no último ano. |
| **Estimativa Próx. Div. (R$)**| Script (Matemática) | Cálculo preditivo: (Média dos dividendos do último ano) x (Quantidade de ações que o usuário possui). |
| **Previsão Mês Próx. Div.**| Script (Datetime) | Projeção da data do próximo pagamento, baseada na média de dias de intervalo dos últimos pagamentos. |
| **Projeção 30d (R$)** | Script (NumPy) | Preço alvo da ação para daqui 30 dias, utilizando modelo de Machine Learning (Regressão Linear / `polyfit`) sobre o histórico de 6 meses. |
| **Viés Tendência** | Regra de Negócio | Classificação visual ("Alta 🟢" ou "Baixa 🔴") comparando o Preço Atual com a Projeção de 30 dias. |