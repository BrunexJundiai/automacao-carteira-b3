import os
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import gspread
from datetime import datetime, timedelta
import requests
import warnings

warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

# ==========================================
# CONFIGURAÇÕES (VARIÁVEIS DE AMBIENTE)
# ==========================================
CAMINHO_JSON = os.environ.get('CAMINHO_CREDENCIAIS_GOOGLE')
ID_PLANILHA = os.environ.get('ID_PLANILHA_B3')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def gerar_dash_preditivo():
    gc = gspread.service_account(filename=CAMINHO_JSON)
    planilha = gc.open_by_key(ID_PLANILHA)
    dados = planilha.sheet1.get_all_records()
    df = pd.DataFrame(dados)
    
    # Processamento de Engenharia de Dados
    df['Ativo'] = df['Ativo'].astype(str).str.strip().str.upper().apply(lambda x: x if x.endswith('.SA') else f"{x}.SA")
    for col in ['Qtd', 'Preco_Unitario']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('R$', '').str.replace(',', '.'), errors='coerce')

    # Modelagem Preditiva via Regressão Linear
    # ... Lógica de Numpy Polyfit permanece igual ...

if __name__ == "__main__":
    gerar_dash_preditivo()