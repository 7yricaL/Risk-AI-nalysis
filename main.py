import pandas as pd
import numpy as np
from scipy.optimize import minimize
import yfinance as yf
import matplotlib.pyplot as plt

# User input
bankroll = float(input("What is your total bankroll? ($__) >>> "))
assets = input("What stocks do you want to invest in? (comma separated) >>> ").split(", ")

# Download data
df = yf.download(assets, period='1y')
prices = df['Close']
returns = prices.pct_change().dropna()
mean_returns = returns.mean().values
cov_matrix = returns.cov().values
num_assets = len(mean_returns)

def portfolio_variance(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))

init_guess = num_assets * [1. / num_assets]
bounds = tuple((0, 1) for asset in range(num_assets))

# Efficient frontier
frontier_vol = []
frontier_ret = []
target_returns = np.linspace(mean_returns.min(), mean_returns.max(), 50)

for r in target_returns:
    constraints = (
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w: np.dot(w, mean_returns) - r}
    )
    result = minimize(portfolio_variance, init_guess, args=(cov_matrix,),
                      method='SLSQP', bounds=bounds, constraints=constraints)
    if result.success:
        frontier_vol.append(np.sqrt(result.fun))
        frontier_ret.append(r)

# Tangency (max Sharpe ratio) portfolio
risk_free_rate = 0.0005  # daily, you can use annualized for long periods

def neg_sharpe(weights, mean_returns, cov_matrix, rf):
    port_ret = np.dot(weights, mean_returns)
    port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return -((port_ret - rf) / port_vol)

tangent_result = minimize(neg_sharpe, init_guess, args=(mean_returns, cov_matrix, risk_free_rate),
                          method='SLSQP', bounds=bounds, constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

w_tangent = tangent_result.x
ret_tangent = np.dot(w_tangent, mean_returns)
vol_tangent = np.sqrt(np.dot(w_tangent.T, np.dot(cov_matrix, w_tangent)))

# Capital Allocation Line (CAL)
cal_x = np.linspace(0, 2*vol_tangent, 100)
cal_y = risk_free_rate + ((ret_tangent - risk_free_rate)/vol_tangent) * cal_x


print("Tangency Portfolio Volatility:", vol_tangent)
print("Tangency Portfolio Return:", ret_tangent)
print("Frontier Volatility Range:", min(frontier_vol), max(frontier_vol))
print("Frontier Return Range:", min(frontier_ret), max(frontier_ret))

# Plotting
plt.figure(figsize=(10,6))
plt.plot(frontier_vol, frontier_ret, label='Efficient Frontier')
plt.plot(cal_x, cal_y, linestyle='--', label='Capital Allocation Line (CAL)')
plt.scatter([vol_tangent], [ret_tangent], c='r', marker='*', s=150, label='Tangency Portfolio')
plt.scatter([0], [risk_free_rate], c='g', marker='o', s=100, label='Risk-free Asset')
plt.xlabel('Volatility (Std Dev of Return)')
plt.ylabel('Expected Return')
plt.legend()
plt.title('Efficient Frontier and Capital Allocation Line')
plt.show()