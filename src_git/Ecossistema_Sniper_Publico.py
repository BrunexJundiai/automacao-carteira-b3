# ================================================================= #
# ECOSSISTEMA SNIPER B3 - SHOWCASE VERSION (PUBLIC REPOSITORY)      #
# ================================================================= #
# Autor: Bruno Felipe (BrunexJundiai)
# Descrição: Versão simplificada do Ecossistema Master Quantitativo.
# As credenciais e blocos de geração de PDF foram abstraídos por 
# segurança e proteção de propriedade intelectual (Portfólio).
# ================================================================= #

import os
import gspread
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# ==========================================
# 1. CONFIGURAÇÕES E CREDENCIAIS (MASCARADAS)
# ==========================================
# TODO: Insira suas credenciais locais e IDs para rodar o projeto
CAMINHO_JSON = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "caminho/para/sua/credencial.json")
ID_PLANILHA = os.getenv("SPREADSHEET_ID", "SEU_ID_DE_PLANILHA_AQUI")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_TOKEN_AQUI")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "SEU_CHAT_ID_AQUI")

def autenticar_google():
    if os.path.exists(CAMINHO_JSON):
        return gspread.service_account(filename=CAMINHO_JSON)
    raise FileNotFoundError("JSON de credenciais não configurado.")

def enviar_telegram(mensagem, caminho_arquivo=None, modo_texto="HTML"):
    url_text = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    url_doc = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        requests.post(url_text, json={"chat_id": CHAT_ID, "text": mensagem, "parse_mode": modo_texto})
        # Lógica de envio de documento abstraída
    except Exception as e:
        pass

# ==========================================
# 2. FUNÇÕES MATEMÁTICAS CORE (QUANTITATIVO)
# ==========================================
def calcular_rsi(dados_preco, periodos=14):
    delta = dados_preco.diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=periodos).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=periodos).mean()
    rs = ganho / (perda + 1e-9)
    return 100 - (100 / (1 + rs))

def calcular_vies_preditivo(serie_precos, dias_frente=30):
    """ Regressão Linear Simples para projetar viés de 30 dias """
    try:
        y = serie_precos.values
        x = np.arange(len(y))
        coeffs = np.polyfit(x, y, 1)
        pred = coeffs[0] * (len(y) + dias_frente) + coeffs[1]
        return ((pred / y[-1]) - 1) * 100
    except:
        return 0.0

# ==========================================
# 3. MOTOR CENTRAL DO ECOSSISTEMA
# ==========================================
def rodar_ecossistema():
    agora = datetime.now()
    if agora.weekday() > 4 or agora.hour < 10 or agora.hour >= 18:
        print("Fora do horário comercial da B3.")
        return

    # --- EXTRAÇÃO ÚNICA (ETL) ---
    gc = autenticar_google()
    aba = gc.open_by_key(ID_PLANILHA).sheet1
    df_raw = pd.DataFrame(aba.get_all_records())
    
    # [BLOCO DE CÓDIGO RESUMIDO] Tratamento numérico e padronização
    df_raw['Qtd_Ajustada'] = df_raw.apply(lambda x: -x['Qtd'] if str(x['Tipo']).upper() == 'VENDA' else x['Qtd'], axis=1)
    df_raw['Vol_Ajustado'] = df_raw.apply(lambda x: -x['Qtd']*x['Preco_Unitario'] if str(x['Tipo']).upper() == 'VENDA' else x['Qtd']*x['Preco_Unitario'], axis=1)

    carteira_mestre = df_raw.groupby('Ativo').agg(
        Qtd_Total=('Qtd_Ajustada', 'sum'),
        Investido_Liquido=('Vol_Ajustado', 'sum')
    ).reset_index()

    # Preço Médio e DOWNLOAD YAHOO FINANCE
    tickers = carteira_mestre['Ativo'].tolist()
    dados_mercado = yf.download(tickers, period="180d", progress=False)['Close']

    # ==========================================
    # MÓDULO 1: RADAR SNIPER (TÁTICO)
    # ==========================================
    alertas_radar = []
    for _, row in carteira_mestre.iterrows():
        t = row['Ativo']
        try:
            precos = dados_mercado[t].dropna() if len(tickers) > 1 else dados_mercado.dropna()
            p_atual = float(precos.iloc[-1])
            rsi = float(calcular_rsi(precos).iloc[-1])
            upside = calcular_vies_preditivo(precos)
            
            # Lógica Pública Demonstrativa: Compra Extrema
            if rsi <= 25:
                alertas_radar.append(f"ALERTA TÁTICO: {t} | RSI {rsi:.1f} | Viés 30d: {upside:.1f}%")
        except: continue

    # ==========================================
    # MÓDULO 2 e 3: DASHBOARD E APORTES (ESTRATÉGICO)
    # ==========================================
    analise_ap = []
    for _, row in carteira_mestre.iterrows():
        t = row['Ativo']
        try:
            precos = dados_mercado[t].dropna() if len(tickers) > 1 else dados_mercado.dropna()
            vies = calcular_vies_preditivo(precos)
            analise_ap.append({'Ativo': t, 'Vies_Preditivo_%': vies})
        except: continue

    df_ap = pd.DataFrame(analise_ap)
    
    def definir_acao_quantitativa(row):
        if row['Vies_Preditivo_%'] < 0: return "BLOQUEADO - FACA CAINDO"
        elif row['Vies_Preditivo_%'] > 0: return "COMPRA"
        return "AGUARDAR"

    if not df_ap.empty:
        df_ap['Ação'] = df_ap.apply(definir_acao_quantitativa, axis=1)
        
    # ==========================================
    # GERAÇÃO DE RELATÓRIOS E PDFS
    # ==========================================
    # Nota de Segurança/Portfólio:
    # A lógica complexa de renderização visual (Matplotlib/Seaborn)
    # e a estrutura detalhada das mensagens de Telegram foram abstraídas
    # nesta versão pública para proteger a propriedade intelectual.
    print("Módulos processados com sucesso. Preparando envio de webhooks...")

if __name__ == "__main__":
    rodar_ecossistema()