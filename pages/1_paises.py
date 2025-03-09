import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title='Países', page_icon='📊', layout='wide')

#========================================================
# FUNÇÕES
#========================================================
def top_five(df, coluna1, coluna2):
    df_aux = (df[[coluna1, coluna2]].groupby(coluna1)
                                    .nunique()
                                    .sort_values(coluna2, ascending=False)
                                    .reset_index()
                                    .head())                
    fig = px.bar(df_aux, x=coluna1,
                y=coluna2)                
    return fig



#----------------------------Início da estrutura lógica------------------------------------

#========================================================
# importando os dados
#========================================================

df = pd.read_csv('data/data.csv')

# Os dados já estão limpos

#========================================================
# barra lateral
#========================================================

st.header('Países')

st.sidebar.image('fome.jpg', width=300)

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
        st.title('Métricas principais')

        col1, col2, col3, col4, col5 = st.columns(5, gap='large')

        with col1:
            # quantidade de restaurantes
            restaurante = df['restaurant_id'].nunique()

            col1.metric('Número de Restaurantes', restaurante,
                        border=True)

        with col2:
            # quantidade de países
            pais = df['country'].nunique()

            col2.metric('Quantidade de países', pais,
                        border=True)

        with col3:
            # quantidade de cidades
            cidades = df['city'].nunique()

            col3.metric('Quantidade de cidades', cidades,
                        border=True)

        with col4:
            # quantidade de avaliações
            avaliacoes = df['votes'].sum()

            col4.metric('Avaliações registradas', avaliacoes,
                        border=True)

        with col5:
            # tipos culinários
            culinario = df['cuisines'].nunique()

            col5.metric('Tipos Culinários', culinario,
                        border=True)

    with st.container(border=True):

        col1, col2 = st.columns(2, gap='large')

        with col1:
            # top 5 países com mais restaurantes
            st.markdown('## 5 Países com mais restaurantes')
            fig = top_five(df, 'country', 'restaurant_id')
            st.plotly_chart(fig)

        with col2:
            # top 5 países com mais avaliações
            st.markdown('## 5 Países com mais avaliações registradas')

            fig = top_five(df, 'country', 'votes')
            st.plotly_chart(fig)

    with st.container(border=True):

        col1, col2 = st.columns(2, gap='large')

        with col1:
             st.markdown('## Países com percentil maior de tipos culinários')

             df_aux = (df[['country', 'cuisines']].groupby('country')
                            .nunique()
                            .sort_values('cuisines', ascending=False)
                            .reset_index()
                            .head(3))
             
             fig = px.pie(df_aux, values='cuisines',names='country')

             st.plotly_chart(fig, use_container_width=True)

        with col2:
             st.markdown('## Média de preço de um prato para dois por país')
             
             df_aux = (df[['country', 'average_cost_for_two']].groupby('country')
                                                              .mean()
                                                              .sort_values('average_cost_for_two', 
                                                                            ascending=False)
                                                              .reset_index())
             
             st.dataframe(df_aux)
        
        with st.container():
             st.markdown('## Nota média por país')

             df_aux = (df[['country', 'aggregate_rating']].groupby('country')
                                                          .mean()
                                                          .sort_values('aggregate_rating',
                                                                       ascending=False)
                                                          .reset_index())
             
             fig = px.bar(df_aux, x='country',
                          y='aggregate_rating',
                          color='country')
             
             fig.update_layout(showlegend=False)
             
             st.plotly_chart(fig)
