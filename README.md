# 📈 Sniper B3: Automação, BI e Inteligência Preditiva (V2.0)

Um ecossistema avançado de **Engenharia de Dados** e **Decisão Estratégica** construído em Python. O projeto automatiza o monitoramento tático de ativos, o rebalanceamento de carteira e utiliza modelos de **Regressão Linear** para projetar tendências de curto prazo na B3.

## 🎯 O Desafio
Investidores enfrentam dificuldades em manter a disciplina emocional em mercados voláteis, muitas vezes falhando em identificar o *timing* técnico ideal para aportes ou saídas estratégicas. Este projeto resolve essa dor através de algoritmos frios e precisos.

## 💡 A Solução (Arquitetura de Duas Camadas)
O ecossistema opera em dois níveis complementares de inteligência:

1. **Camada Estratégica (BI Mensal):** Relatórios executivos em PDF que cruzam a necessidade de rebalanceamento com o potencial de valorização futura.
2. **Camada Tática (Radar Sniper):** Um robô de alta frequência que monitora RSI, preço médio e viés preditivo para disparar alertas de execução via Telegram.

---

## 📊 Visualização de Resultados (Sniper V2)

### 1. Radar Tático & Heartbeat (Telegram)
O sistema opera em tempo real com envio de "Sinal de Vida" em zonas neutras e alertas táticos em oportunidades reais.

| Compra Sniper | Venda Estratégica | Heartbeat (Status) |
| :---: | :---: | :---: |
| ![Compra](img/alerta_compra.png) | ![Venda](img/alerta_venda.png) | ![Neutro](img/alerta_neutro.png) |

> [cite_start]**Destaque:** O novo alerta integra o **Viés 30d**, distinguindo se uma queda é uma oportunidade de fundo (VALE3) ou uma inversão de tendência perigosa (PETR4)[cite: 14, 57].

### 2. DRE Analítico & Inteligência Preditiva (PDF)
Relatórios que utilizam modelos estatísticos para projetar o preço alvo dos ativos.

![Performance e Vies](img/Reporte_Inteligente_20260305.pdf)

> [cite_start]**Insight:** Ativos com `Distância < -2%` e `Upside > 5%` são classificados como **🔥 SNIPER (ALTA TENDÊNCIA)**[cite: 56].

---

## ⚙️ Regras de Negócio e Engenharia Quantitativa

| Módulo | Técnica / Regra Aplicada | Objetivo |
| :--- | :--- | :--- |
| **Compra Sniper** | `RSI <= 25` + `Preço < (PM * 0.85)` | [cite_start]Capturar exaustão de venda e pânico irracional[cite: 56]. |
| **Venda Tática** | `RSI >= 75` ou `Lucro > 5% + Viés Negativo` | [cite_start]Realizar lucro em ativos esticados ou proteger capital em inversões[cite: 56]. |
| **Viés Preditivo** | `Regressão Linear (180 dias)` | [cite_start]Projetar a tendência estatística para os próximos 30 dias[cite: 57]. |
| **Heartbeat** | `Monitoramento Sistêmico` | Garantir a resiliência do robô e do agendador de tarefas. |

---

## 🛠️ Tecnologias e Técnicas Utilizadas

* [cite_start]**Python (Pandas & Numpy):** Motor central para manipulação de grandes volumes de dados financeiros e cálculos de regressão[cite: 57].
* **YFinance API:** Consumo de dados históricos e cotações em tempo real da B3.
* **Gspread (Google Cloud):** Integração com banco de dados em nuvem para controle de ativos.
* [cite_start]**Matplotlib & Seaborn:** Geração de visualizações de alta resolução e dashboards em PDF[cite: 6, 33].
* **Telegram Bot API:** Interface de entrega de insights táticos e notificações operacionais.
* **PyInstaller:** Empacotamento para executáveis resilientes voltados para automação em Windows.

---

## 🚀 Como utilizar
1. Clone o repositório.
2. Configure as **Variáveis de Ambiente** no sistema (ID_PLANILHA, BOT_TOKEN, etc).
3. O Radar está configurado para rodar via **Windows Task Scheduler** em intervalos de 60 minutos.
4. Utilize o script de simulação incluído para validar os gatilhos de alerta.

---
*Projeto desenvolvido por Bruno Felipe de Almeida (BrunexJundiai) - 2026*