import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

ticker = 'IVV' # S&P 500 ETF
start_date = '2010-01-01'
end_date = '2023-12-31'
interval = '1mo' # monthly data
amount = 150 # investment amount in USD
total_investment = 0
shares = 0

# Download data
data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

data = data.dropna() # drop rows with missing values
data_one_month = data.resample('ME').first() # resample to monthly data and use the first value of each month


dollar_average_cost_log = [] # log of dollar average cost per share

for date, row in data_one_month.iterrows():
    dollar_average_cost = amount / row['Adj Close']
    total_investment += amount
    shares += amount / row['Adj Close']
    dollar_average_cost_log.append(
        {
            'Date': date,
            'Dollar Average Cost': dollar_average_cost,
            'Total Investment': total_investment,
            'Shares': shares,
            'Portfolio Value': shares * row['Adj Close']
        }
    )

dollar_average_cost_df = pd.DataFrame(dollar_average_cost_log)

final_portfolio_value = dollar_average_cost_df['Portfolio Value'].iloc[-1]
total_profit = final_portfolio_value - total_investment

#Visualization
plt.figure(figsize=(10, 6))
plt.plot(dollar_average_cost_df['Date'], dollar_average_cost_df['Portfolio Value'], label='Portfolio Value')
plt.plot(dollar_average_cost_df['Date'], dollar_average_cost_df['Total Investment'], label='Total Investment')
plt.xlabel('Date')
plt.ylabel('Portfolio Value (USD)')
plt.title(f'{ticker} Portfolio Value Over Time')
plt.legend()
plt.grid(True)
plt.show()