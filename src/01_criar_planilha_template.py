"""
Script de Inicialização: Cria a estrutura transacional (banco de dados) no Google Sheets.
"""
from google.colab import auth
import gspread
from google.auth import default

def inicializar_banco_dados():
    # 1. Autenticação via Google Auth
    auth.authenticate_user()
    creds, _ = default()
    gc = gspread.authorize(creds)

    # 2. Criação do arquivo
    nome_planilha = "Controle_Acoes_Carteira_Template"
    sh = gc.create(nome_planilha)
    aba = sh.sheet1

    # 3. Inserção dos cabeçalhos estruturais (Tabela Transacional)
    cabecalhos = [['Data', 'Ativo', 'Tipo', 'Qtd', 'Preco_Unitario', 'Target_%']]
    aba.update('A1:F1', cabecalhos)

    print("✅ Banco de dados (Planilha Transacional) criado com sucesso!")
    print(f"🔗 Link gerado: {sh.url}")

if __name__ == "__main__":
    inicializar_banco_dados()