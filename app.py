import streamlit as st
from datetime import datetime
import pandas as pd
from main_scraper import get_river_level, update_data, plot_data

DATA_FILE = "river_level.csv"

st.title("Monitoramento do Nível do Rio Sapucaí")

# Obter o nível atual
level_info, timestamp = get_river_level()
if level_info:
    st.metric(label="Nível Atual do Rio", value=level_info)
    st.write(f"Última atualização: {timestamp}")

    # Atualizar os dados
    df = update_data(level_info, timestamp, data_file=DATA_FILE)
    st.dataframe(df)

    # Plotar o gráfico
    plot_data(df)
    st.image("plot.png")
else:
    st.error("Não foi possível obter os dados do nível do rio.")
