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
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    level_div = soup.find("div", class_="entry-content")  # Altere a classe se necessário
    if not level_div:
        return None, None

    # Supondo que a informação esteja num <p> específico
    level_info = level_div.find("p").text.strip()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return level_info, timestamp
