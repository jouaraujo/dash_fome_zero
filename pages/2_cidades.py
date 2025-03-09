import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Cidades', page_icon='🏢', layout='wide')

#========================================================
# FUNÇÕES
#========================================================


#----------------------------Início da estrutura lógica------------------------------------

#========================================================
# importando os dados
#========================================================

df = pd.read_csv('../data/data.csv')

# Os dados já estão limpos

#========================================================
# barra lateral
#========================================================

st.header('Cidades')

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

tab1, tab2 = st.tabs(['Visão Gerencial', 'Visão Geográfica'])

with tab1:
    with st.container():
        st.header('Métricas')
        
        col1, col2 = st.columns(2, gap='large')

        with col1:
            # cidade que possui mais restaurantes registrados
            cidade = (df[['city', 'restaurant_id']].groupby('city')
                                                   .count()
                                                   .sort_values('restaurant_id',
                                                                ascending=False)
                                                   .reset_index()
                                                   .iloc[0,0])
            
            col1.metric('Cidade que possui mais restaurantes', cidade, border=True)

        with col2:
            # cidade que possui mais restaurantes com nota média acima de 4?
            df_aux = df[df['aggregate_rating'] > 4]

            cidade = (df_aux[['city', 'restaurant_id']].groupby('city')
                                                       .count()
                                                       .sort_values('restaurant_id', 
                                                                    ascending=False)
                                                       .reset_index()
                                                       .iloc[0,0])
            
            col2.metric('Cidade com mais restaurantes com nota média maior que 4', cidade, border=True)

    with st.container():

        col1, col2 = st.columns(2, gap='large')
    
        with col1:
            # cidade que possui mais restaurantes com nota média abaixo de 2.5

            df_aux = df[df["aggregate_rating"] < 2.5]

            cidade = (df_aux[['city', 'restaurant_id']].groupby('city')
                                                       .count()
                                                       .sort_values('restaurant_id',
                                                                    ascending=False)
                                                        .reset_index()
                                                        .iloc[0,0])
            
            st.metric('Cidade que possui mais restaurantes com nota média abaixo de 2.5', 
                                                                    cidade, border=True)
            
        with col2:
            # cidade que possui a maior quantidade de restaurantes que aceitam pedidos online

            cidade = (df[df['has_online_delivery'] == 1][['city', 'restaurant_id']].groupby('city')
                                                                                   .count()
                                                                                   .sort_values('restaurant_id',
                                                                                                ascending=False)
                                                                                   .reset_index()
                                                                                   .iloc[0,0])
            
            st.metric('cidade que possui a maior quantidade de restaurantes que aceitam pedidos online',
                      cidade, border=True)
            
    with st.container(border=True):
            st.markdown('## Quantidades de restaurantes por cidade')
            # gráfico com as cidades que possuem mais restaurantes
            df_aux = (df[['city', 'restaurant_id']].groupby('city')
                                                   .count()
                                                   .sort_values('restaurant_id',
                                                                ascending=False)
                                                   .reset_index()
                                                   )
            
            fig = px.bar(df_aux, x='city',
                         y='restaurant_id',
                         color='city')
            
            fig.update_layout(showlegend=False)

            st.plotly_chart(fig)

    with st.container(border=True):
         col1, col2 = st.columns(2, gap='large')

         with col1:
              st.markdown('### Cidades que possuem e que não possuem delivery online')
              df_aux = (df[['has_online_delivery', 'city']].groupby('has_online_delivery')
                                                           .count()
                                                           .reset_index())
              
              df_aux['has_online_delivery'] = df_aux['has_online_delivery'].replace({0: 'Não possui',
                                                                                     1: 'Possui'})
              
              fig = px.pie(df_aux, values='city',
                           names='has_online_delivery')
              
              st.plotly_chart(fig, use_container_width=True)

         with col2:
              st.markdown('### Cidades que possuem e que não possuem entregas')
              df_aux = (df[['is_delivering_now', 'city']].groupby('is_delivering_now')
                                                           .count()
                                                           .reset_index())
              
              df_aux['is_delivering_now'] = df_aux['is_delivering_now'].replace({0: 'Não possui',
                                                                                     1: 'Possui'})
              
              fig = px.pie(df_aux, values='city',
                           names='is_delivering_now')
              
              st.plotly_chart(fig, use_container_width=True)  

with tab2:
    st.markdown('# Mapa com as cidades registradas')
    
    df_aux = df[['city', 'country', 'latitude', 'longitude']].groupby(['city', 'country'])\
                                                             .median().reset_index()
    
    map = folium.Map()
    
    for i in range(len(df_aux)):
            folium.Marker([df_aux.loc[i,'latitude'], df_aux.loc[i,'longitude']],
            popup=df_aux.loc[i, ['city', 'country']]).add_to(map)    
    
    folium_static(map, width=1024, height=600)
