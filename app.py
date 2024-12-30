# pylint: skip-file

import streamlit as st
from datetime import datetime
import pandas as pd
from main_scraper import get_river_level, update_data, plot_data
import time
from streamlit_option_menu import option_menu  # Importando a biblioteca

DATA_FILE = "river_level.csv"

# Intervalo de 5 segundos para testes
refresh_interval = 5

hide_github_icon = """
#GithubIcon {
    visibility: hidden;
}
"""
# Inicializar uma variável de estado para controle de tempo
if "last_run" not in st.session_state:
    st.session_state.last_run = time.time()
    st.session_state.first_run = True  # Flag para a primeira execução
    st.session_state.last_fetch = None  # Armazena a data da última busca

# Obter o tempo atual
current_time = time.time()

# Menu com opção de selecionar entre várias páginas
with st.sidebar:
    selected = option_menu(
        "Menu",  # Título do menu
        ["Nível do Rio", "Preços de Aluguel", "Outras Informações"],  # Opções do menu
        icons=["cloud-rain", "house", "info-circle"],  # Ícones para cada opção
        menu_icon="cast",  # Ícone do menu
        default_index=0,  # A primeira opção será selecionada por padrão
    )

# Tela de Nível do Rio
if selected == "Nível do Rio":
    st.title("Monitoramento do Nível do Rio Sapucaí")

    # Exibir dados na primeira execução
    if st.session_state.first_run:
        st.session_state.first_run = False  # Desmarcar a primeira execução
        level_info, timestamp = get_river_level()

        # Exibir o gráfico e dados
        if level_info:
            st.metric(label="Nível Atual do Rio", value=f'{level_info} Metros')
            st.write(f"Última atualização: {timestamp}")

            # Atualizar os dados
            df = update_data(level_info, timestamp, data_file=DATA_FILE)
            
            # Plotar o gráfico
            plot_data(df)
            st.image("plot.png")

            # Renomear as colunas após o plot
            df = df.rename(columns={
                'timestamp': 'Hora da Atualização',
                'level': 'Nível em Metros'
            })

            # Exibir a tabela abaixo do gráfico
            st.dataframe(df)
        else:
            st.error("Não foi possível obter os dados do nível do rio.")
        
        # Armazenar a última hora da busca
        st.session_state.last_fetch = timestamp

    # Verificar se o tempo de espera foi atingido para a próxima atualização
    if current_time - st.session_state.last_run >= refresh_interval:
        # Atualiza o tempo da última execução
        st.session_state.last_run = current_time
        
        # Obter o nível atual
        level_info, timestamp = get_river_level()

        # Exibir os dados atualizados
        if level_info:
            st.metric(label="Nível Atual do Rio", value=f"{level_info} metros")
            st.write("As informações são coletadas do site: [Nível do Rio Sapucaí](https://pmsrs.mg.gov.br/nivel-do-rio-sapucai/)")

            st.write(f"Última atualização: {timestamp}")

            # Atualizar os dados
            df = update_data(level_info, timestamp, data_file=DATA_FILE)
            st.dataframe(df)

            # Plotar o gráfico
            plot_data(df)
            st.image("plot.png")
        else:
            st.error("Não foi possível obter os dados do nível do rio.")

        # Armazenar a última hora da busca
        st.session_state.last_fetch = timestamp
        
        # Exibir a mensagem da última busca
        st.write(f"Última busca de informações: {st.session_state.last_fetch}")

        # Forçar a atualização da interface
        st.experimental_rerun()  # Atualização correta para forçar o rerun

    else:
        pass
        # Exibe a mensagem de espera entre as atualizações
        st.write(f"Aguardando {refresh_interval} segundos para a próxima atualização...")

# Tela de Preços de Aluguel (exemplo de outra tela)
elif selected == "Preços de Aluguel":
    st.title("Preços de Aluguel")
    st.write("Em breve, valores de alugueis das imobiliárias de Santa Rita do Sapucaí.")

    # Aqui você pode adicionar o código para a página de preços de aluguel.

# Outra tela que você desejar
else:
    st.title("Outras Informações")
    st.write("Serão disponibilizadas outras informações úteis, como valores de alugueis e outros utilitários para a população.")
