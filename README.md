# 📈 Automação e Balanceamento de Carteira B3

Um pipeline de dados (ETL) e dashboard gerencial construído em Python para automatizar o acompanhamento e o rebalanceamento de uma carteira de ações na Bolsa de Valores Brasileira (B3).

## 🎯 O Problema
Plataformas de corretoras e planilhas manuais mostram a cotação atual, mas falham em fornecer *insights* acionáveis. O investidor frequentemente perde tempo calculando preço médio na mão ou deixa o emocional ditar qual ativo comprar no mês.

## 💡 A Solução
Este projeto utiliza conceitos de Engenharia de Dados e Business Intelligence para criar uma arquitetura simples e autônoma:
1. **Extract:** Consome dados transacionais diretamente de um banco de dados em nuvem (Google Sheets) via API, mantendo o histórico de compras como fonte única da verdade.
2. **Transform:** Realiza o agrupamento matemático das posições, calcula o Preço Médio ponderado e cruza com dados em tempo real da B3.
3. **Load/BI:** Gera um painel analítico com indicadores fundamentalistas (Dividend Yield, P/VP, Setor) e calcula a distância exata de cada ativo em relação à meta de alocação da carteira.

O resultado é um *insight* automático informando **exatamente qual ativo deve receber o aporte do mês**, garantindo a compra na baixa e o controle rigoroso de risco.

## 🛠️ Tecnologias Utilizadas
* **Python**
* **Pandas:** Para manipulação de DataFrames, limpeza e cálculos de agregação.
* **YFinance:** Para extração de cotações e indicadores fundamentalistas em tempo real.
* **Gspread / Google Auth:** Para integração segura e consumo de dados via API.

## 📂 Arquitetura do Projeto
- `/src`: Scripts Python contendo o motor de análise e a infraestrutura de criação do banco de dados.
- `/docs`: Documentação do projeto, incluindo o Dicionário de Dados da modelagem.
- `README.md`: Apresentação e documentação principal.

## 🚀 Como utilizar
Os scripts na pasta `src` servem como base. Para uso pessoal, recomenda-se a execução do motor analítico em um ambiente como o Google Colab, inserindo as credenciais de autenticação próprias para leitura do banco de dados transacional.