# =================================================================
# MÓDULO 04: DASHBOARD ANALÍTICO E MODELAGEM PREDITIVA (Avançado)
# =================================================================
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from google.colab import auth
import gspread
from google.auth import default
import warnings

warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

# 1. AUTENTICAÇÃO E EXTRAÇÃO DOS DADOS
auth.authenticate_user()
creds, _ = default()
gc = gspread.authorize(creds)

# ⚠️ COLOQUE SEU LINK AQUI ANTES DE RODAR NO COLAB
LINK_PLANILHA = "COLE_O_LINK_DA_SUA_PLANILHA_AQUI"

print("📡 Conectando ao Banco de Dados e B3...")
planilha = gc.open_by_url(LINK_PLANILHA)
aba = planilha.sheet1
dados_planilha = aba.get_all_records()

df_transacoes = pd.DataFrame(dados_planilha)
df_transacoes['Ativo'] = df_transacoes['Ativo'].astype(str).str.strip().str.upper()
df_transacoes['Ativo'] = df_transacoes['Ativo'].apply(lambda x: x if x.endswith('.SA') else f"{x}.SA")

for col in ['Qtd', 'Preco_Unitario']:
    df_transacoes[col] = df_transacoes[col].astype(str).str.replace('R$', '').str.replace('%', '').str.replace(',', '.').astype(float)

# Filtra apenas compras e calcula totais
df_compras = df_transacoes[df_transacoes['Tipo'].str.upper() == 'COMPRA'].copy()
df_compras['Total_Gasto'] = df_compras['Qtd'] * df_compras['Preco_Unitario']

# Agrupamento da Carteira
carteira = df_compras.groupby('Ativo').agg(
    Qtd_Total=('Qtd', 'sum'),
    Total_Investido=('Total_Gasto', 'sum')
).reset_index()

carteira['Preco_Medio'] = carteira['Total_Investido'] / carteira['Qtd_Total']

# 2. ENRIQUECIMENTO DE DADOS, PREVISÃO E DIVIDENDOS
resultados = []
hoje = datetime.now()

print("🧠 Rodando Modelos Preditivos e Análise de Dividendos...")
for index, row in carteira.iterrows():
    ticker = row['Ativo']
    qtd = row['Qtd_Total']
    pm = row['Preco_Medio']
    investido = row['Total_Investido']
    
    stock = yf.Ticker(ticker)
    
    try:
        hist_1d = stock.history(period="1d")
        preco_atual = float(hist_1d['Close'].iloc[-1])
    except:
        preco_atual = pm
        
    valor_atual = qtd * preco_atual
    lucro_rs = valor_atual - investido
    lucro_pct = (lucro_rs / investido) * 100
    
    dividendos_totais = stock.dividends
    div_ultimos_12m = 0
    projecao_proximo_div = 0
    data_prevista = "Desconhecida"
    
    if not dividendos_totais.empty:
        dividendos_totais.index = dividendos_totais.index.tz_localize(None)
        div_12m = dividendos_totais[dividendos_totais.index > (hoje - timedelta(days=365))]
        div_ultimos_12m = div_12m.sum()
        
        if len(div_12m) > 0:
            projecao_proximo_div_por_acao = div_12m.mean()
            projecao_proximo_div = projecao_proximo_div_por_acao * qtd
            intervalo_dias = 365 / len(div_12m)
            ultima_data = div_12m.index[-1]
            data_prevista_dt = ultima_data + timedelta(days=intervalo_dias)
            data_prevista = data_prevista_dt.strftime('%m/%Y')

    hist_6m = stock.history(period="6mo")
    if len(hist_6m) > 30:
        x = np.arange(len(hist_6m))
        y = hist_6m['Close'].values
        tendencia = np.polyfit(x, y, 1)
        funcao_tendencia = np.poly1d(tendencia)
        preco_projetado_30d = funcao_tendencia(len(hist_6m) + 30)
        movimento_esperado = ((preco_projetado_30d / preco_atual) - 1) * 100
    else:
        preco_projetado_30d = preco_atual
        movimento_esperado = 0
        
    resultados.append({
        'Ativo': ticker.replace('.SA', ''),
        'Total Investido (R$)': investido,
        'Valor Atual (R$)': valor_atual,
        'Lucro/Perda (R$)': lucro_rs,
        'Lucro (%)': lucro_pct,
        'Div. Últimos 12m/Ação (R$)': div_ultimos_12m,
        'Estimativa Próx. Div. (R$)': projecao_proximo_div,
        'Previsão Mês Próx. Div.': data_prevista,
        'Projeção 30d (R$)': preco_projetado_30d,
        'Viés Tendência': 'Alta 🟢' if movimento_esperado > 0 else 'Baixa 🔴'
    })

