import streamlit as st

st.set_page_config(
    page_title='Home',
    page_icon='🏚️'
)

st.sidebar.image('fome.jpg', width=300)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown('## Elevando experiências, conectando paladares.')
st.sidebar.markdown("""---""")

st.write('# Fome Zero Dashboard')

st.markdown(
    """
    Dashboard foi construído para acompanhar as métricas dos Países, Cidades, Consumidores e Restaurantes.
    ### Como utilizar esse Dashboard?
    - Visão Países:
        - Visão Gerencial: Métricas gerais de comportamento.
    - Visão Cidades:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for Help
    - @Jou
    """
)