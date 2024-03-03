# Importando os pacotes e bibliotecas 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

sns.set()  

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None

# Configurando o layout da pagina
st.set_page_config(page_title='SINASC RONDONIA', 
                    page_icon='https://w7.pngwing.com/pngs/368/547/png-transparent-rondoniense-social-clube-campeonato-rondoniense-rondonia-real-desportivo-ariquemes-fc-guajara-esporte-clube-brasil-futebol-emblem-text-logo.png',
                    layout='wide')

# Adicionando um titulo na nossa pagina 
st.title('Analise SINASC Rôndonia')

# Importando os dados:
sinasc = pd.read_csv("D:\\CURSOS\\2 - EBAC\\Ciêntista de Dados\\2 - Cientista de Dados\\16 - Streamlit I\\Exercicio 1\\dadosdf.csv")
st.markdown('----')

# Introdução:
st.subheader("Entendendo os dados")
st.markdown("Esses dados são referentes aos nascido, no estado de Rôndonia no ano de 2019. Nesses dados possui informações como; data de nascimento, local de nascimento, pai, mãe, nidel de escolaridade da mãe entre outros dados tanto do bebê como dos pais")
st.markdown('----')

# transformando os dados de csv para dataframe e mostrando na tela do aplicativo:
st.write('A seguir, você encontrará uma tabela contendo nossos dados:\nque serão utilizados ao longo de nossas análises:')
st.dataframe(sinasc)
st.markdown('----')

# Criando uma tabela para explicar as variaveis
st.write('Maior date e meno dates')
sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)

st.write(sinasc.DTNASC.max())
st.write(sinasc.DTNASC.min())

max_data = sinasc.DTNASC.max()
min_data = sinasc.DTNASC.min()
st.markdown('----')

data_inicial = st.sidebar.date_input('Data inicial',
              value = min_data,
              min_value = min_data,
              max_value = max_data)
data_final = st.sidebar.date_input('Data inicial',
              value = max_data,
              min_value = min_data,
              max_value = max_data)

st.sidebar.write('Data inicial = ', data_inicial)
st.sidebar.write('Data inicial = ', data_final)


# Plotar o mapa
# Renomear colunas
st.subheader('Mapa das regiões de nascimento de bebes')
sinasc = sinasc.rename(columns={'munResLat': 'LAT', 'munResLon': 'LON'})
sinasc = sinasc.dropna(subset=['LAT', 'LON'])
st.map(sinasc[['LAT', 'LON']])
st.markdown('----')

# Criando filtro para cidades
# Extrair a lista de nomes das cidades únicas
cidades_unicas = sinasc['munResNome'].unique()

# Criar o filtro multiselect para as cidades na barra lateral esquerda
cidades_selecionadas = st.sidebar.multiselect('Selecione as cidades', cidades_unicas)

# Aplicar o filtro
if cidades_selecionadas:
    sinasc_filtrado = sinasc[sinasc['munResNome'].isin(cidades_selecionadas)]
    st.write(sinasc_filtrado)
else:
    st.write('Nenhuma cidade selecionada. Por favor, selecione uma ou mais cidades.')
st.markdown('----')


sinasc = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final)) & (sinasc['DTNASC'] >=pd.to_datetime(data_inicial)  )]

# Plotando os Graficos 
st.subheader('Média idade mãe X Date')
plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')
st.markdown('----')

st.subheader('Média idade mãe X Date de nascimento')
plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
st.markdown('----')

st.subheader('Média peso bebe X Date nascimento')
plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
st.markdown('----')

st.subheader('Peso mediano X Escolariade Mãe')
plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort')
st.markdown('----')

st.subheader('APGAR1 médio X Gestação')
plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort')
st.markdown('----')