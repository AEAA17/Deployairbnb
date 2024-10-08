import pandas as pd
import streamlit as st
import joblib
url = 'https://raw.githubusercontent.com/AEAA17/Deployairbnb/main/dados.csv'

# Definindo os dicionários de entrada
x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancelation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }

dic = {}
for item in x_listas:
    for valor in x_listas[item]:
        dic[f'{item}_{valor}'] = 0

# Processando as entradas numéricas
for item in x_numericos:
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(f'{item.capitalize()}', step=0.00001, value=0.0, format='%.5f')
    elif item == 'pessoas extras':
        valor = st.number_input(f'{item.capitalize()}', step=0.01, value=0.0)
    else:        
        valor = st.number_input(f'{item.capitalize()}', step=1)
    x_numericos[item] = valor

# Processando as entradas booleanas
for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    if valor == "Sim":
        x_tf[item] = 1
    else:
        x_tf[item] = 0

# Processando as entradas de lista
for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item])
    dic[f'{item}_{valor}'] = 1

# Botão para prever o preço
botao = st.button('Prever Preço')
if botao:
    dic.update(x_numericos)
    dic.update(x_tf)
    valores_x = pd.DataFrame([dic])  # Criando o DataFrame com os valores de entrada
    dados = pd.read_csv(url)
    colunas = list(dados.columns)[1:-1]
    valores_x = valores_x[colunas]
    modelo = joblib.load(r"C:\Users\euric\Documents\Códigos Py\PDC\modelo.joblib")
    preco = modelo.predict(valores_x)
    st.write(f'O preço previsto é: R${preco[0]:.2f}')
