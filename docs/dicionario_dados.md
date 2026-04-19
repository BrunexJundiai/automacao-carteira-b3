# Dicionario de Dados - Sniper B3 V6

Este documento descreve os campos de entrada, as variaveis transformadas, os objetos internos e os artefatos produzidos pela V6.

## 1. Fonte primaria: Google Sheets

### Campos minimos esperados

| Campo | Tipo | Descricao |
| :--- | :--- | :--- |
| `Ativo` | String | Codigo do papel conforme a carteira do usuario. |
| `Tipo` | String | Direcao da operacao. Esperado: `COMPRA` ou `VENDA`. |
| `Qtd` | Float | Quantidade da operacao. |
| `Preco_Unitario` | Float | Preco unitario da transacao. |

### Campos recomendados

| Campo | Tipo | Descricao |
| :--- | :--- | :--- |
| `Target_%` | Float | Meta percentual ideal na carteira. |
| `Mercado` | String | Classificacao do ativo, por exemplo `B3`, `USA`, `GLOBAL`. |
| `Bolsa` | String | Campo alternativo para identificacao de mercado. |
| `Ticker_Yahoo` | String | Ticker final a ser usado no Yahoo Finance, quando o mapeamento automatico nao bastar. |

## 2. Campos internos derivados no ETL

| Variavel | Tipo | Descricao |
| :--- | :--- | :--- |
| `Mercado` | String | Mercado resolvido a partir de `Mercado`, `Bolsa`, `Pais` ou default `B3`. |
| `YahooTicker` | String | Ticker final usado em mercado e noticias. |
| `Ticker_Base` | String | Nome base do ativo na carteira. |
| `Qtd_Ajustada` | Float | Quantidade com sinal invertido para vendas. |
| `Vol_Ajustado` | Float | Volume financeiro com sinal invertido para vendas. |
| `Qtd_Total` | Float | Saldo consolidado da posicao. |
| `Investido_Liquido` | Float | Capital liquido historicamente alocado no ativo. |
| `Meta_Alvo` | Float | Meta percentual consolidada do ativo. |
| `PM` | Float | Preco medio da posicao. |

## 3. Regras de resolucao de ticker

| Situacao | Resultado |
| :--- | :--- |
| `Ticker_Yahoo` informado | `YahooTicker = Ticker_Yahoo` |
| Mercado B3 e ativo sem `.SA` | adiciona `.SA` |
| Mercado global | mantem ticker informado |

## 4. Estrutura de historico de mercado

Depois do `yf.download`, cada ativo e normalizado para um `DataFrame` com:

| Campo | Tipo | Descricao |
| :--- | :--- | :--- |
| `Open` | Float | Preco de abertura |
| `High` | Float | Maxima do periodo |
| `Low` | Float | Minima do periodo |
| `Close` | Float | Fechamento utilizado nas metricas |
| `Volume` | Float | Volume negociado, usado no POC |

Se `Adj Close` estiver disponivel, ele alimenta `Close`.

## 5. Objeto institucional: AssetSnapshot

Cada ativo processado pelo ciclo gera um `AssetSnapshot` com:

| Campo | Tipo | Descricao |
| :--- | :--- | :--- |
| `portfolio_symbol` | String | Ticker como aparece na carteira |
| `yahoo_symbol` | String | Ticker efetivo usado no Yahoo |
| `market` | String | Mercado do ativo |
| `quantity` | Float | Quantidade em custodia |
| `avg_price` | Float | Preco medio |
| `invested_net` | Float | Investimento liquido historico |
| `current_price` | Float | Ultimo preco disponivel |
| `profit_pct` | Float | Lucro ou prejuizo percentual |
| `target_pct` | Float | Meta percentual |
| `current_value` | Float | Valor atual da posicao |
| `headlines` | List[String] | Manchetes recentes do ativo |
| `indicators` | `IndicatorSnapshot` | Pacote de indicadores calculados |

## 6. Pacote de indicadores: IndicatorSnapshot

| Campo | Tipo | Descricao |
| :--- | :--- | :--- |
| `rsi` | Float | RSI de 14 periodos |
| `macd_line` | Float | Linha do MACD |
| `macd_signal` | Float | Sinal do MACD |
| `macd_hist` | Float | Histograma do MACD |
| `bollinger_upper` | Float | Banda superior de Bollinger |
| `bollinger_lower` | Float | Banda inferior de Bollinger |
| `predictive_bias_30d` | Float | Vies preditivo projetado para 30 dias |
| `point_of_control` | Float | POC calculado por volume |
| `fibonacci_38` | Float | Retração de Fibonacci 38.2 |
| `fibonacci_61` | Float | Zona de ouro 61.8 |

