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
    'BTC':    {'quantidade': 0.00318941, 'porcentagem': (0.05 * 0.8),            'tipo': 'CR', 'preco': 0},
    'ETH':    {'quantidade': 0.0205375,  'porcentagem': (0.05 * 0.2),            'tipo': 'CR', 'preco': 0},
    'RE':     {'quantidade': 1000,       'porcentagem': (0.1),                   'tipo': 'BR', 'preco': 1},
}


# Função para escrever o relatório de aportes
def print_report(aportes):
    with open("report.txt", "w") as arquivo:
        for ativo, propriedades in aportes.items():
            nome_ativo = ativo.ljust(10)
            quantidade = str(propriedades['quantidade']).ljust(10)
            valor = str(propriedades['valor']).ljust(10)
            linha = f"Ativo: {nome_ativo} Quantidade: {quantidade} Valor: {valor}\n"
            arquivo.write(linha)


# Função para obter o valor atual do dólar em reais
def get_usd_to_brl_price():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    response = requests.get(url)
    data = response.json()
    return float(data["USDBRL"]["bid"])


# Função para obter os preços atuais dos ativos brasileiros e atualizar no dicionário 'ativos'
def update_brazilian_assets_prices():
    url = "https://brapi.dev/api/quote/list?sortBy=name&sortOrder=asc&token=2RpfSrYsBy4i23T6TLdZa2"
    response = requests.get(url)
    data = response.json()

    for stock in data['stocks']:
        if stock['stock'] in ativos and ativos[stock['stock']]['tipo'] == 'BR':
            ativos[stock['stock']]['preco'] = stock['close']


# Função para obter o preço atual de um ativo estrangeiro e atualizar no dicionário 'ativos'
def update_foreign_assets_prices(symbol):
    api_key = 'SUA_CHAVE_DE_API'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if 'Global Quote' in data:
        price = float(data['Global Quote']['05. price'])
        ativos[symbol]['preco'] = (price * get_usd_to_brl_price())


# Função para obter o preço atual de uma crypto e atualizar no dicionário 'ativos'
def update_cryptos_prices(symbol):
    url = f'https://economia.awesomeapi.com.br/last/{symbol}-BRL'
    response = requests.get(url)
    data = response.json()
    ativos[symbol]['preco'] = float(data[f'{symbol}BRL']['bid'])


# Função para calcular e realizar aportes conforme as porcentagens desejadas
def realizar_aportes(aporte_total):
    aportes = {}

    while aporte_total > 0:
        # Calcula o valor total da carteira
        valor_total_carteira = sum(propriedades['quantidade'] * propriedades['preco'] for propriedades in ativos.values())

        # Calcula as porcentagens atuais de cada ativo
        porcentagens_atuais = {ativo: (propriedades['quantidade'] * propriedades['preco'] / valor_total_carteira) * 100
                               for ativo, propriedades in ativos.items()}

        # Encontra o ativo com a maior diferença percentual
        ativo_maior_diferenca = max(ativos.items(), key=lambda x: x[1]['porcentagem'] * 100 - porcentagens_atuais[x[0]])

        # Calcula a diferença percentual do ativo com maior diferença
        maior_diferenca = ativo_maior_diferenca[1]['porcentagem'] * 100 - porcentagens_atuais[ativo_maior_diferenca[0]]

        # Verifica o tique mínimo
        tique_minimo = 1 if ativo_maior_diferenca[1]['tipo'] == 'BR' else 0.01 if ativo_maior_diferenca[1]['tipo'] == 'US' else 0.0001

        # Calcula o valor financeiro a ser aportado
        valor_aportar = abs(maior_diferenca / 100 * valor_total_carteira)

        # Verifica se o valor financeiro a ser aportado é maior que o aporte total
        if valor_aportar > aporte_total:
            break

        # Calcula a quantidade a ser aportada
        quantidade_aportar = valor_aportar / ativo_maior_diferenca[1]['preco']

        # Ajusta a quantidade a ser aportada para múltiplos do tique mínimo
        quantidade_aportar = int(quantidade_aportar / tique_minimo) * tique_minimo

        # Verifica se o valor financeiro do tique mínimo é maior que o aporte total
        if tique_minimo * ativo_maior_diferenca[1]['preco'] > aporte_total:
            break

        # Atualiza o valor financeiro a ser aportado
        valor_aportar = quantidade_aportar * ativo_maior_diferenca[1]['preco']

        # Atualiza o aporte total
        aporte_total -= valor_aportar

        # Adiciona o ativo nos aportes
        if ativo_maior_diferenca[0] not in aportes:
            aportes[ativo_maior_diferenca[0]] = {'quantidade': quantidade_aportar, 'valor': valor_aportar}
        else:
            aportes[ativo_maior_diferenca[0]]['quantidade'] += quantidade_aportar
            aportes[ativo_maior_diferenca[0]]['valor'] += valor_aportar

        # Atualiza as quantidades e preços nos ativos
        ativo_maior_diferenca[1]['quantidade'] += quantidade_aportar
        ativo_maior_diferenca[1]['preco'] += (ativo_maior_diferenca[1]['preco'] *
                                              (quantidade_aportar / ativo_maior_diferenca[1]['quantidade']))

    # Já escreve no txt os aportes a realizar
    print_report(aportes)


# Função principal
def main():
    # Solicitar o valor do aporte ao usuário
    aporte_total = float(input("Digite o valor do aporte: "))
    print("Calculando...")

    # Atualizar preços BR
    update_brazilian_assets_prices()

    # Atualizar preços US
    for symbol, propriedades in ativos.items():
        if propriedades['tipo'] == 'US':
            update_foreign_assets_prices(symbol)

    # Atualizar preços Crypto
    for symbol, propriedades in ativos.items():
        if propriedades['tipo'] == 'CR':
            update_cryptos_prices(symbol)

    # Realizar os aportes
    realizar_aportes(aporte_total)


# Executar a função principal
if __name__ == "__main__":
    main()
