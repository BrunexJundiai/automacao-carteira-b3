# ================================================================= #
# ECOSSISTEMA SNIPER B3 - SHOWCASE VERSION (PUBLIC REPOSITORY)      #
# ================================================================= #
# Autor: Bruno Felipe
# Descrição: Versão estrutural do Ecossistema Master Quantitativo & IA (V4.0).
# Demonstra a arquitetura Core-Satellite (Ações + Cripto), ETL otimizado,
# Cotação Sintética (Cross-currency), Regressão Linear e a injeção 
# de Agentes de Inteligência Artificial (LangGraph/LLMs) na tomada de decisão.
# 
# NOTA DE SEGURANÇA: Credenciais, orquestração de Agentes IA (LangChain), 
# envio de webhooks via Telegram e a renderização complexa de Lâminas 
# Multi-page em PDF (Treemaps) foram abstraídos para proteger a 
# propriedade intelectual e chaves privadas.
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
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "SUA_CHAVE_LLM_AQUI")

def autenticar_google():
    """ Conecta à API do Google Cloud """
    if os.path.exists(CAMINHO_JSON):
        return gspread.service_account(filename=CAMINHO_JSON)
    raise FileNotFoundError("JSON de credenciais não configurado.")

def enviar_telegram(mensagem, caminho_arquivo=None, modo_texto="HTML"):
    """ Abstração: Envio de relatórios e sinais intraday para o celular """
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
    """ Regressão Linear Simples para projetar viés (Upside) de 30 dias """
    try:
        y = serie_precos.values
        x = np.arange(len(y))
        coeffs = np.polyfit(x, y, 1)
        pred = coeffs[0] * (len(y) + dias_frente) + coeffs[1]
        return ((pred / y[-1]) - 1) * 100
    except:
        return 0.0

def calcular_macd(dados_preco):
    """ Moving Average Convergence Divergence para capturar reversões """
    exp1 = dados_preco.ewm(span=12, adjust=False).mean()
    exp2 = dados_preco.ewm(span=26, adjust=False).mean()
    macd_linha = exp1 - exp2
    macd_sinal = macd_linha.ewm(span=9, adjust=False).mean()
    macd_hist = macd_linha - macd_sinal
    return macd_linha.iloc[-1], macd_sinal.iloc[-1], macd_hist.iloc[-1]

def calcular_bollinger(dados_preco, janela=20, desvios=2):
    """ Limites dinâmicos de preço para identificar suporte e resistência """
    sma = dados_preco.rolling(window=janela).mean()
    std = dados_preco.rolling(window=janela).std()
    bollinger_sup = sma + (std * desvios)
    bollinger_inf = sma - (std * desvios)
    return bollinger_sup.iloc[-1], bollinger_inf.iloc[-1]

# ==========================================
# 3. ABSTRAÇÃO DO MOTOR DE IA (MULTI-AGENT)
# ==========================================
def invocar_agente_ia(ativo, dados_quantitativos):
    """
    ABSTRAÇÃO DE ARQUITETURA: 
    Na versão de produção, este método aciona um grafo de estado (LangGraph)
    que injeta as métricas financeiras num LLM (Llama 3 via Groq), faz 
    scraping de notícias em tempo real (RAG) e gera um Dossiê Fundamentalista
    formatado em Markdown para validar matematicamente a decisão de aporte.
    """
    return f"🤖 [MOCK IA] Dossiê de Value Investing gerado com sucesso para {ativo}."

