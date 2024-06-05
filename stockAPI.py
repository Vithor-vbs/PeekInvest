import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import pprint
from functools import reduce
from datetime import datetime, timedelta


def fetch_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

def fetch_historical_earnings(ticker):
    stock = yf.Ticker(ticker)
    earnings = stock.dividends
    return earnings

def fetch_plot_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def plot_stock_data(stock_data, ticker):
    plt.figure(figsize=(14, 7))
    plt.plot(stock_data['Close'], label='Close Price')
    plt.title(f'{ticker} Preço da ação')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    
#------------------ User input ------------------#
ticker = 'BBAS3.SA'
months = 3 # Quantidade de meses considerados para montar o gráfico

start_date = (datetime.now() - timedelta(days=months*30)).strftime('%Y-%m-%d') 
end_date = datetime.now().strftime('%Y-%m-%d')

desired_dividend_yield = 0.06
years_to_consider = 5

#------------------------------------------------#

info = fetch_stock_info(ticker)
earnings = fetch_historical_earnings(ticker)
stock_plot_data = fetch_plot_data(ticker, start_date, end_date)

def calculate_average_dividend(earnings, num_years=5):
    df = pd.DataFrame({'Date': earnings.index, 'Dividends': earnings.values})
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    yearly_averages = df.groupby('Year')['Dividends'].sum()

    # Usando list comprehension em lambda para calcular a média
    yearly_dividend_avg = sum([dividend for dividend in yearly_averages[-num_years:]]) / num_years if len(yearly_averages) >= num_years else None

    if yearly_dividend_avg is None:
        print(f"Sem informações suficientes para calcular a média dos dividendos nos últimos {num_years} anos.")
    
    return yearly_dividend_avg

average_eps = calculate_average_dividend(earnings, years_to_consider)

# Currying com funções lambda
calculate_projected_ceiling_price = (lambda x: (lambda y: y / desired_dividend_yield if y else None))(average_eps)
projected_ceiling_price = calculate_projected_ceiling_price(average_eps)

p_e_ratio = info.get('trailingPE')
profit_margin = info.get('profitMargins')
dividend_yield = info.get('dividendYield') * 100  
dividend_per_share = info.get('dividendRate')
book_value = info.get('currentPrice')
eps = info.get('trailingEps')

# Usando lambda alta ordem
graham_formula_value = (lambda eps, bv: (lambda e, b: (22.5 * e * b) ** 0.5 if e and b else None)(eps, book_value))(eps, book_value)

# Dicionário dentro do escopo de uma função lambda
peter_lynch_ratio = (lambda d: d['pe'] / (d['gr'] * 100) if d['pe'] and d['gr'] else None)({'pe': p_e_ratio, 'gr': 0.10})

# Usando uma função lambda recursiva para calcular o total de dividendos acumulados
total_dividends = (lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))(lambda f: lambda data: 0 if not data else data[0] + f(data[1:]))
dividends_data = earnings.values.tolist() 
total_dividends_accumulated = total_dividends(dividends_data)

# Usando `reduce` como um functor
dividends_sum = reduce(lambda x, y: x + y, earnings, 0)

# Usando o monad lambda
maybe_monad = (lambda value: (lambda func: None if value is None else func(value))) 

monad_result = maybe_monad(average_eps)(lambda x: x / 0.06 if x else None)


print("\nInformações sobre a ação:")
print(f"Ticker: {ticker}")
print(f"Preço/Lucro: {p_e_ratio:.2f}")
print(f"Margem de lucro: {profit_margin:.2f}%")
print(f"Dividendos por ação: {dividend_per_share}")
print(f"Valor por ação: {book_value}")
print(f"Dividend Yield: {dividend_yield:.2f}%")

print("\nAnálise da ação:")
if graham_formula_value:
    print(f"Valor intrínseco Graham: {graham_formula_value:.2f}")
else:
    print("Valor intrínseco Graham: Informações não disponíveis")

if peter_lynch_ratio:
    print(f"Relação Peter Lynch: {peter_lynch_ratio:.2f}")
else:
    print("Relação Peter Lynch: Informações não disponíveis")

if projected_ceiling_price:
    print(f"Preço teto projetivo: {projected_ceiling_price:.2f}")
else:
    print("Preço teto projetivo: Informações não disponíveis")

print("\noutros:")
if total_dividends_accumulated is not None:
    print(f"Total de dividendos acumulados: {total_dividends_accumulated}")
else:
    print("Total de dividendos acumulados: Informações não disponíveis")

print(f"Soma total dos dividendos: {dividends_sum}")

if monad_result is not None:
    print(f"Resultado do Monad: {monad_result:.2f}")
else:
    print("Resultado do Monad: Informações não disponíveis")
    

plot_stock_data(stock_plot_data, ticker)