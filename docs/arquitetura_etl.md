# Arquitetura de Dados e Automacao - Sniper B3 V6

Este documento descreve a arquitetura operacional da V6 com foco no fluxo real de dados, transformacoes internas, sincronizacao de mercado e entrega de relatorios.

## 1. Principio estrutural

O Sniper B3 V6 adota o modelo `Single Source of Truth`:

- a planilha Google Sheets define a carteira;
- o Yahoo Finance fornece historicos e manchetes;
- o orquestrador gera snapshots consistentes para todos os modulos do ciclo;
- Telegram e PDFs sao apenas camadas de entrega.

Isso significa que o mesmo snapshot alimenta radar, dashboard, rebalanceamento e analise individual.

## 2. Fluxo ETL central

### Extract

As fontes da V6 sao:

- `Google Sheets API`: operacoes da carteira, metas de alocacao e metadados de mercado.
- `Yahoo Finance`: historico OHLCV, dividendos e headlines.

### Transform

O modulo `dados_mercado.py` aplica as seguintes transformacoes:

- normalizacao de `Ativo` para caixa alta;
- resolucao de `Mercado`;
- resolucao de `YahooTicker` com prioridade para `Ticker_Yahoo`;
- injecao de `.SA` para ativos marcados como `B3`;
- criacao de `Qtd_Ajustada` e `Vol_Ajustado` para consolidar compras e vendas;
- calculo de `Qtd_Total`, `Investido_Liquido`, `Meta_Alvo` e `PM`.

### Load

O resultado do ETL e um `DataFrame` consolidado da carteira, que serve como base para:

- snapshots por ativo;
- modulos de decisao;
- relatorios;
- comandos do bot.

## 3. Resolucao de tickers

A V6 corrige uma fragilidade historica do projeto: assumir que todo ticker sem hifen pertence a B3.

Regra final:

1. se `Ticker_Yahoo` existir, ele prevalece;
2. se o mercado for `B3`, o sistema usa `ATIVO.SA`;
3. se o mercado for global, o ticker e mantido como informado.

Com isso, a V6 passa a suportar com mais confiabilidade:

- acoes B3;
- ETFs locais;
- BDRs;
- ativos globais;
- miners e outros papeis internacionais.

## 4. Download de mercado

O historico e baixado por `yf.download` em lote, com:

- `period="1y"` no ciclo principal;
- `interval="1d"`;
- `threads=False`;
- `group_by="ticker"`.

Essa escolha reduz ruido de concorrencia e deixa o ciclo previsivel em producao.

O retorno e sanitizado para manter o conjunto:

- `Open`
- `High`
- `Low`
- `Close`
- `Volume`

Se `Adj Close` existir e estiver preenchido, ele passa a alimentar `Close`.

## 5. Snapshot institucional por ativo

Cada ativo do ciclo e consolidado em um `AssetSnapshot`, contendo:

- ticker da carteira;
- ticker do Yahoo;
- mercado;
- quantidade;
- preco medio;
- investido liquido;
- preco atual;
- lucro percentual;
- alvo percentual;
- valor atual;
- indicadores institucionais;
- headlines recentes.

Esse objeto e a materia-prima do radar, dos aportes, dos dashboards e do dossie individual.

## 6. Fabrica quantitativa

O modulo `indicadores.py` concentra os calculos:

- `RSI 14`;
- `MACD`;
- `Bandas de Bollinger`;
- `Viés Preditivo 30d`;
- `Fibonacci 38.2 / 61.8`;
- `POC por volume`.

O POC da V6 usa `Volume` agregado por faixa de preco, abandonando a aproximacao antiga por frequencia pura.

## 7. Camada de contexto e IA

O modulo `agentes_ia.py` nao promete um RAG documental pesado. O que ele faz de forma objetiva e:

- recuperar ate 3 headlines recentes do Yahoo Finance;
- montar um grafo simples com leitura quantitativa, leitura fundamentalista e parecer final;
- devolver um dossie curto em Markdown para decisao assistida.

Essa camada deve ser entendida como `context enrichment`, nao como substituta de pesquisa fundamentalista profunda.

## 8. Orquestracao do ciclo

O modulo `orquestrador.py` governa:

- horario de pregrao;
- execucao a cada `RADAR_INTERVAL_MINUTES`;
- relatorio global a cada `GLOBAL_REPORT_EVERY_N_CYCLES`;
- comandos manuais do Telegram.

O loop protege contra concorrencia por lock de processo e registra warnings de ativos que falharam no pipeline.

## 9. Relatorios e entrega

O modulo `relatorios_pdf.py` preserva a linguagem visual legada do projeto:

- `Radar_Sniper_V6.pdf`;
- `Relatorio_Carteira.pdf`;
- `Reporte_Mensal_Aportes_V6.pdf`;
- `Analise_<ATIVO>.pdf`.

As mensagens de Telegram seguem o mesmo principio:

- radar tatico em HTML;
- dashboard global em Markdown;
- aportes e rebalanceamento em Markdown;
- dossie individual sob demanda.

## 10. Dividendos e datas

A V6 estima dividendos por media dos ultimos 12 meses e normaliza datas para evitar conflito entre `tz-aware` e `tz-naive`, problema que historicamente pode quebrar o ciclo automatico quando o feed retorna indices em timezone diferente do relogio da aplicacao.

## 11. Pesquisa e validacao

O modulo `backtesting.py` foi introduzido para responder uma pergunta que a documentacao antiga nao respondia: existe sinal observavel?

Ele permite medir:

- quantidade de observacoes;
- hit rate;
- retorno medio;
- drawdown da janela do sinal.

Nao substitui um backtester institucional completo, mas cria a base correta para validacao progressiva.

## 12. Containerizacao e producao

A V6 roda em `python:3.11-slim`, com:

- `PYTHONDONTWRITEBYTECODE=1`;
- `PYTHONUNBUFFERED=1`;
- `TZ=America/Sao_Paulo`.

O `Dockerfile` aponta para:

```bash
python -m sniper_b3_v6.main run-loop
```

Isso elimina o descolamento entre documentacao e runtime que existia nas versoes antigas.

