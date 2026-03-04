import os
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import gspread
import requests
import warnings
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

# ==========================================
# CONFIGURAÇÕES (VARIÁVEIS DE AMBIENTE)
# ==========================================
CAMINHO_JSON = os.environ.get('CAMINHO_CREDENCIAIS_GOOGLE')
ID_PLANILHA = os.environ.get('ID_PLANILHA_B3')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def enviar_telegram(mensagem, caminho_arquivo=None):
    url_text = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    url_doc = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    requests.post(url_text, data={"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "Markdown"})
    if caminho_arquivo:
        with open(caminho_arquivo, "rb") as f:
            requests.post(url_doc, data={"chat_id": CHAT_ID}, files={"document": f})

def processar_relatorio():
    gc = gspread.service_account(filename=CAMINHO_JSON)
    sh = gc.open_by_key(ID_PLANILHA)
    df_raw = pd.DataFrame(sh.sheet1.get_all_records())

    df_raw['Ativo'] = df_raw['Ativo'].str.strip().str.upper().apply(lambda x: x if x.endswith('.SA') else f"{x}.SA")
    for col in ['Qtd', 'Preco_Unitario', 'Target_%']:
        df_raw[col] = df_raw[col].astype(str).str.replace('R$', '').str.replace('%', '').str.replace(',', '.').astype(float)

    df_compras = df_raw[df_raw['Tipo'].str.upper() == 'COMPRA'].copy()
    df_compras['Total_Gasto'] = df_compras['Qtd'] * df_compras['Preco_Unitario']

    carteira = df_compras.groupby('Ativo').agg(Qtd_Total=('Qtd', 'sum'), Investido=('Total_Gasto', 'sum'), Meta_Alvo=('Target_%', 'max')).reset_index()
    carteira['PM'] = carteira['Investido'] / carteira['Qtd_Total']

    tickers = carteira['Ativo'].tolist()
    dados_mercado = yf.download(tickers, period="1d", progress=False)['Close']

    analise = []
    for t in tickers:
        preco = float(dados_mercado[t].iloc[-1]) if len(tickers) > 1 else float(dados_mercado.iloc[-1])
        row = carteira.loc[carteira['Ativo'] == t].iloc[0]
        analise.append({
            'Ativo': t.replace('.SA', ''),
            'Qtd': row['Qtd_Total'],
            'Preço': preco,
            'PM': row['PM'],
            'Valor_R$': row['Qtd_Total'] * preco,
            'Meta_%': row['Meta_Alvo']
        })

    df = pd.DataFrame(analise)
    patrimonio = df['Valor_R$'].sum()
    df['Peso_%'] = (df['Valor_R$'] / patrimonio) * 100
    df['Distancia'] = df['Peso_%'] - df['Meta_%']
    df['Ação'] = df['Distancia'].apply(lambda x: "FORTE COMPRA" if x < -2.0 else ("COMPRA" if x < 0 else "AGUARDAR"))
    df = df.sort_values(by='Distancia', ascending=True)

    # Geração de PDF e Disparo Telegram (Omitido para brevidade no exemplo de limpeza)
    # ... Lógica de Matplotlib permanece igual, utilizando os nomes de colunas limpos ...

if __name__ == "__main__":
    processar_relatorio()