import requests
import math

# My assets
assets = {
    'BBAS3':  {'quantity': 9.00000000,    'targetPercent': (0.4  * 0.28 * (1 / 3)), 'type': 'BR', 'price': 0},
    'BBDC3':  {'quantity': 37.00000000,   'targetPercent': (0.4  * 0.28 * (1 / 3)), 'type': 'BR', 'price': 0},
    'SANB3':  {'quantity': 49.00000000,   'targetPercent': (0.4  * 0.28 * (1 / 3)), 'type': 'BR', 'price': 0},
    'AESB3':  {'quantity': 42.00000000,   'targetPercent': (0.4  * 0.45 * (1 / 5)), 'type': 'BR', 'price': 0},
    'AURE3':  {'quantity': 53.00000000,   'targetPercent': (0.4  * 0.45 * (1 / 5)), 'type': 'BR', 'price': 0},
    'CMIG4':  {'quantity': 46.00000000,   'targetPercent': (0.4  * 0.45 * (1 / 5)), 'type': 'BR', 'price': 0},
    'TAEE3':  {'quantity': 68.00000000,   'targetPercent': (0.4  * 0.45 * (1 / 5)), 'type': 'BR', 'price': 0},
    'TRPL4':  {'quantity': 27.00000000,   'targetPercent': (0.4  * 0.45 * (1 / 5)), 'type': 'BR', 'price': 0},
    'BBSE3':  {'quantity': 14.00000000,   'targetPercent': (0.4  * 0.18 * (1 / 2)), 'type': 'BR', 'price': 0},
    'CXSE3':  {'quantity': 28.00000000,   'targetPercent': (0.4  * 0.18 * (1 / 2)), 'type': 'BR', 'price': 0},
    'SAPR3':  {'quantity': 89.00000000,   'targetPercent': (0.4  * 0.09 * (1)),     'type': 'BR', 'price': 0},
    'KNRI11': {'quantity': 6.00000000,    'targetPercent': (0.25 * 0.5  * (1 / 2)), 'type': 'BR', 'price': 0},
    'MXRF11': {'quantity': 86.00000000,   'targetPercent': (0.25 * 0.5  * (1 / 2)), 'type': 'BR', 'price': 0},
    'HGLG11': {'quantity': 2.00000000,    'targetPercent': (0.25 * 0.18 * (1 / 2)), 'type': 'BR', 'price': 0},
    'VILG11': {'quantity': 6.00000000,    'targetPercent': (0.25 * 0.18 * (1 / 2)), 'type': 'BR', 'price': 0},
    'BRCR11': {'quantity': 10.00000000,   'targetPercent': (0.25 * 0.18 * (1 / 2)), 'type': 'BR', 'price': 0},
    'HGRE11': {'quantity': 5.00000000,    'targetPercent': (0.25 * 0.18 * (1 / 2)), 'type': 'BR', 'price': 0},
    'MALL11': {'quantity': 2.00000000,    'targetPercent': (0.25 * 0.14 * (1 / 2)), 'type': 'BR', 'price': 0},
    'XPML11': {'quantity': 2.00000000,    'targetPercent': (0.25 * 0.14 * (1 / 2)), 'type': 'BR', 'price': 0},
    'VOO':    {'quantity': 0.64399000,    'targetPercent': (0.2  * 0.5),            'type': 'US', 'price': 0},
    'BIL':    {'quantity': 1.86310000,    'targetPercent': (0.2  * 0.30),           'type': 'US', 'price': 0},
    'VNQ':    {'quantity': 1.76097000,    'targetPercent': (0.2  * 0.20),           'type': 'US', 'price': 0},
    'BTC':    {'quantity': 0.00318941,    'targetPercent': (0.05 * 0.80),           'type': 'CR', 'price': 0},
    'ETH':    {'quantity': 0.02053750,    'targetPercent': (0.05 * 0.20),           'type': 'CR', 'price': 0},
    'RE':     {'quantity': 1500.00000000, 'targetPercent': (0.10),                  'type': 'BR', 'price': 1},
}


# Write the contribution report
def print_report(contribution):
    with open("report.txt", "w") as file:
        for asset, properties in contribution.items():
            asset_name = asset.ljust(20)
            quantity = "{:.8f}".format((properties['quantity'])).ljust(20)
            value = "{:.3f}".format(properties['value']).ljust(20)
            line = f"Asset: {asset_name} Quantity: {quantity} Value: {value}\n"
            file.write(line)


