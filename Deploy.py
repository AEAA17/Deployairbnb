import pandas as pd
import streamlit as st
import joblib

# Definindo os dicionários de entrada
x_numericos = {'latitude': 0, 'longitude': 0, 'hóspedes': 0, 'banheiros': 0, 'quartos': 0, 'camas': 0, 'R$ por pessoas extras': 0,
               'noites mínimas': 0, 'ano': 0, 'mês': 0, 'comodidades': 0, 'número de imóveis do anfitrião': 0}

x_tf = {'Anfitrião Superhost?': 0, 'Reserva instantânea?': 0}

x_listas = {'Tipo de Propriedade': ['Apartamento', 'Cama e Café', 'Condomínio', 'Suíte de Hóspedes', 'Casa de Hóspedes', 'Hostel', 'Casa', 'Loft', 'Outros', 'Apartamento com Serviço'],
            'Tipo de Quarto': ['Imóvel Inteiro', 'Quarto de Hotel', 'Quarto Privado', 'Quarto Compartilhado'],
            'Política de Cancelamento': ['Flexível', 'Moderada', 'Rígida', 'Rígida 14 dias com Período de Carência']}           

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
    dados = pd.read_csv(r"https://raw.githubusercontent.com/AEAA17/Deployairbnb/refs/heads/main/dados.csv")
    colunas = list(dados.columns)[1:-1]
    valores_x = valores_x[colunas]
    modelo = joblib.load(r"C:\Users\euric\Documents\Códigos Py\PDC\modelo.joblib")
    preco = modelo.predict(valores_x)
    st.write(f'O preço previsto é: R${preco[0]:.2f}')
