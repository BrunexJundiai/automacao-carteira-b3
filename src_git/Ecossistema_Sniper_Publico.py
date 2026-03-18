# ================================================================= #
# ECOSSISTEMA SNIPER B3 - SHOWCASE VERSION (PUBLIC REPOSITORY)      #
# ================================================================= #
# Autor: Bruno Felipe (BrunexJundiai)
# Descrição: Versão simplificada do Ecossistema Master Quantitativo (V3.0).
# Demonstração da arquitetura Core-Satellite (Ações + Cripto), 
# Cotação Sintética (Cross-currency) e Regressão Linear.
# 
# NOTA: Credenciais, envio de webhooks via Telegram e a renderização 
# avançada de Lâminas Multi-page em PDF foram abstraídos por segurança 
# e proteção de propriedade intelectual.
# ================================================================= #

import os
import gspread
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

# ==========================================
# 1. CONFIGURAÇÕES E CREDENCIAIS (MASCARADAS)
# ==========================================
CAMINHO_JSON = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "caminho/para/sua/credencial.json")
ID_PLANILHA = os.getenv("SPREADSHEET_ID", "SEU_ID_DE_PLANILHA_AQUI")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_TOKEN_AQUI")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "SEU_CHAT_ID_AQUI")

def autenticar_google():
    if os.path.exists(CAMINHO_JSON):
        return gspread.service_account(filename=CAMINHO_JSON)
    raise FileNotFoundError("JSON de credenciais não configurado.")

def enviar_telegram(mensagem, caminho_arquivo=None, modo_texto="HTML"):
    # Lógica de requests e envio de documentos abstraída para o repositório público
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
    
    # TRUQUE DE ENGENHARIA: UNFORMATTED_VALUE evita bugs de leitura de moedas e milhares do GSheets
    df_raw = pd.DataFrame(aba.get_all_records(value_render_option='UNFORMATTED_VALUE'))
    
    # [BLOCO DE CÓDIGO RESUMIDO] Tratamento numérico
    df_raw['Qtd_Ajustada'] = df_raw.apply(lambda x: -x['Qtd'] if str(x['Tipo']).upper() == 'VENDA' else x['Qtd'], axis=1)
    
    # Tratamento de Tickers (B3 recebe .SA, Cripto com hífen é mantido intacto)
    if 'Ativo' in df_raw.columns:
        df_raw['Ativo'] = df_raw['Ativo'].str.strip().str.upper().apply(lambda x: x if x.endswith('.SA') or '-' in x else f"{x}.SA")

    carteira_mestre = df_raw.groupby('Ativo').agg(
        Qtd_Total=('Qtd_Ajustada', 'sum')
    ).reset_index()

    # --- DOWNLOAD YAHOO FINANCE & COTAÇÃO SINTÉTICA CRIPTO ---
    tickers = carteira_mestre['Ativo'].tolist()
    
    # Lógica Sintética: Contorna o delisting de pares BRL gerando cotação em tempo real via Dólar
    tem_btc_brl = False
    if 'BTC-BRL' in tickers:
        tickers.remove('BTC-BRL')
        tickers.extend(['BTC-USD', 'USDBRL=X'])
        tem_btc_brl = True

    dados_mercado = yf.download(tickers, period="180d", progress=False)['Close']
    
    if tem_btc_brl:
        dados_mercado['USDBRL=X'] = dados_mercado['USDBRL=X'].ffill() # Preenche FDS do câmbio
        dados_mercado['BTC-BRL'] = dados_mercado['BTC-USD'] * dados_mercado['USDBRL=X']
        tickers = carteira_mestre['Ativo'].tolist() # Restaura a lista original

    # ==========================================
    # MÓDULO 1: RADAR SNIPER (TÁTICO)
    # ==========================================
    alertas_radar = []
    for t in tickers:
        try:
            precos = dados_mercado[t].dropna() if len(tickers) > 1 else dados_mercado.dropna()
            rsi = float(calcular_rsi(precos).iloc[-1])
            upside = calcular_vies_preditivo(precos)
            
            # Lógica Demonstrativa: Compra Extrema (Ignora cripto nos alertas diários para não gerar ruído no FDS)
            if rsi <= 25 and '-' not in t:
                alertas_radar.append(f"ALERTA TÁTICO: {t} | RSI {rsi:.1f} | Viés 30d: {upside:.1f}%")
        except: continue

    # ==========================================
    # MÓDULO 2 e 3: DASHBOARD E APORTES (ESTRATÉGICO)
    # ==========================================
    # O processamento aplica o filtro anti "faca caindo", separando 
    # visualmente a alocação da B3 (Core) do acompanhamento Cripto (Satélite).
    
    analise_ap = []
    for t in tickers:
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
    # GERAÇÃO DE RELATÓRIOS E PDFS (ABSTRAÍDO)
    # ==========================================
    # Em produção, este script utiliza Matplotlib e PdfPages para gerar 
    # relatórios de múltiplas lâminas (Trend Following Cripto e DRE B3) 
    # e aciona os webhooks do Telegram Bot API.
    print("Processamento Quantitativo concluído. Preparando envio de relatórios...")

if __name__ == "__main__":
    rodar_ecossistema()