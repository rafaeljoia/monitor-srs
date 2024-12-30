# pylint: skip-file

import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def update_data(level, timestamp, data_file="river_level.csv"):
    try:
        df = pd.read_csv(data_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "level"])

    new_row = {"timestamp": timestamp, "level": float(level)}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(data_file, index=False)
    return df

def plot_data(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['level'], marker='o')
    plt.title("Nível do Rio Sapucaí ao longo do tempo")
    plt.xlabel("Data/Hora")
    plt.ylabel("Nível do Rio (m)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plot.png")


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