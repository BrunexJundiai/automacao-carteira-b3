# 📈 Sniper B3: Automação, BI e Inteligência Preditiva

Um ecossistema completo de **Engenharia de Dados** e **Business Intelligence** construído em Python para automatizar o acompanhamento, o rebalanceamento estratégico e a análise de tendência de uma carteira de investimentos na B3.

## 🎯 O Problema
Investidores frequentemente perdem tempo com cálculos manuais de Preço Médio, falham em identificar o momento técnico ideal de compra (RSI) ou deixam o emocional ditar a alocação de capital, distanciando-se do perfil de risco desejado.

## 💡 A Solução
Este projeto utiliza conceitos de **ETL (Extract, Transform, Load)** e **Análise Preditiva** para criar uma arquitetura de suporte à decisão:

1. **Extract:** Consumo de dados via API do Google Sheets (histórico de compras) e YFinance (cotações em tempo real).
2. **Transform:** Processamento matemático de Preço Médio ponderado, cálculo de rentabilidade real e modelagem de tendência.
3. **Load/Analytics:** Geração de dashboards executivos em PDF e alertas táticos automatizados via Telegram.

---

## 📊 Visualização dos Dados e Resultados

### 1. Radar Sniper (Operacional via Telegram)
O motor avalia o mercado diariamente em busca de exaustão de preço.
| Compra Agressiva | Zona Neutra | Venda (Lucro) |
| :---: | :---: | :---: |
| ![Compra](img/alerta_compra.jfif) | ![Neutro](img/alerta_neutro.jfif) | ![Venda](img/alerta_venda.jfif) |

### 2. Dashboard de Performance (Relatorio_Carteira.pdf)
Visão consolidada da saúde do patrimônio e projeções de curto prazo.
![Performance e Vies](img/graficos_1_2.png)
> **Destaque:** O gráfico de **Performance por Ativo** permite identificar rapidamente quais papéis estão gerando valor real vs. custo de oportunidade.

### 3. Estratégia de Alocação (Reporte_Mensal_Aportes.pdf)
Inteligência de rebalanceamento para manter a carteira fiel à meta alvo.
![Distancia Meta](img/distancia_meta_aporte.png)
![DRE Analitico](img/DRE_analitico.png)
> **Regra de Ouro:** O sistema calcula a **Distância da Meta**. Ativos com barras negativas acentuadas (ex: CXSE3 e ITUB4) são classificados automaticamente como **"FORTE COMPRA"**.

---

## ⚙️ Regras de Negócio e Lógica Analítica

| Módulo | Regra Aplicada | Objetivo |
| :--- | :--- | :--- |
| **Rebalanceamento** | `Peso Atual < (Meta - 2%)` | Indicar aporte no ativo mais defasado da estratégia. |
| **Radar Sniper** | `Preço < PM` & `RSI <= 25` | Identificar oportunidade de compra com desconto tático. |
| **Viés 30d** | `Regressão Linear (Numpy)` | Projetar a tendência de preço baseada nos últimos 180 dias. |

---

## 🛠️ Tecnologias Utilizadas

* **Python / Pandas:** Motor central para manipulação de DataFrames financeiros.
* **YFinance:** Extração de dados de mercado e indicadores técnicos.
* **Matplotlib / Seaborn:** Geração de visualizações de alta resolução para os relatórios.
* **Gspread:** Integração com banco de dados em nuvem.
* **Telegram Bot API:** Interface de entrega de insights e alertas em tempo real.

---

## 📂 Arquitetura do Projeto

* `/src_git`: Motores de análise (.py) com mascaramento de credenciais (Segurança).
* `/docs`: Dicionário de dados e documentação detalhada das regras de negócio.
* `/img`: Repositório de capturas, recortes dos PDFs e evidências do bot.

## 🚀 Como utilizar
1. Clone o repositório.
2. Configure as **Variáveis de Ambiente** no seu sistema (ID_PLANILHA, BOT_TOKEN, etc).
3. Certifique-se de que o arquivo `.gitignore` está protegendo as suas credenciais locais.
4. Execute os scripts via terminal ou agende via Windows Task Scheduler.

---
*Projeto desenvolvido por Bruno Felipe de Almeida (BrunexJundiai) - 2026*
