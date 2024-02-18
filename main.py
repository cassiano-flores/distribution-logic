import requests

# Definição dos Ativos
ativos = {
    'BBAS3':  {'quantidade': 5,          'porcentagem': (0.4 * 0.28 * (1 / 3)),  'tipo': 'BR', 'preco': 0},
    'BBDC3':  {'quantidade': 35,         'porcentagem': (0.4 * 0.28 * (1 / 3)),  'tipo': 'BR', 'preco': 0},
    'SANB3':  {'quantidade': 31,         'porcentagem': (0.4 * 0.28 * (1 / 3)),  'tipo': 'BR', 'preco': 0},
    'AESB3':  {'quantidade': 20,         'porcentagem': (0.4 * 0.45 * (1 / 5)),  'tipo': 'BR', 'preco': 0},
    'AURE3':  {'quantidade': 35,         'porcentagem': (0.4 * 0.45 * (1 / 5)),  'tipo': 'BR', 'preco': 0},
    'CMIG4':  {'quantidade': 28,         'porcentagem': (0.4 * 0.45 * (1 / 5)),  'tipo': 'BR', 'preco': 0},
    'TAEE3':  {'quantidade': 37,         'porcentagem': (0.4 * 0.45 * (1 / 5)),  'tipo': 'BR', 'preco': 0},
    'TRPL4':  {'quantidade': 17,         'porcentagem': (0.4 * 0.45 * (1 / 5)),  'tipo': 'BR', 'preco': 0},
    'BBSE3':  {'quantidade': 10,         'porcentagem': (0.4 * 0.18 * (1 / 2)),  'tipo': 'BR', 'preco': 0},
    'CXSE3':  {'quantidade': 20,         'porcentagem': (0.4 * 0.18 * (1 / 2)),  'tipo': 'BR', 'preco': 0},
    'SAPR3':  {'quantidade': 41,         'porcentagem': (0.4 * 0.09 * (1)),      'tipo': 'BR', 'preco': 0},
    'KNRI11': {'quantidade': 4,          'porcentagem': (0.25 * 0.5 * (1 / 2)),  'tipo': 'BR', 'preco': 0},
    'MXRF11': {'quantidade': 70,         'porcentagem': (0.25 * 0.5 * (1 / 2)),  'tipo': 'BR', 'preco': 0},
    'HGLG11': {'quantidade': 1,          'porcentagem': (0.25 * 0.18 * (1 / 2)), 'tipo': 'BR', 'preco': 0},
    'VILG11': {'quantidade': 0,          'porcentagem': (0.25 * 0.18 * (1 / 2)), 'tipo': 'BR', 'preco': 0},
    'BRCR11': {'quantidade': 0,          'porcentagem': (0.25 * 0.18 * (1 / 2)), 'tipo': 'BR', 'preco': 0},
    'HGRE11': {'quantidade': 0,          'porcentagem': (0.25 * 0.18 * (1 / 2)), 'tipo': 'BR', 'preco': 0},
    'MALL11': {'quantidade': 1,          'porcentagem': (0.25 * 0.14 * (1 / 2)), 'tipo': 'BR', 'preco': 0},
    'XPML11': {'quantidade': 2,          'porcentagem': (0.25 * 0.14 * (1 / 2)), 'tipo': 'BR', 'preco': 0},
    'DLR':    {'quantidade': 0,          'porcentagem': (0.2 * (1 / 7)),         'tipo': 'US', 'preco': 0},
    'O':      {'quantidade': 2.65,       'porcentagem': (0.2 * (1 / 7)),         'tipo': 'US', 'preco': 0},
    'STAG':   {'quantidade': 0,          'porcentagem': (0.2 * (1 / 7)),         'tipo': 'US', 'preco': 0},
    'SPG':    {'quantidade': 0,          'porcentagem': (0.2 * (1 / 7)),         'tipo': 'US', 'preco': 0},
    'AMT':    {'quantidade': 0.85,       'porcentagem': (0.2 * (1 / 7)),         'tipo': 'US', 'preco': 0},
    'ARR':    {'quantidade': 9.16225,    'porcentagem': (0.2 * (1 / 7)),         'tipo': 'US', 'preco': 0},
    'VOO':    {'quantidade': 0,          'porcentagem': (0.2 * (1 / 7)),         'tipo': 'US', 'preco': 0},
    'BTC':    {'quantidade': 0.00318941, 'porcentagem': (0.05 * 0.8),            'tipo': 'NA', 'preco': 0},
    'ETH':    {'quantidade': 0.0205375,  'porcentagem': (0.05 * 0.2),            'tipo': 'NA', 'preco': 0},
    'RE':     {'quantidade': 1000,       'porcentagem': (0.1),                   'tipo': 'NA', 'preco': 0},
}

# Função para escrever o relatório
def print_report(ativos):
    with open("relatorio.txt", "w") as arquivo:
        for ativo, propriedades in ativos.items():
            nome_ativo = ativo.ljust(10)
            quantidade = str(propriedades['quantidade']).ljust(10)
            preco = str(propriedades['preco']).ljust(10)
            linha = f"Ativo: {nome_ativo} Quantidade: {quantidade} Preco: {preco}\n"
            arquivo.write(linha)

# Função para obter o valor atual do dólar em reais
def get_usd_to_brl_price():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    response = requests.get(url)
    data = response.json()
    return float(data["USDBRL"]["bid"])

# Função para obter os preços atuais dos ativos brasileiros e atualizar no dicionário 'ativos'
def update_brazilian_stock_prices():
    url = "https://brapi.dev/api/quote/list?sortBy=name&sortOrder=asc&token=2RpfSrYsBy4i23T6TLdZa2"
    response = requests.get(url)
    data = response.json()
    
    for stock in data['stocks']:
        if stock['stock'] in ativos and ativos[stock['stock']]['tipo'] == 'BR':
            ativos[stock['stock']]['preco'] = stock['close']

# Função para obter o preço atual de um ativo estrangeiro e atualizar no dicionário 'ativos'
def update_foreign_asset_price(symbol):
    api_key = 'SUA_CHAVE_DE_API'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if 'Global Quote' in data:
        price = float(data['Global Quote']['05. price'])
        ativos[symbol]['preco'] = (price * get_usd_to_brl_price())


# Atualiza preços BR
update_brazilian_stock_prices()

# Atualiza preços US
for symbol, propriedades in ativos.items():
    if propriedades['tipo'] == 'US':
        update_foreign_asset_price(symbol)

# Escreve o relatório
print_report(ativos)
