# pylint: skip-file

import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd

def update_data(level, timestamp, data_file="river_level.csv"):
    try:
        # Tentar ler o arquivo CSV existente
        df = pd.read_csv(data_file)
    except FileNotFoundError:
        # Se o arquivo não existir, criar um DataFrame vazio com as colunas esperadas
        df = pd.DataFrame(columns=["timestamp", "level"])

    # Criar uma nova linha de dados
    new_row = {"timestamp": timestamp, "level": float(level)}

    # Verificar se os dados já existem no DataFrame
    if not ((df["timestamp"] == timestamp) & (df["level"] == float(level))).any():
        # Se não existir, adicionar a nova linha
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        # Atualizar o arquivo CSV com os novos dados
        df.to_csv(data_file, index=False)
    else:
        # Caso já exista, você pode optar por não atualizar o CSV
        print("Dados já existem no CSV. Nenhuma atualização realizada.")

    return df



def plot_data(df):
    # Certificar que 'timestamp' está no formato correto
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Criação do gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['level'], marker='o', color='b', linestyle='-', markersize=5)

    # Adicionando título e rótulos
    plt.title("Nível do Rio Sapucaí ao longo do tempo")
    plt.xlabel("Data/Hora")
    plt.ylabel("Nível do Rio (m)")

    # Ajustando o formato do eixo X para hora
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Intervalo de 1 hora
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))  # Formato de data e hora

    # Rotacionando os rótulos do eixo X para melhor legibilidade
    plt.xticks(rotation=45)

    # Adicionando a grade para melhorar a visualização
    plt.grid(True)

    # Ajustando o layout para evitar sobreposição de elementos
    plt.tight_layout()

    # Salvando o gráfico como imagem
    plt.savefig("plot.png")
    plt.close()  # Fechar o gráfico após salvar

def get_river_level():
    url = "https://pmsrs.mg.gov.br/nivel-do-rio-sapucai/"
    
    # Adiciona cabeçalhos à requisição
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }
    
    # Faz a requisição GET com os cabeçalhos
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Faz o parse do HTML com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Localiza o elemento que contém o texto desejado
    page_content = soup.find("div", class_="page__content")
    if not page_content:
        return None, None
    
    # Extrai o texto com o nível e a data/hora
    text_content = page_content.get_text(separator=" ", strip=True)
    
    # Procura as informações específicas no texto
    import re
    level_match = re.search(r"Nível do Rio Sapucaí: ([\d.]+) metros", text_content)
    timestamp_match = re.search(r"Data e hora da medição: ([\d\-: ]+)", text_content)
    
    if level_match and timestamp_match:
        level_info = level_match.group(1)
        timestamp = timestamp_match.group(1)
        return level_info, timestamp
    
    return None, None