df_resultado = pd.DataFrame(resultados)

# 3. EXIBIÇÃO DO PAINEL GERENCIAL
print("\n" + "="*100)
print(f"📊 DRE GERAL DA CARTEIRA")
print("="*100)
print(f"💰 Total Gasto Histórico: R$ {df_resultado['Total Investido (R$)'].sum():,.2f}")
print(f"📈 Valor Atual da Carteira: R$ {df_resultado['Valor Atual (R$)'].sum():,.2f}")
lucro_geral = df_resultado['Lucro/Perda (R$)'].sum()
print(f"⚖️ Resultado Global Não-Realizado: R$ {lucro_geral:,.2f} ({'Lucro 🟢' if lucro_geral > 0 else 'Prejuízo 🔴'})")
print("="*100 + "\n")

display(df_resultado.round(2))

# 4. VISUALIZAÇÕES (DASHBOARDS COM RÓTULOS)
fig, axs = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Visão Analítica da Carteira', fontsize=18, fontweight='bold')

# Gráfico 1: Peso do Investimento
axs[0, 0].pie(df_resultado['Total Investido (R$)'], labels=df_resultado['Ativo'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
axs[0, 0].set_title('Composição do Patrimônio Investido')

# Gráfico 2: Lucro / Perda por Ativo com Rótulos de R$
cores_lucro = ['green' if x > 0 else 'red' for x in df_resultado['Lucro/Perda (R$)']]
sns.barplot(x='Ativo', y='Lucro/Perda (R$)', data=df_resultado, ax=axs[0, 1], palette=cores_lucro)
axs[0, 1].set_title('Lucro / Prejuízo por Empresa (R$)')
axs[0, 1].axhline(0, color='black', linewidth=1)

# Adicionando os textos Verde/Vermelho nas barras
for p in axs[0, 1].patches:
    height = p.get_height()
    if height != 0:
        y_pos = height + (height * 0.05) if height > 0 else height + (height * 0.05)
        cor_texto = 'green' if height > 0 else 'red'
        axs[0, 1].annotate(f'R$ {height:.2f}', (p.get_x() + p.get_width() / 2., y_pos),
                           ha='center', va='bottom' if height > 0 else 'top',
                           color=cor_texto, fontweight='bold', fontsize=10)

# Gráfico 3: Previsão de Dividendos (Ordenado por Data)
# Criando uma cópia para ordenar cronologicamente
df_div = df_resultado.copy()
df_div['Data_Real'] = pd.to_datetime(df_div['Previsão Mês Próx. Div.'], format='%m/%Y', errors='coerce').fillna(pd.Timestamp.max)
df_div = df_div.sort_values('Data_Real').reset_index(drop=True)

sns.barplot(x='Ativo', y='Estimativa Próx. Div. (R$)', data=df_div, ax=axs[1, 0], palette="Blues_d")
axs[1, 0].set_title('Estimativa de Recebimento no Próximo Dividendo (Ordem Cronológica)')
for i, v in enumerate(df_div['Estimativa Próx. Div. (R$)']):
    if v > 0:
        axs[1, 0].text(i, v + (v * 0.02), f"R$ {v:.2f}\n{df_div['Previsão Mês Próx. Div.'].iloc[i]}", 
                       ha='center', va='bottom', fontsize=9, fontweight='bold')

# Gráfico 4: Previsão de Tendência 30 Dias com Rótulos de R$
x = np.arange(len(df_resultado))
width = 0.35
barra1 = axs[1, 1].bar(x - width/2, df_resultado['Valor Atual (R$)'] / carteira['Qtd_Total'], width, label='Preço Atual', color='gray')
barra2 = axs[1, 1].bar(x + width/2, df_resultado['Projeção 30d (R$)'], width, label='Projeção 30 Dias', color='orange')
axs[1, 1].set_xticks(x)
axs[1, 1].set_xticklabels(df_resultado['Ativo'])
axs[1, 1].set_title('Viés de Movimento: Preço Atual vs 30 Dias')
axs[1, 1].legend()

# Função para colocar rótulos nas barras do gráfico 4
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        axs[1, 1].annotate(f'R$ {height:.2f}',
                           xy=(rect.get_x() + rect.get_width() / 2, height),
                           xytext=(0, 3),  # 3 points vertical offset
                           textcoords="offset points",
                           ha='center', va='bottom', fontsize=9, fontweight='bold')

autolabel(barra1)
autolabel(barra2)

# Ajuste de layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()