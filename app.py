# pylint: skip-file

import streamlit as st
from datetime import datetime
import pandas as pd
from main_scraper import get_river_level, update_data, plot_data
import time

DATA_FILE = "river_level.csv"

# Intervalo de 5 segundos para testes
refresh_interval = 5

# Inicializar uma variável de estado para controle de tempo
if "last_run" not in st.session_state:
    st.session_state.last_run = time.time()
    st.session_state.first_run = True  # Flag para a primeira execução

# Obter o tempo atual
current_time = time.time()

# Exibir dados na primeira execução
if st.session_state.first_run:
    st.session_state.first_run = False  # Desmarcar a primeira execução
    level_info, timestamp = get_river_level()

    # Exibir o gráfico e dados
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
    
# Após a primeira execução, aguardar o intervalo para atualização
if current_time - st.session_state.last_run >= refresh_interval:
    # Atualiza o tempo da última execução
    st.session_state.last_run = current_time
    
    # Obter o nível atual
    level_info, timestamp = get_river_level()

    # Exibir os dados atualizados
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
    
    # Forçar a atualização da interface
    st.experimental_rerun()
else:
    # Exibe a mensagem de espera entre as atualizações
    st.write(f"Aguardando {refresh_interval} segundos para a próxima atualização...")

