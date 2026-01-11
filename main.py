
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf

#python -m streamlit run main.py
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao=yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(interval="1d", start ="2022-01-01", end = "2024-07-01")
    cotacoes_acao=cotacoes_acao["Close"]
    
    return cotacoes_acao

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("tickers.csv")  
    tickers = list(base_tickers["Ticker"])
    tickers = [item + ".SA" for item in tickers]
    return tickers


acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)



st.write("""
### App Preço de Açõess
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos
""")

st.sidebar.header("Filtros")

#Filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar",   dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})
    
#Filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_data = st.sidebar.slider("Selecione o periodo", 
                  min_value=data_inicial, 
                  max_value=data_final,
                  value=(data_inicial,data_final))
dados = dados.loc[intervalo_data[0]:intervalo_data[1]]


#gráfico
st.line_chart(dados)

texto_performance_ativos = ""

if len(lista_acoes)==0:
    lista_acoes =list(dados.columns)
elif len(lista_acoes)==1:
    dados = dados.rename(columns ={"Close": acao_unica})

for ativo in lista_acoes:
    perfomance_ativo = dados[ativo].iloc[-1] / dados[ativo].iloc[0] -1
    perfomance_ativo = float(perfomance_ativo)
    
    if perfomance_ativo > 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{ativo}: :green[{perfomance_ativo: .1%}]"
    elif perfomance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{ativo}: :red[{perfomance_ativo: .1%}]"
    else:
        texto_performance_ativos = texto_performance_ativos + f"  \n{ativo}: {perfomance_ativo: .1%}"
st.write(f"""
### Performance dos Ativos
Essa foi a perfomance de cada ativo no período selecionado:
         
{texto_performance_ativos}
""")