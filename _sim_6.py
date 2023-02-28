from bitpreco import public_data
from _sim_6_dev import compra_teste, venda_teste
from datetime import datetime
from tqdm import tqdm
import time
import json

# Simulador com índice inteligente de compra e venda com altas e baixas das últimas 24h

t_exec = 1440  # (MINUTOS) duração de execução do código
t_registro = 1  # (MINUTOS) tempo do registro dos preços das cotações
t_espera = 30  # (SEGUNDOS) tempo de espera entre cada ciclo
bid_ref = 500  # (R$) valor de referência para as transações
var_com = -1.0  # % de variação das últimas 24h para ordem de compra
var_ven = 1.0  # % de variação das últimas 24h para ordem de venda

# configura a barra de progresso:
n = int(t_exec * 60 / t_espera)
pbar = tqdm(total=n, position=0, leave=True)

# abre o arquivo de registro de cotações:
with open('_sim_6_memoria.json', 'r+') as f:
    reg = json.load(f)
# verifica o número máximo de registros e realiza a limpeza dos valores antigos:
    ciclos = int(t_exec * 60 / t_espera)
    for i in range(ciclos):
        if len(reg) > int(t_registro * 60 / t_espera):
            limpa_reg = float('inf')
            for item in reg:
                if float(item) < float(limpa_reg):
                    limpa_reg = item
            reg.pop(limpa_reg)
            f.seek(0)
            json.dump(reg, f, indent=4)
            f.truncate()
        elif len(reg) < int(t_registro * 60 / t_espera):
            print(f'\nA memória possui {len(reg)} de {int(t_registro * 60 / t_espera)} registro(s).')
            reg[str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '').replace('.', '')] = public_data('ticker')
            f.seek(0)
            json.dump(reg, f, indent=4)
            f.truncate()
# adiciona a cotação em tempo real no registro de cotações:
        else:
            print(f'\nA memória possui {len(reg)} de {int(t_registro * 60 / t_espera)} registro(s).')
            reg[str(datetime.now()).replace('-', '').replace(':', '').replace(' ', '').replace('.', '')] = public_data('ticker')
            f.seek(0)
            json.dump(reg, f, indent=4)
            f.truncate()
# define o maior e menor valor no período integral e identifica o último registro adicionado:
            ultimo_reg = 0
            primeiro_reg = float('inf')
            for cotacao in reg:
                data = int(cotacao)
                if data < primeiro_reg:
                    primeiro_reg = data
                    v_prim = reg[f'{cotacao}']['var']
                if data > ultimo_reg:
                    ultimo_reg = data
                    maior = reg[f'{cotacao}']['high']
                    menor = reg[f'{cotacao}']['low']
                    media = reg[f'{cotacao}']['avg']
                    varia = reg[f'{cotacao}']['var']
            print(f'\nMédia  24h   BTC {float(media)}')
            print(f'Máxima 24h   BTC {float(maior)}')
            print(f'Mínima 24h   BTC {float(menor)}')
            print(f'Valor atual  BTC {float(reg[str(ultimo_reg)]["last"])}')
            print(f'Variação 24h        {float(varia)}')
        # gera a ordem de compra e venda
            if varia > var_ven and varia > v_prim:
                venda_teste(bid_ref)
            if varia < var_com and varia < v_prim:
                compra_teste(bid_ref)
        pbar.update()
        time.sleep(t_espera)
