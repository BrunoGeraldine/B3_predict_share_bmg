import streamlit as st
import yfinance as yf
from datetime import date
import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go

# Craindo as data
DATA_INICIO = '2017-01-01'
DATA_FIM = date.today().strftime('%Y-%m-%d') #Formatando a data

#Chamando o Streamlit
st.title('Analise de ações')

#Criando a sidebar (ações)
st.sidebar.header('Escolha a ação')

#Criando o slider dos dias
n_dias = st.slider('Quantidade de dias de previsão', 30, 365)

#Função das informações da ação e a sigla
def pegar_dados_acoes():
    path = '../data/acoes.csv'
    return pd.read_csv(path, delimiter=';')

df = pegar_dados_acoes()

acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação: ', acao)

df_acao = df[df['snome'] == nome_acao_escolhida]
acao_escolhida = df_acao.iloc[0]['sigla_acao']
acao_escolhida = acao_escolhida + '.SA' #formato esperado pelo yfinance

#st.write(df_acao.iloc[0]['sigla_acao']) #Captura apenas a sigla da ação

#Função captura valores online
@st.cache #utiliza a função e guarda em cache para agilizar o dashboard (tipo um arq temporario)
def pegar_valores_online(sigla_acao):
    df = yf.download(sigla_acao, DATA_INICIO, DATA_FIM) # EXECUTA DOWNLOAD ONLINE
    df.reset_inde(inplace=True) #reseta o index pelo campo data
    return df

# Capturar os valores
df_valores = pegar_valores_online(acao_escolhida)

# Montar a tabela dos valores
st.subheader('Tabela de valores - ' + nome_acao_escolhida)
st.write(df_valores.tail(10))

# Criar Graficos
st.subheader('Gráfico dos preços')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['Close'],
                         name='Preco Fechamento',
                         line_color='yellow'))
fig.add_trace(go.Scatter(x=df_valores['Date'],
                         y=df_valores['Open'],
                         name='Preco Abertura',
                         line_color='blue'))
st.plotly_chart(fig)


#Previsão
df_treino = df_valores[['Date', 'Close']]

# Renomear colunas
df_treino = df_treino.rename(columns={'Date': 'ds', 'Close': 'y'})

# Criando o modelo
modelo = Prophet()
modelo.fit(df_treino)

#previsçoes
futuro = modelo.make_future_dataframe(periods=n_dias, freq='B')
previsao = modelo.predict(futuro)

st.subheader('Previsão')
st.write(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(n_dias))

# Grafico previsão
gra1 = plot_plotly(modelo, previsao)
st.plotly_chart(gra1)

gra2 = plot_components_plotly(modelo, previsao)
st.st.plotly_chart(gra2)
