import pandas as pd
import numpy as np
from scipy.optimize import minimize
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Disable mathtext for all text elements to prevent $ parsing issues
plt.rcParams['text.usetex'] = False

# User input
bankroll = float(input("What is your total bankroll? ($__) >>> "))
assets = input("What stocks do you want to invest in? (comma separated) >>> ").split(", ")

# Download data
df = yf.download(assets, period='1y')
prices = df['Close']
returns = prices.pct_change().dropna()

# Annualize both returns and covariance consistently
mean_returns = returns.mean().values * 252  # Annualized
cov_matrix = returns.cov().values * 252     # Annualized
num_assets = len(mean_returns)

def portfolio_variance(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))

init_guess = num_assets * [1. / num_assets]
bounds = tuple((0, 1) for asset in range(num_assets))

# Efficient frontier
frontier_vol = []
frontier_ret = []
frontier_weights = []
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
        frontier_weights.append(result.x)

# Tangency (max Sharpe ratio) portfolio
risk_free_rate = 0.04  # Annualized rate (4% annual)

def neg_sharpe(weights, mean_returns, cov_matrix, rf):
    port_ret = np.dot(weights, mean_returns)
    port_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return -((port_ret - rf) / port_vol)

tangent_result = minimize(neg_sharpe, init_guess, args=(mean_returns, cov_matrix, risk_free_rate),
                          method='SLSQP', bounds=bounds, 
                          constraints={'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

w_tangent = tangent_result.x
ret_tangent = np.dot(w_tangent, mean_returns)
vol_tangent = np.sqrt(np.dot(w_tangent.T, np.dot(cov_matrix, w_tangent)))

# Capital Allocation Line (CAL)
cal_x = np.linspace(0, max(frontier_vol)*1.2, 100)
cal_y = risk_free_rate + ((ret_tangent - risk_free_rate)/vol_tangent) * cal_x

# Function to find portfolio on CAL for given volatility
def get_portfolio_on_cal(target_vol):
    """
    Returns the portfolio allocation along the CAL for a given target volatility.
    This combines the risk-free asset with the tangency portfolio.
    """
    if target_vol <= 0:
        # 100% risk-free asset
        weight_risky = 0
    else:
        # Weight in risky (tangency) portfolio
        weight_risky = target_vol / vol_tangent
    
    weight_rf = 1 - weight_risky
    
    # Expected return on CAL
    expected_return = risk_free_rate + ((ret_tangent - risk_free_rate)/vol_tangent) * target_vol
    
    # Actual portfolio weights (including risk-free)
    portfolio_weights = weight_risky * w_tangent
    
    return weight_risky, weight_rf, expected_return, portfolio_weights

# Initial target volatility (start at tangency portfolio)
initial_vol = vol_tangent

# Create the plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
plt.subplots_adjust(bottom=0.25)

# Left plot: Efficient Frontier
ax1.plot(frontier_vol, frontier_ret, label='Efficient Frontier', linewidth=2)
ax1.plot(cal_x, cal_y, linestyle='--', label='Capital Allocation Line (CAL)', linewidth=2, color='orange')
ax1.scatter([vol_tangent], [ret_tangent], c='r', marker='*', s=200, 
            label='Tangency Portfolio', zorder=5)
ax1.scatter([0], [risk_free_rate], c='g', marker='o', s=100, 
            label='Risk-free Asset', zorder=5)

# User's selected portfolio point
weight_risky, weight_rf, expected_return, portfolio_weights = get_portfolio_on_cal(initial_vol)
user_point = ax1.scatter([initial_vol], [expected_return], c='blue', marker='D', s=150, 
                         label='Your Portfolio', zorder=6)

ax1.set_xlabel('Volatility (Annualized Std Dev)')
ax1.set_ylabel('Expected Return (Annualized)')
ax1.legend()
ax1.set_title('Efficient Frontier and Capital Allocation Line')
ax1.grid(True, alpha=0.3)

# Right plot: Portfolio Allocation
allocation_labels = assets + ['Risk-free']
allocation_values = list(portfolio_weights * bankroll) + [weight_rf * bankroll]
bars = ax2.barh(allocation_labels, allocation_values, color=['steelblue']*len(assets) + ['green'])
ax2.set_xlabel('Allocation (USD)')
ax2.set_title('Portfolio Allocation')
ax2.grid(True, alpha=0.3, axis='x')

# Add value labels on bars - ESCAPE dollar signs for matplotlib
for i, (bar, val) in enumerate(zip(bars, allocation_values)):
    if val > 0:
        label_text = r'\${:.2f}'.format(val)
        ax2.text(val, bar.get_y() + bar.get_height()/2, label_text, 
                va='center', ha='left', fontsize=9)

# Create slider
ax_slider = plt.axes([0.15, 0.1, 0.7, 0.03])
vol_slider = Slider(
    ax=ax_slider,
    label='Target Volatility',
    valmin=0,
    valmax=max(frontier_vol)*1.5,
    valinit=initial_vol,
    valstep=0.001
)

# Text box for statistics - ESCAPE dollar signs
stats_text = fig.text(0.15, 0.05, '', fontsize=10, family='monospace')

def update_stats(target_vol):
    weight_risky, weight_rf, expected_return, portfolio_weights = get_portfolio_on_cal(target_vol)
    sharpe = (expected_return - risk_free_rate) / target_vol if target_vol > 0 else 0
    
    # Use raw string with escaped dollar signs
    stats_str = r"Target Volatility: {:.2f}% | Expected Return: {:.2f}% | Sharpe Ratio: {:.3f}".format(
        target_vol*100, expected_return*100, sharpe) + "\n"
    stats_str += r"Risky Assets: {:.2f}% (\${:.2f}) | Risk-free: {:.2f}% (\${:.2f})".format(
        weight_risky*100, weight_risky*bankroll, weight_rf*100, weight_rf*bankroll)
    
    if weight_risky > 1:
        leverage = weight_risky - 1
        stats_str += r" | LEVERAGED: Borrowing \${:.2f} at risk-free rate".format(leverage*bankroll)
    
    stats_text.set_text(stats_str)

# Update function for slider
def update(val):
    target_vol = vol_slider.val
    weight_risky, weight_rf, expected_return, portfolio_weights = get_portfolio_on_cal(target_vol)
    
    # Update user point on left plot
    user_point.set_offsets([[target_vol, expected_return]])
    
    # Update allocation bars on right plot
    allocation_values = list(portfolio_weights * bankroll) + [weight_rf * bankroll]
    
    for bar, val in zip(bars, allocation_values):
        bar.set_width(val)
    
    # Update bar labels - ESCAPE dollar signs
    for txt in ax2.texts:
        txt.remove()
    for i, (bar, val) in enumerate(zip(bars, allocation_values)):
        if val > 0:
            label_text = r'\${:.2f}'.format(val)
            ax2.text(val, bar.get_y() + bar.get_height()/2, label_text, 
                    va='center', ha='left', fontsize=9)
    
    # Update x-axis limit for better visualization
    ax2.set_xlim(0, max(allocation_values)*1.15 if max(allocation_values) > 0 else bankroll)
    
    # Update statistics
    update_stats(target_vol)
    
    fig.canvas.draw_idle()

# Initialize stats
update_stats(initial_vol)

vol_slider.on_changed(update)

# Print initial portfolio info - console output doesn't need escaping
print("\n" + "="*60)
print("INITIAL PORTFOLIO (Tangency Portfolio)")
print("="*60)
print("Total Bankroll: ${:,.2f}".format(bankroll))
print("\nTangency Portfolio:")
print("  Volatility: {:.4f} ({:.2f}%)".format(vol_tangent, vol_tangent*100))
print("  Expected Return: {:.4f} ({:.2f}%)".format(ret_tangent, ret_tangent*100))
print("  Sharpe Ratio: {:.4f}".format((ret_tangent - risk_free_rate)/vol_tangent))
print("\nWeights:")
for i, asset in enumerate(assets):
    print("  {}: {:.2f}% (${:,.2f})".format(asset, w_tangent[i]*100, w_tangent[i]*bankroll))
print("="*60 + "\n")

plt.show()
