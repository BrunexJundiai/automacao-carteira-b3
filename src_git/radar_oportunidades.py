import os
import gspread
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# ==========================================
# CONFIGURAÇÕES (MASCARADAS VIA OS.ENVIRON)
# ==========================================
ID_PLANILHA = os.environ.get('ID_PLANILHA_B3')
CAMINHO_JSON = os.environ.get('CAMINHO_CREDENCIAIS_GOOGLE')
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def enviar_mensagem_telegram(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"})
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")

def conectar_ao_google():
    return gspread.service_account(filename=CAMINHO_JSON)

def calcular_rsi(dados_preco, periodos=14):
    delta = dados_preco.diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=periodos).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=periodos).mean()
    rs = ganho / (perda + 1e-9)
    return 100 - (100 / (1 + rs))

def buscar_dados():
    gc = conectar_ao_google()
    sh = gc.open_by_key(ID_PLANILHA)
    ws = sh.worksheet('ControleAcoes')
    raw_records = ws.get_all_records()
    
    df = pd.DataFrame.from_records(raw_records)
    compras = df[df['Tipo'].str.upper() == 'COMPRA'].copy()
    compras['Qtd'] = pd.to_numeric(compras['Qtd'], errors='coerce')
    compras['Preco_Unitario'] = pd.to_numeric(compras['Preco_Unitario'], errors='coerce')
    compras['Vol'] = compras['Qtd'] * compras['Preco_Unitario']

    agrupado = compras.groupby('Ativo').agg({'Qtd': 'sum', 'Vol': 'sum'}).reset_index()
    agrupado['pm'] = agrupado['Vol'] / agrupado['Qtd']
    return [{'ticker': r['Ativo'], 'preco_medio': r['pm']} for _, r in agrupado.iterrows()]

def rodar_radar(carteira):
    agora = datetime.now().strftime('%d/%m/%Y %H:%M')
    alertas = []
    tickers = [f"{a['ticker']}.SA" if not ".SA" in str(a['ticker']) else a['ticker'] for a in carteira]
    
    print(f"📡 Baixando dados da B3 para {len(tickers)} ativos...")
    dados = yf.download(tickers, period="60d", progress=False)['Close']

    for ativo in carteira:
        t = ativo['ticker']
        t_yf = t if ".SA" in str(t) else f"{t}.SA"
        pm = ativo['preco_medio']
        
        try:
            if isinstance(dados, pd.DataFrame):
                precos = dados[t_yf].dropna()
            else:
                precos = dados.dropna()

            p_atual = float(precos.iloc[-1])
            rsi = float(calcular_rsi(precos).iloc[-1])

            if rsi <= 25 and p_atual < (pm * 0.85):
                alertas.append(f"<b>{t}</b> - 🟢 COMPRA AGRESSIVA\nPreço: R$ {p_atual:.2f} | RSI: {rsi:.1f}\nRegra: RSI Sobrevendido + Preço 15% abaixo do PM.")
            elif rsi >= 75 and p_atual > (pm * 1.20):
                alertas.append(f"<b>{t}</b> - 🔴 VENDA (LUCRO)\nPreço: R$ {p_atual:.2f} | RSI: {rsi:.1f}\nRegra: RSI Sobrecomprado + Lucro superior a 20%.")
        except:
            continue

    if not alertas:
        msg = f"⚖️ <b>RADAR B3: ZONA NEUTRA</b>\n🕒 {agora}\n\nStatus: Mercado em equilíbrio técnico."
    else:
        msg = f"🚨 <b>RADAR B3 - MODO SNIPER</b> 🚨\n🕒 {agora}\n\n" + "\n\n".join(alertas)
    
    enviar_mensagem_telegram(msg)

if __name__ == "__main__":
    try:
        minha_carteira = buscar_dados()
        rodar_radar(minha_carteira)
    except Exception as e:
        print(f"Erro na execução: {e}")