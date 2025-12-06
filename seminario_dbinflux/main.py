import time
import random
import math
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


token = "vwHc7xpH2shdHuGsf_3MNoN9cGBlxTDCjh4RY5kE3cV-7gIg3Bk_GXJMsAyb5IbCinTbOGM91dS_ECHLHPql5w=="
org = "ufrpe"
bucket = "financeiro"

client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Preços Iniciais
preco_btc = 60000.00
preco_eth = 3000.00

# Variáveis de Controle de Tendência
tendencia_atual = 0 
contador_tendencia = 0 

print("Iniciando Simulação de Mercado (Crypto Exchange)...")
print("Pressione Ctrl+C para parar.")

try:
    while True:
        # 1. MUDANÇA DE TENDÊNCIA
        # A cada 50 iterações (aprox 10 seg), o mercado "decide" para onde vai
        # Isso cria aquelas "ondas" no gráfico em vez de ruído puro
        if contador_tendencia <= 0:
            tendencia_atual = random.choice([-1, -1, 0, 1, 1, 1]) 
            contador_tendencia = random.randint(20, 50) 
            print(f"--- Mudança de Mercado: Tendência {tendencia_atual} ---")
        
        contador_tendencia -= 1

        # 2. CÁLCULO DA VARIAÇÃO (A Mágica acontece aqui)
        # random.gauss gera uma curva normal (mais realista que random puro)
        # Mu (média) é ajustada pela tendência. Sigma (desvio) é a volatilidade.
        
        # Fator de variação do BTC (0.05% de volatilidade base)
        fator_btc = random.gauss(mu=tendencia_atual * 0.0005, sigma=0.002)
        
        # Fator do ETH (Mais volátil que o BTC, sigma maior)
        fator_eth = random.gauss(mu=tendencia_atual * 0.0006, sigma=0.003)

        # 3. CRASH EVENT (O "Cisne Negro") - Para testar seus Alertas
        # 1% de chance de acontecer um crash relâmpago
        if random.random() < 0.01: 
            print("FLASH CRASH DETECTADO!")
            fator_btc = -0.05 # Cai 5% de uma vez
            fator_eth = -0.08 # Cai 8% de uma vez

        # Aplica o preço
        preco_btc = preco_btc * (1 + fator_btc)
        preco_eth = preco_eth * (1 + fator_eth)

        # 4. ENVIA PARA O INFLUXDB
        p_btc = Point("cotacao") \
            .tag("ativo", "BTC") \
            .field("preco", preco_btc) \
            .field("volume", random.randint(10, 500)) 

        p_eth = Point("cotacao") \
            .tag("ativo", "ETH") \
            .field("preco", preco_eth) \
            .field("volume", random.randint(50, 1000))

        write_api.write(bucket=bucket, org=org, record=[p_btc, p_eth])
        
        # Log visual no terminal
        seta = "⬆️" if fator_btc > 0 else "⬇️"
        print(f"{seta} BTC: ${preco_btc:.2f} | ETH: ${preco_eth:.2f}")
        
        time.sleep(0.2) 

except KeyboardInterrupt:
    print("\nMercado fechado.")