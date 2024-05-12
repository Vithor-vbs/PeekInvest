import requests
import pandas as pd
from io import StringIO
import numpy as np
import pprint

#79LYIIN6023AXMH8
chave_api = "79LYIIN6023AXMH8"

acoes = ['ITUB4']
acao = 'ITUB4'
margem_anos = 5
dividendo_desejado_porc = 0.06

# url_earnings_quote = f'https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo'
# r_earnings_quote = requests.get(url_earnings_quote)

def convert_to_float(lst):
    return [float(item['reportedEPS']) for item in lst]


url_global_quote = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo'
# url_global_quote = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={acao}.SAO&apikey={chave_api}'
r_global_quote = requests.get(url_global_quote)
if r_global_quote.status_code == 200:
    # pprint.pprint(r_global_quote.json())
    dados_global_quote = r_global_quote.json()
    preco_atual = float(dados_global_quote['Global Quote']['05. price'])
else:
    print(f"Falha ao obter dados do GLOBAL_QUOTE para {acao}")

url_earnings = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo'
# url_earnings = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={acao}&apikey={chave_api}'
r_earnings = requests.get(url_earnings)
if r_earnings.status_code == 200:
    dados_earnings = r_earnings.json()
    # pprint.pprint(dados_earnings)
    # get avg eps
    eps_values = convert_to_float(dados_earnings['annualEarnings'])
    eps_recent_years = eps_values[:margem_anos]
    eps_average = sum(eps_recent_years) / len(eps_recent_years)

    ultima_entrada_anual = dados_earnings['annualEarnings'][0] 
    eps = float(ultima_entrada_anual['reportedEPS'])
else:
    print(f"Falha ao obter dados de ganhos para {acao}")

url_overview = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo'
# url_overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={acao}&apikey={chave_api}'
r_overview = requests.get(url_overview)
if r_overview.status_code == 200:
    dados_overview = r_overview.json()
    pprint.pprint(dados_overview)
    beta = float(dados_overview.get('Beta', 1))  # Se não houver beta, assumimos 1 para evitar divisão por zero
    diluted_eps = float(dados_overview.get('DilutedEPSTTM', 0))

    dividend_per_share = float(dados_overview.get('DividendPerShare', 0))
    
    book_value = float(dados_overview.get('BookValue', 0))
    profit_margin = float(dados_overview.get('ProfitMargin', 0))
else:
    print(f"Falha ao obter dados do OVERVIEW para {acao}")

print(f"Preço atual: {preco_atual}")
print(f"eps: {eps}")

p_e_ratio = preco_atual / diluted_eps
graham_number = np.sqrt(22.5 * diluted_eps * book_value)
dividend_yield = (dividend_per_share / preco_atual) * 100  # Em percentual
margin_of_safety = (book_value - preco_atual) / book_value * 100  # Em percentual
graham_formula_value = diluted_eps * (8.5 + 2 * beta)
# intrinsic_value = graham_formula_value * (4.4 / yield_rate)

preco_teto_proj = eps_average / dividendo_desejado_porc


peter_lynch_ratio = (preco_atual / eps) * 0.10  # Assumindo uma taxa de crescimento de 10%

print(f"Preço/Lucro: {p_e_ratio:.2f}")
print(f"Margem de segurança: {margin_of_safety:.2f}%")
print(f"Margem de lucro: {profit_margin:.2f}%")
print(f"Dividendos por ação: {dividend_per_share}")
print(f"Valor por ação: {book_value}")
print(f"Relação Peter Lynch: {peter_lynch_ratio:.2f}")
print(f"Valor intrínseco Graham: {graham_formula_value:.2f}")
print(f"preço teto projetivo: {preco_teto_proj:.2f} ")
print(f"Dividend Yield: {dividend_yield:.2f}%")

