# =================================================================
# CONTROLE TRANSACIONAL DE CARTEIRA
# =================================================================
import pandas as pd
import yfinance as yf
from datetime import datetime
from google.colab import auth
import gspread
from google.auth import default
import warnings

warnings.filterwarnings('ignore')

# 1. AUTENTICAÇÃO E EXTRAÇÃO DOS DADOS
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

LINK_PLANILHA = "COLE_AQUI_O_LINK_DA_SUA_PLANILHA"

print("Lendo histórico de transações no Google Drive...")
planilha = gc.open_by_url(LINK_PLANILHA)
aba = planilha.sheet1
dados_planilha = aba.get_all_records()

if not dados_planilha:
    print("❌ Sua planilha está vazia. Adicione suas transações e rode novamente.")
else:
    # 2. TRANSFORMAÇÃO E CÁLCULO DE PREÇO MÉDIO (ETL)
    df_transacoes = pd.DataFrame(dados_planilha)

    # Limpeza e tipagem dos dados
    df_transacoes['Ativo'] = df_transacoes['Ativo'].astype(str).str.strip().str.upper()
    df_transacoes['Ativo'] = df_transacoes['Ativo'].apply(lambda x: x if x.endswith('.SA') else f"{x}.SA")

    for col in ['Qtd', 'Preco_Unitario', 'Target_%']:
        df_transacoes[col] = df_transacoes[col].astype(str).str.replace('R$', '').str.replace('%', '').str.replace(',', '.').astype(float)

    # Filtrar apenas compras (futuramente você pode adicionar lógica de venda aqui)
    df_compras = df_transacoes[df_transacoes['Tipo'].str.upper() == 'COMPRA'].copy()
    df_compras['Total_Gasto'] = df_compras['Qtd'] * df_compras['Preco_Unitario']

    # Agrupamento: Calculando o Preço Médio Dinâmico
    carteira_agrupada = df_compras.groupby('Ativo').apply(
        lambda x: pd.Series({
            'Qtd_Total': x['Qtd'].sum(),
            'Preco_Medio': x['Total_Gasto'].sum() / x['Qtd'].sum() if x['Qtd'].sum() > 0 else 0,
            'Target_%': x['Target_%'].max()
        })
    ).reset_index()

    # Convertendo de volta para dicionário para o motor de análise
    minha_carteira = {}
    for _, row in carteira_agrupada.iterrows():
        minha_carteira[row['Ativo']] = {
            'Qtd': row['Qtd_Total'],
            'Preco_Medio': row['Preco_Medio'],
            'Target_%': row['Target_%']
        }

    # 3. MOTOR DE ANÁLISE DO MERCADO
    print(f"Extraindo dados ao vivo da B3 - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    dados_processados = []
    tickers = list(minha_carteira.keys())
    dados_mercado = yf.download(tickers, period="1d", progress=False)['Close']

    for ticker in tickers:
        try:
            if len(tickers) > 1:
                preco_atual = float(dados_mercado[ticker].iloc[0])
            else:
                preco_atual = float(dados_mercado.iloc[0])
        except:
            preco_atual = minha_carteira[ticker]['Preco_Medio']

        stock = yf.Ticker(ticker)
        info = stock.info

        nome_empresa = info.get('shortName', info.get('longName', 'N/A'))
        ramo = info.get('industry', info.get('sector', 'N/A'))
        dy_pct = round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0.0
        pvp = round(info.get('priceToBook', 0), 2) if info.get('priceToBook') else 0.0

        qtd = minha_carteira[ticker]['Qtd']
        pm = minha_carteira[ticker]['Preco_Medio']
        target = minha_carteira[ticker]['Target_%']

        valor_posicao = qtd * preco_atual
        rentabilidade = ((preco_atual / pm) - 1) * 100 if pm > 0 else 0

        dados_processados.append({
            'Ativo': ticker.replace('.SA', ''),
            'Empresa': nome_empresa,
            'Ramo/Setor': ramo,
            'Qtd': qtd,
            'Preço Atual': round(preco_atual, 2),
            'Seu PM': round(pm, 2),
            'Rentab. (%)': round(rentabilidade, 2),
            'DY (%)': dy_pct,
            'P/VP': pvp,
            'Valor (R$)': round(valor_posicao, 2),
            'Meta (%)': target
        })

    df = pd.DataFrame(dados_processados)

    # 4. BALANCEAMENTO E RECOMENDAÇÃO
    patrimonio_total = df['Valor (R$)'].sum()
    df['Peso Atual (%)'] = round((df['Valor (R$)'] / patrimonio_total) * 100, 2) if patrimonio_total > 0 else 0
    df['Distância Meta (%)'] = round(df['Peso Atual (%)'] - df['Meta (%)'], 2)
    df = df.sort_values(by='Distância Meta (%)', ascending=True)

    def definir_acao(distancia):
        if distancia < -2.0: return "Forte Compra"
        elif distancia < 0:  return "Compra Marginal"
        else:                return "Aguardar"

    df['Ação'] = df['Distância Meta (%)'].apply(definir_acao)

    # 5. EXIBIÇÃO DO DASHBOARD
    print("\n" + "="*105)
    print(f"PAINEL INTELIGENTE DA CARTEIRA | PATRIMÔNIO TOTAL: R$ {patrimonio_total:,.2f}")
    print("="*105 + "\n")

    colunas_visuais = ['Ativo', 'Empresa', 'Ramo/Setor', 'Qtd', 'Preço Atual', 'Seu PM', 'Rentab. (%)', 'DY (%)', 'P/VP', 'Peso Atual (%)', 'Distância Meta (%)', 'Ação']
    display(df[colunas_visuais])

    print("\nInsight Automático de Aporte:")
    ativo_compra = df.iloc[0]['Ativo']
    distancia = df.iloc[0]['Distância Meta (%)']

    if distancia < 0:
        print(f"👉 Ação recomendada para hoje: {ativo_compra} (Está {abs(distancia)}% abaixo do peso ideal).")
    else:
        print(f"👉 Sua carteira está balanceada perfeitamente.")