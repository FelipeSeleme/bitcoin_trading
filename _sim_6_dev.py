import json
import pandas as pd

pd.set_option('display.width', 640)
pd.set_option('display.max_columns', 100)

min_compra = 50
min_venda = 50


def compra_teste(valor):
    ultimo_reg = 0
    with open('_sim_6_memoria.json', 'r+') as f:
        reg = json.load(f)
        for item in reg:
            if float(item) > float(ultimo_reg):
                ultimo_reg = item
        with open('_sim_6_balanco.json', 'r+') as b:
            bal = json.load(b)
            if float(bal['BRL']) > min_compra:
                cotacao = reg[f'{ultimo_reg}']['sell']
                i_buy = valor * (float(bal['BRL']) / (float(bal['BTC']) * cotacao))
                if bal['BRL'] > i_buy > 50:
                    bal['BTC'] += i_buy / cotacao
                    bal['BRL'] -= i_buy
                    print(f'\n[➕] ⚠️COMPRA EFETUADA:')
                    print(f"Saldo em BRL: R$ {float(bal['BRL'])}")
                    print(f"Saldo em BTC: BTC {float(bal['BTC'])}")
                    print(f"Saldo TOTAL: R$ {float(bal['BRL']) + (float(bal['BTC']) * float(reg[f'{ultimo_reg}']['sell']))}")
                    b.seek(0)
                    json.dump(bal, b, indent=4)
                    b.truncate()


def venda_teste(valor):
    ultimo_reg = 0
    with open('_sim_6_memoria.json', 'r+') as f:
        reg = json.load(f)
        for item in reg:
            if float(item) > float(ultimo_reg):
                ultimo_reg = item
        with open('_sim_6_balanco.json', 'r+') as b:
            bal = json.load(b)
            if float(bal['BTC']) * float(reg[f'{ultimo_reg}']['sell']) > min_venda:
                cotacao = reg[f'{ultimo_reg}']['buy']
                i_sell = valor * ((float(bal['BTC']) * cotacao) / float(bal['BRL']))
                if bal['BTC'] * cotacao > i_sell > 50:
                    bal['BRL'] += i_sell
                    bal['BTC'] -= i_sell / cotacao
                    print(f'\n[➖] ⚠️VENDA EFETUADA:')
                    print(f"Saldo em BRL:  R$ {float(bal['BRL'])}")
                    print(f"Saldo em BTC: BTC {float(bal['BTC'])}")
                    print(f"Saldo TOTAL:   R$ {float(bal['BRL']) + (float(bal['BTC']) * float(reg[f'{ultimo_reg}']['sell']))}")
                    b.seek(0)
                    json.dump(bal, b, indent=4)
                    b.truncate()

