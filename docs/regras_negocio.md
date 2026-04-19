# Regras de Negocio e Logica Quantitativa - Sniper B3 V6

Este documento consolida as regras de decisao da V6 com base na arquitetura nova, no comportamento validado em producao e nas tecnicas quantitativas atualmente implementadas.

## 1. Escopo de mercado

A V6 foi redesenhada para o universo:

- acoes da B3;
- BDRs;
- ETFs;
- ativos globais;
- miners e papeis internacionais relacionados a commodities.

Fica explicitamente fora do escopo da V6:

- logica tatica de cripto;
- pares sinteticos de BTC em BRL;
- monitoramento 24/7 de ativos digitais.

## 2. Trava sistemica

O motor automatico so roda em horario comercial local:

- bloqueia sabado e domingo;
- bloqueia antes de `10h`;
- bloqueia a partir de `18h`.

Objetivos:

- reduzir ruido de leilao;
- evitar leitura de mercado parado;
- economizar chamadas de API;
- manter disciplina operacional.

## 3. Radar Sniper

O radar tatico varre a carteira procurando assimetria de curto prazo.

### Compra Sniper

Gatilho:

- `RSI <= 25`
- `Preço Atual < PM * 0.85`

Interpretacao:

- busca panico extremo;
- exige 15% de desconto em relacao ao preco medio;
- usa o vies preditivo para diferenciar recuperacao de queda em curso.

### Recompra Sniper

Na documentacao conceitual, a memoria historica segue valida como filosofia. Na implementacao atual da V6, o foco principal esta em ativos com posicao consolidada na carteira. Se a estrategia voltar a enfatizar recompras de ativos zerados, a regra deve ser reativada de forma explicita no pipeline com auditoria de posicao passada.

### Venda por Exaustao

Gatilho:

- posicao ativa;
- `RSI >= 75`;
- `Lucro > 15%`;
- `Viés <= 2%`.

Interpretacao:

- nao basta o RSI estar alto;
- a tendencia tambem precisa mostrar enfraquecimento;
- preserva a filosofia `let winners run`.

### Venda por Inversao de Tendencia

Gatilho:

- posicao ativa;
- `Lucro > 5%`;
- `Viés < -10%`.

Interpretacao:

- protege capital quando o modelo aponta deterioracao mais severa;
- reduz dependencia de intuicao subjetiva.

## 4. Filosofia "Let Winners Run"

A V6 preserva o principio central do projeto:

- um ativo vencedor nao deve ser vendido so porque o oscilador esticou;
- a confirmacao de enfraquecimento via vies preditivo continua sendo parte da regra.

Na pratica:

- sobrecompra isolada nao basta;
- exaustao so ganha prioridade quando a inclinacao projetada perde forca.

## 5. Motor de aportes e rebalanceamento

O modulo estrategico calcula:

- peso atual da posicao;
- distancia para a meta;
- rentabilidade;
- vies preditivo;
- RSI.

Em seguida classifica cada ativo em uma das acoes abaixo.

### BLOQUEADO - FACA CAINDO

Gatilho:

- `Viés Preditivo < 0`

Objetivo:

- impedir alocacao de novo capital em ativos cujo modelo segue projetando enfraquecimento.

### AGUARDAR CORRECAO

Gatilho:

- `RSI >= 65`

Objetivo:

- evitar aportes em ativos com leitura de curto prazo esticada;
- forcar disciplina de entrada.

### FORTE COMPRA

Gatilho:

- `Viés > 0`
- `Distancia < -2%` ou `Rentab_% <= -10%`

Objetivo:

- priorizar ativos subalocados com tendencia favoravel;
- capturar assimetria quando a carteira esta leve no papel ou quando a posicao esta pressionada, mas o modelo ainda projeta recuperacao.

### COMPRA

Gatilho:

- `Viés > 0`
- `Distancia < 0`

Objetivo:

- recompor ativos abaixo da meta sem violar filtro de tendencia e sem comprar topo evidente.

### AGUARDAR

Situacao:

- sem edge claro;
- meta equilibrada;
- sinal insuficiente.

### PODA

Gatilho:

- `Distancia >= 1%`
- `Rentab_% > 0`
- `Viés < 2%` ou `Distancia >= 5%`

Objetivo:

- identificar gordura acima da meta;
- sugerir valor financeiro de venda;
- reequilibrar sem desrespeitar o historico vencedor do ativo.

## 6. Caçador de assimetrias

Quando ha mais de um ativo elegivel para compra, a V6 ordena o universo de forma deterministica.

A logica pratica favorece:

- maior prioridade de acao;
- menor rentabilidade atual quando faz sentido;
- maior vies preditivo como desempate favoravel.

Isso reduz arbitrariedade no foco de compra do ciclo.

## 7. Indicadores e metricas institucionais

### RSI

- janela de 14 periodos;
- usado como filtro tatico e de correcao.

### MACD

- leitura de momentum e enfraquecimento;
- incorporado ao snapshot e ao dossie individual.

### Bollinger

- referencia dinamica para regime de preco;
- usada na leitura quantitativa e na camada consultiva.

### Viés Preditivo 30d

- regressao linear simples sobre `Close`;
- representa inclinacao projetada;
- nao deve ser tratado como `target price`.

### Point of Control por Volume

- soma volume por faixa de preco;
- busca a regiao de maior defesa institucional;
- substitui a aproximacao antiga por frequencia pura de observacoes.

### Fibonacci 38.2 e 61.8

- usa os ultimos 60 pontos da serie;
- fornece leitura de correcao e zona de ouro.

### Dividendos projetados

- media simplificada dos proventos dos ultimos 12 meses;
- alimenta a mensagem executiva e o dashboard global.

## 8. Conselho de IA

O conselho de IA continua existindo, mas a V6 documenta seu papel com mais rigor:

- nao e oraculo;
- nao substitui tese fundamentalista profunda;
- nao executa ordens.

A camada usa:

- snapshot quantitativo do ativo;
- manchetes recentes do Yahoo Finance;
- pipeline simples de analise via LangGraph.

O resultado e um parecer executivo em Markdown para apoiar decisao humana.

## 9. Pesquisa quantitativa

O comando `/b3 pesquisa TICKER` introduz uma camada de validacao que faltava nas versoes anteriores.

Mede:

- observacoes do sinal;
- hit rate em 5 dias;
- hit rate em 20 dias;
- retorno medio em 5 e 20 dias;
- drawdown da janela.

Essa camada e o primeiro passo para evoluir a plataforma de `sistema de sinais` para `framework de validacao`.

## 10. Regras operacionais de apresentacao

Uma decisao importante da V6 foi manter a camada visual conhecida da operacao:

- mensagens do Telegram seguem o formato historico do projeto;
- PDFs seguem o layout legado;
- as melhorias ficaram no motor, nao na experiencia de consumo.

Isso reduz choque operacional e facilita comparacao entre V5 e V6.

## 11. Regras de seguranca e governanca

Valem como regra de negocio de producao:

- nenhum token no codigo;
- `.env` e `secrets/` como fonte de configuracao sensivel;
- logs explicitos de falha;
- proibicao de dependencias legadas ocultas fora da arquitetura modular.

## 12. Interpretacao correta do sistema

O Sniper B3 V6 deve ser interpretado como:

- plataforma de monitoramento e decisao assistida;
- motor disciplinado de carteira;
- laboratorio quantitativo em evolucao.

Nao deve ser vendido nem entendido como:

- garantia de retorno;
- sistema de execucao automatica de ordens;
- substituto de validacao estatistica formal.

