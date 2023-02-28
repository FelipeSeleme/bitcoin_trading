import requests
from chaves import auth_token_btp

# documentação completa: https://bitpreco.com/api

# modos: simulação / API oficial
simulador = True  # True: API de simulação ativa; False: API OFICIAL
if simulador:
    sim = '-simulator'
    print('🟢 Executando em ambiente de SIMULAÇÃO')
else:
    print('🔴 ATENÇÃO: Executando ações na API OFICIAL!')
    confirmacao = input('Deseja contunuar? [s/n]: ')
    if confirmacao.lower() == 's':
        sim = ''
        print('✔️Continuando no ambiente da API OFICIAL.')
    else:
        print('⛔ OPERAÇÃO CANCELADA')
        exit()


# dados públicos
def public_data(dados='ticker'):  # ticker, orderbook ou trades
    """ Busca informações em tempo real.

    Parameters: ticker: Returns current prices.
    orderbook: Returns a list with open sell orders and open buy orders.
    trades: Returns a list of already executed orders.

    Returns: retorna as informações em formato de dicionário.
    """
    url = f'https://api{sim}.bitpreco.com/btc-brl/'
    return requests.get(url + dados).json()


def trading_data(operacao='balance', market='BTC-BRL'):  # balance, open_orders, executed_orders,
    """ Busca os saldos em carteira.

    Parameters: balance: Returns current balance of the user account.
    open_orders: Returns open orders made by user.
    executed_orders: Returns the last executed orders in our platform.,
    market: 'BTC-BRL'.

    Returns: retorna as saldos em formato de dicionário.
    """
    url = f'https://api{sim}.bitpreco.com/trading/'
    return requests.post(url, data={'cmd': f'{operacao}',
                                    'auth_token': f'{auth_token_btp}',
                                    'market': f'{market}'}).json()


def trading_request(operacao, valor, limited=False, price=None, market='BTC-BRL'):  # buy, sell
    """ Executa ordens de compra e venda.

    Parameters: buy: Places a buy order.
    sell: Places a sell order.

    Returns: executa as ordens de compra ou venda.
    """
    url = f'https://api{sim}.bitpreco.com/trading/'
    return requests.post(url, data={'cmd': f'{operacao}',
                                    'auth_token': f'{auth_token_btp}',
                                    'market': f'{market}',
                                    'price': f'{price}',
                                    'volume': f'{valor}',
                                    'amount': f'{valor}',
                                    'limited': f'{limited}'}).text


def order_options(ordem='order_status', order_id=None):  # order_cancel, order_status
    """ Informa o status ou cancela uma ordem em específico através do ID da ordem.

    Parameters: order_status: Returns the status of an order made by user.
    order_cancel: Cancels an order made by user.,
    order_id: Order ID

    Returns: informa o status ou executa o cancelamento da ordem informada pelo ID.
    """
    url = f'https://api{sim}.bitpreco.com/trading/'
    return requests.post(url, data={'cmd': f'{ordem}',
                                    'auth_token': f'{auth_token_btp}',
                                    'order_id': f'{order_id}'}).text


def all_orders_cancel():  # cancela todas as ordens abertas
    """ Cancela todas as ordens de compra e venda feitas pelo o usuário

    Parameters: None

    Returns: Cancela todas as ordens feitas pelo o usuário.
    """
    url = f'https://api{sim}.bitpreco.com/trading/'
    return requests.post(url, data={'cmd': 'all_orders_cancel',
                                    'auth_token': f'{auth_token_btp}'}).text


if __name__ == "__main__":

    import pandas as pd
    pd.set_option('display.width', 640)
    pd.set_option('display.max_columns', 100)

    ticker = public_data('ticker')
    # orderbook = public_data('orderbook')
    # trades = public_data('trades')
    #
    # balance = trading_data('balance')
    # open_orders = trading_data('open_orders')
    # executed_orders = trading_data('executed_orders')
    print(ticker)
