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