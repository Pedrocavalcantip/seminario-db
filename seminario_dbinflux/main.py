import time
import random
import math
from datetime import datetime, timedelta, UTC
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

token = "6udfe8gCb-dvi1i6UiINdlGLj4KxvK4fA5KOHU81FZVSxswPyQ15s_12-82VDom4CPO3V_nsae5zTEtdxOAsGw=="
org = "ufrpe"
bucket = "financeiro"

client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Preços Iniciais
preco_btc = 60000.00
preco_eth = 3000.00

# Controle de tendência
tendencia_atual = 0
contador_tendencia = 0

# Timestamp inicial (agora)
tempo_atual = datetime.now(UTC)

print("Iniciando Simulação de Mercado (Crypto Exchange)...")
print("Pressione Ctrl+C para parar.")

try:
    while True:

        # 1. Mudança de tendência (mesma lógica)
        if contador_tendencia <= 0:
            tendencia_atual = random.choice([-1, -1, 0, 1, 1, 1])
            contador_tendencia = random.randint(20, 50)
            print(f"--- Mudança de Mercado: Tendência {tendencia_atual} ---")

        contador_tendencia -= 1

        # 2. Variação do mercado
        fator_btc = random.gauss(mu=tendencia_atual * 0.0005, sigma=0.002)
        fator_eth = random.gauss(mu=tendencia_atual * 0.0006, sigma=0.003)

        # Crash event
        if random.random() < 0.01:
            print("FLASH CRASH DETECTADO!")
            fator_btc = -0.05
            fator_eth = -0.08

        # Aplica preço
        preco_btc *= (1 + fator_btc)
        preco_eth *= (1 + fator_eth)

        # 3. Envia para o InfluxDB com timestamp real
        p_btc = (
            Point("cotacao")
            .tag("ativo", "BTC")
            .field("preco", float(preco_btc))
            .field("volume", random.randint(10, 500))
            .time(tempo_atual)
        )

        p_eth = (
            Point("cotacao")
            .tag("ativo", "ETH")
            .field("preco", float(preco_eth))
            .field("volume", random.randint(50, 1000))
            .time(tempo_atual)
        )

        write_api.write(bucket=bucket, org=org, record=[p_btc, p_eth])

        # Log no terminal
        seta = "⬆️" if fator_btc > 0 else "⬇️"
        print(f"{seta} BTC: ${preco_btc:.2f} | ETH: ${preco_eth:.2f}")

        # Avança o tempo + 1 segundo
        tempo_atual += timedelta(seconds=1)

        # Espera para a simulação ficar suave
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nMercado fechado.")
