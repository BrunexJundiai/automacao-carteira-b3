"""
Script de Ingestão de Dados: Automatiza o registro de novos aportes mensais no banco de dados.
"""
from google.colab import auth
import gspread
from google.auth import default
from datetime import datetime

def registrar_aporte_mensal():
    # 1. Autenticação e Conexão
    auth.authenticate_user()
    creds, _ = default()
    gc = gspread.authorize(creds)

    # ⚠️ INSIRA O LINK DA SUA PLANILHA TRANSACIONAL AQUI
    LINK_PLANILHA = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

    print("Conectando ao banco de dados...")
    planilha = gc.open_by_url(LINK_PLANILHA)
    aba = planilha.sheet1

    # 2. Dados de Exemplo para Ingestão (Substitua pelos dados reais no momento da execução)
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    
    novos_aportes = [
        [data_hoje, 'TICKER1', 'Compra', 10, 50.00, 25],
        [data_hoje, 'TICKER2', 'Compra', 15, 30.00, 25],
        [data_hoje, 'TICKER3', 'Compra', 20, 20.00, 25],
        [data_hoje, 'TICKER4', 'Compra', 12, 40.00, 25]
    ]

    # 3. Inserção no final do banco de dados (Append)
    print("Injetando novas transações...")
    aba.append_rows(novos_aportes, value_input_option='USER_ENTERED')

    print("✅ SUCESSO! Aportes registrados na base de dados.")

if __name__ == "__main__":
    registrar_aporte_mensal()