# ==========================================
# 4. MOTOR CENTRAL DO ECOSSISTEMA (ETL)
# ==========================================
def rodar_ecossistema():
    agora = datetime.now()
    if agora.weekday() > 4 or agora.hour < 10 or agora.hour >= 18:
        print("Fora do horário comercial da B3. Sistema em repouso (Economia de API).")
        return

    # --- EXTRAÇÃO ÚNICA E BLINDADA (ETL) ---
    gc = autenticar_google()
    aba = gc.open_by_key(ID_PLANILHA).sheet1
    
    # TRUQUE DE ENGENHARIA: UNFORMATTED_VALUE evita bugs severos de leitura de moedas e milhares
    df_raw = pd.DataFrame(aba.get_all_records(value_render_option='UNFORMATTED_VALUE'))
    
    # Tratamento Numérico Base
    df_raw['Qtd_Ajustada'] = df_raw.apply(lambda x: -x['Qtd'] if str(x['Tipo']).upper() == 'VENDA' else x['Qtd'], axis=1)
    
    # Tratamento de Tickers (B3 recebe .SA, Cripto com hífen é mantido intacto)
    if 'Ativo' in df_raw.columns:
        df_raw['Ativo'] = df_raw['Ativo'].str.strip().str.upper().apply(lambda x: x if x.endswith('.SA') or '-' in x else f"{x}.SA")

    carteira_mestre = df_raw.groupby('Ativo').agg(Qtd_Total=('Qtd_Ajustada', 'sum')).reset_index()

    # --- DOWNLOAD YAHOO FINANCE & COTAÇÃO SINTÉTICA CRIPTO ---
    tickers = carteira_mestre['Ativo'].tolist()
    
    # Lógica Sintética: Contorna o delisting de pares BRL gerando cotação em tempo real via Dólar
    tem_btc_brl = False
    if 'BTC-BRL' in tickers:
        tickers.remove('BTC-BRL')
        tickers.extend(['BTC-USD', 'USDBRL=X'])
        tem_btc_brl = True

    # Otimização: threads=False impede OperationalError de concorrência no SQLite de Cache
    dados_mercado = yf.download(tickers, period="180d", progress=False, threads=False)['Close']
    
    if tem_btc_brl:
        dados_mercado['USDBRL=X'] = dados_mercado['USDBRL=X'].ffill() # Preenche FDS do câmbio
        dados_mercado['BTC-BRL'] = dados_mercado['BTC-USD'] * dados_mercado['USDBRL=X']
        tickers = carteira_mestre['Ativo'].tolist() # Restaura a lista original

    # ==========================================
    # MÓDULO 1: RADAR SNIPER (TÁTICO INTRADAY)
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
            macd_l, macd_s, macd_hist = calcular_macd(precos)
            
            analise_ap.append({'Ativo': t, 'Vies_Preditivo_%': vies, 'MACD_Hist': macd_hist})
        except: continue

    df_ap = pd.DataFrame(analise_ap)
    
    def definir_acao_quantitativa(row):
        """ Filtro de Proteção de Capital """
        if row['Vies_Preditivo_%'] < 0: return "BLOQUEADO - FACA CAINDO"
        elif row['Vies_Preditivo_%'] > 0: return "COMPRA"
        return "AGUARDAR"

    if not df_ap.empty:
        df_ap['Ação'] = df_ap.apply(definir_acao_quantitativa, axis=1)
        
        # Simula a chamada da IA para o ativo vencedor do ranking quantitativo
        alvo_simulado = df_ap[df_ap['Ação'] == 'COMPRA'].iloc[0]['Ativo'] if not df_ap[df_ap['Ação'] == 'COMPRA'].empty else "Nenhum"
        if alvo_simulado != "Nenhum":
            parecer_ia = invocar_agente_ia(alvo_simulado, df_ap.iloc[0].to_dict())
        
    # ==========================================
    # GERAÇÃO DE RELATÓRIOS E PDFS (ABSTRAÍDO)
    # ==========================================
    # Em produção, este script utiliza Matplotlib, Seaborn e Squarify (Treemap) 
    # para gerar relatórios visuais de múltiplas lâminas e aciona webhooks do Telegram.
    print("Processamento Quantitativo e de IA concluído. Preparando envio de relatórios...")

if __name__ == "__main__":
    rodar_ecossistema()