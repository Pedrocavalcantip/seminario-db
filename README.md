# Seminário Database - Simulador de Mercado InfluxDB

Este projeto demonstra uma implementação de banco de dados de séries temporais usando InfluxDB e Python. Ele simula um mercado de câmbio de criptomoedas (BTC e ETH) gerando pontos de dados em tempo real.

## Pré-requisitos

- Docker e Docker Compose
- Python 3.x

## Instalação

1. Clone o repositório.
2. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
3. Ative o ambiente virtual:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`
4. Instale as dependências:
   ```bash
   pip install influxdb-client
   ```

## Uso

### 1. Iniciar o Banco de Dados

Inicie o container do InfluxDB usando o Docker Compose:

```bash
cd seminario_dbinflux
docker compose up -d
```

O serviço estará disponível em http://localhost:8086.

### 2. Executar o Simulador

Execute o script Python para começar a gerar e gravar dados:

```bash
python seminario_dbinflux/main.py
```

O script irá gerar dados de mercado aleatórios para BTC e ETH e gravá-los no bucket `financeiro_seminario`. Pressione Ctrl+C para parar.

## Configuração

- **URL do InfluxDB**: http://localhost:8086
- **Organização**: ufrpe
- **Bucket**: financeiro_seminario
- **Usuário**: admin
- **Senha**: senhaforte123

## Estrutura do Projeto

- `seminario_dbinflux/docker-compose.yml`: Configuração do serviço InfluxDB.
- `seminario_dbinflux/main.py`: Script Python para geração de dados.
