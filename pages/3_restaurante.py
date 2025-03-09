import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='restaurantes', page_icon='🍽️', layout='wide')

#========================================================
# FUNÇÕES
#========================================================


#----------------------------Início da estrutura lógica------------------------------------

#========================================================
# importando os dados
#========================================================

df = pd.read_csv('data/data.csv')

# Os dados já estão limpos

#========================================================
# barra lateral
#========================================================

st.header('Restaurantes')

st.sidebar.image('../fome.jpg', width=300)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Elevando experiências, conectando paladares.')
st.sidebar.markdown("""---""")

paises = st.sidebar.multiselect(
                    'Quais países',
                    ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland",
                     "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", "Turkey"
                     "United Arab Emirates", "England", "United States of America"],
                    default=["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland",
                     "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", "Turkey"
                     "United Arab Emirates", "England", "United States of America"]
)

st.sidebar.markdown("""---""")

st.sidebar.markdown('### Feito por Jou')

# Filtro de país
linhas_selecionadas = df['country'].isin(paises)
df = df.loc[linhas_selecionadas, :]

#========================================================
# layout streamlit
#========================================================

tab1, tab2 = st.tabs(['Visão Gerencial', '_'])

with tab1:

    with st.container():
        st.header('Métricas')

        col1, col2, col3 = st.columns(3, gap='large')

        with col1:
            # nome do restaurante que possui a maior quantidade de avaliações
            restaurante = (df[['restaurant_name', 'votes']].sort_values('votes',
                                                                        ascending=False)
                                                           .reset_index(drop=True)
                                                           .iloc[0,0])
            
            col1.metric('Restaurante que possui mais avaliações', restaurante,
                        border=True)
            
        with col2:
            # nome do restaurante com a maior nota média
            restaurante = (df[['restaurant_name', 'aggregate_rating']].sort_values('aggregate_rating',
                                                                                    ascending=False)
                                                                      .reset_index(drop=True)
                                                                      .iloc[0,0])
            
            col2.metric('Restaurante com a maior nota média',
                        restaurante, border=True)
            
        with col3:
            # nome do restaurante que possui o maior valor de uma prato para duas pessoas
            restaurante = (df[['restaurant_name', 'average_cost_for_two']].sort_values('average_cost_for_two',
                                                                                       ascending=False)
                                                                          .reset_index(drop=True)
                                                                          .iloc[0,0])
            
            col3.metric('Restaurante que possui o maior valor de uma prato para duas pessoas',
                        restaurante, border=True)
    
    with st.container(border=True):

        col1, col2 = st.columns(2, gap='large')

        with col1:
           st.markdown('### Comparação no número de avaliações de restaurantes que trabalham e não online')
           # restaurantes que aceitam pedido online são também, na média, 
           # os restaurantes que mais possuem avaliações registradas
           df_aux = (df[['has_online_delivery', 'votes']].groupby('has_online_delivery')
                                                         .mean()
                                                         .sort_values('votes', ascending=False)
                                                         .reset_index()
                                                         )
           
           df_aux['has_online_delivery'].replace({0: 'Não trabalham',
                                                  1: 'trabalham'},
                                                  inplace=True)
           
           fig = px.pie(df_aux, values='votes',
                        names='has_online_delivery')
           
           st.plotly_chart(fig, use_container_width=True)

        with col2:
           st.markdown('### Comparação do valor médio de restaurantes que fazem e não reservas')
           #restaurantes que fazem reservas são também, na média, os restaurantes que
           # possuem o maior valor médio de um prato para duas pessoas?
           df_aux = (df[['has_table_booking','average_cost_for_two']].groupby('has_table_booking')
                                                         .mean()
                                                         .sort_values('average_cost_for_two', ascending=False)
                                                         .reset_index()
                                                         )
           
           df_aux['has_table_booking'].replace({0: 'Não fazem reservas',
                                                  1: 'Fazem reservas'},
                                                  inplace=True)
           
           fig = px.pie(df_aux, values='average_cost_for_two',
                        names='has_table_booking')
           
           st.plotly_chart(fig, use_container_width=True)