## 7. Regras das metricas

### Viés Preditivo 30d

- Baseado em regressao linear simples sobre a serie de `Close`.
- Usa pelo menos 30 observacoes para produzir leitura.
- Deve ser interpretado como inclinacao projetada, nao alvo garantido.

### Point of Control

- Divide a faixa de preco em bins.
- Soma o `Volume` por faixa.
- Seleciona a faixa de maior concentracao de volume.
- Retorna o ponto medio dessa faixa.

### Fibonacci

- Usa janela recente de 60 observacoes.
- Calcula `38.2%` e `61.8%` com base em maximo e minimo do recorte.

### Dividendos projetados

- Media dos proventos dos ultimos 12 meses.
- Multiplica pela quantidade em custodia.
- Gera `Estimativa_Div`, `Mes_Previsto` e `Data_Prev_Dt`.

## 8. DataFrame de dashboard

No relatorio global, a V6 materializa um `DataFrame` com:

| Campo | Tipo | Descricao |
| :--- | :--- | :--- |
| `Ativo` | String | Ticker do ativo |
| `Ativo_Display` | String | Ticker limpo para exibicao |
| `Preco_Unitario_Atual` | Float | Ultimo preco |
| `Investido` | Float | Investimento historico liquido |
| `Valor_Atual` | Float | Valor atual da posicao |
| `Lucro_RS` | Float | Resultado absoluto |
| `Estimativa_Div` | Float | Projecao anualizada simplificada |
| `Mes_Previsto` | String | Janela prevista para proximo provento |
| `Data_Prev_Dt` | Datetime | Data prevista normalizada |
| `Projeção_30d` | Float | Valor atual ajustado pelo vies preditivo |
| `Qtd` | Float | Quantidade em custodia |
| `PM` | Float | Preco medio |

## 9. DataFrame de rebalanceamento

O modulo de aportes e poda cria um `DataFrame` com:

| Campo | Tipo | Descricao |
| :--- | :--- | :--- |
| `Ativo` | String | Ticker do ativo |
| `Qtd` | Float | Quantidade em custodia |
| `Meta_%` | Float | Meta percentual |
| `Peso_%` | Float | Peso atual na carteira |
| `Distancia` | Float | Desvio entre peso atual e meta |
| `Rentab_%` | Float | Rentabilidade percentual |
| `Vies_Preditivo_%` | Float | Vies de 30 dias |
| `RSI` | Float | RSI atual |
| `Preço` | Float | Preco atual |
| `PM` | Float | Preco medio |
| `Valor_R$` | Float | Valor atual da posicao |
| `Ação` | String | Classificacao do motor de rebalanceamento |
| `Valor_Poda_R$` | Float | Valor financeiro sugerido para poda |

## 10. Artefatos de saida

### Telegram

| Saida | Conteudo |
| :--- | :--- |
| Radar | Alertas taticos de compra e venda |
| Dashboard | Patrimonio, resultado, top performance, radar de alta e dividendos |
| Aportes | Foco de compra, motivo, poda sugerida e parecer IA |
| Dossie individual | Resumo quantitativo, contextual e PDF individual |

### PDFs

| Arquivo | Funcao |
| :--- | :--- |
| `Radar_Sniper_V6.pdf` | Lamina tecnica dos ativos em alerta |
| `Relatorio_Carteira.pdf` | Dashboard multipagina da carteira |
| `Reporte_Mensal_Aportes_V6.pdf` | Estrategia de aporte e rebalanceamento |
| `Analise_<ATIVO>.pdf` | Lamina tecnica individual |

## 11. Configuracao critica

Variaveis de ambiente relevantes:

| Variavel | Descricao |
| :--- | :--- |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | ID da planilha |
| `GOOGLE_SERVICE_ACCOUNT_JSON_PATH` | Path do JSON de autenticacao |
| `TELEGRAM_BOT_TOKEN` | Token do bot |
| `TELEGRAM_CHAT_ID` | Chat destino |
| `GROQ_API_KEY` | Chave do modelo Groq |
| `PREGAO_HORA_INICIO` | Hora inicial do pregrao |
| `PREGAO_HORA_FIM` | Hora final do pregrao |
| `RADAR_INTERVAL_MINUTES` | Intervalo entre ciclos |
| `GLOBAL_REPORT_EVERY_N_CYCLES` | Frequencia do dashboard global |