# Write the portfolio report
def print_portfolio():
    with open("portfolio.txt", "w") as file:
        total_portfolio = 0
        for asset, properties in assets.items():
            asset_name = asset.ljust(20)
            quantity = "{:.8f}".format((properties['quantity'])).ljust(20)
            price = "{:.3f}".format(properties['price']).ljust(20)
            value = "{:.3f}".format(properties['quantity'] * properties['price']).ljust(20)
            line = f"Asset: {asset_name} Quantity: {quantity} Price: {price} Value: {value}\n"
            file.write(line)
            total_portfolio += (properties['quantity'] * properties['price'])
        total_portfolio = "{:.3f}".format(total_portfolio)
        file.write(f"\nTotal portfolio: R$ {total_portfolio}\n")


# Get the current dollar value in reais
def get_usd_to_brl_price():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    response = requests.get(url)
    data = response.json()
    return float(data["USDBRL"]["bid"])


# Get current prices of BR assets
def update_br_assets_prices():
    url = "https://brapi.dev/api/quote/list?sortBy=name&sortOrder=asc&token=2RpfSrYsBy4i23T6TLdZa2"
    response = requests.get(url)
    data = response.json()

    for stock in data['stocks']:
        if stock['stock'] in assets and assets[stock['stock']]['type'] == 'BR':
            assets[stock['stock']]['price'] = stock['close']


# Get the current price of a US asset
def update_us_assets_prices(symbol):
    api_key = 'YOUR_API_KEY'
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if 'Global Quote' in data:
        price = float(data['Global Quote']['05. price'])
        assets[symbol]['price'] = (price * get_usd_to_brl_price())


# Get the current price of a crypto
def update_crypto_prices(symbol):
    url = f'https://economia.awesomeapi.com.br/last/{symbol}-BRL'
    response = requests.get(url)
    data = response.json()
    assets[symbol]['price'] = float(data[f'{symbol}BRL']['bid'])


# Calculate and make contributions according to the desired percentages
def distribute_contributions(total_contribution):
    new_assets = {}

    while total_contribution > 0:
        # Calculates the total value of the portfolio
        total_value_portfolio = sum(properties['quantity'] * properties['price'] for properties in assets.values())

        # Calculates the current percentages of each asset
        current_percentages = {asset: (properties['quantity'] * properties['price'] / total_value_portfolio) * 100
                               for asset, properties in assets.items()}

        # Finds the asset with the highest percentage difference
        asset_highest_difference = max(assets.items(), key=lambda x: x[1]['targetPercent'] * 100 - current_percentages[x[0]])

        # Get the minimum tick
        minimum_tick = 1 if asset_highest_difference[1]['type'] == 'BR' else 0.01 if asset_highest_difference[1]['type'] == 'US' else 0.0001

        # Calculates the financial amount to be contributed
        amount_to_contribute = asset_highest_difference[1]['price'] * minimum_tick

        # Checks if the financial amount to be contributed is greater than the total contribution
        if amount_to_contribute > total_contribution:
            break

        # Update the total contribution
        total_contribution -= amount_to_contribute

        # Add the new asset
        if asset_highest_difference[0] not in new_assets:
            new_assets[asset_highest_difference[0]] = {'quantity': minimum_tick, 'value': amount_to_contribute}
        else:
            new_assets[asset_highest_difference[0]]['quantity'] += minimum_tick
            new_assets[asset_highest_difference[0]]['value'] += amount_to_contribute

        # Update assets quantity
        assets[asset_highest_difference[0]]['quantity'] += minimum_tick

    print_report(new_assets)


# Main function
def main():
    # Request the amount of the contribution from the user
    total_contribution = float(input("Enter the contribution amount: "))
    print("Calculating...")

    # Update BR prices
    update_br_assets_prices()

    # Update US prices
    for symbol, properties in assets.items():
        if properties['type'] == 'US':
            update_us_assets_prices(symbol)

    # Update crypto prices
    for symbol, properties in assets.items():
        if properties['type'] == 'CR':
            update_crypto_prices(symbol)

    # Calculate the contributions
    distribute_contributions(total_contribution)

    print_portfolio()
    print("Finished")


if __name__ == "__main__":
    main()
