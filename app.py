import streamlit as st
import yfinance as sf
import pandas as pd

st.title("Vijeta's Quantitative Risk Dashboard")

# Let's grab data for a couple of tickers
st.sidebar.header("⚙️ Settings")
ticker_input = st.sidebar.text_input("Enter tickers (comma separated)", "AAPL,MSFT,SPY")
tickers = [t.strip().upper() for t in ticker_input.split(",")]
# Always include SPY as our market benchmark, even if not in the user's list
benchmark = "SPY"
download_tickers = list(set(tickers + [benchmark]))

st.write("Fetching data for:", tickers)

data = sf.download(download_tickers, period="2y")["Close"]

st.write("Here's a peek at the raw data:")
st.dataframe(data.head())
st.write("Now let's calculate daily returns:")
returns = data.pct_change().dropna()

st.dataframe(returns.head())
import numpy as np
st.header("1️⃣ Sharpe Ratios")

st.write("Sharpe Ratios (annualized):")

mean_returns = returns.mean()
std_returns = returns.std()

sharpe_ratios = (mean_returns / std_returns) * np.sqrt(252)

st.dataframe(sharpe_ratios)
st.header("2️⃣ Sharpe Ratio Significance Testing")

st.write("Sharpe Ratio Significance Testing (Bootstrap):")

n_bootstrap = 1000
bootstrap_results = {}

for ticker in returns.columns:
    ticker_returns = returns[ticker].values
    boot_sharpes = []
    
    for i in range(n_bootstrap):
        sample = np.random.choice(ticker_returns, size=len(ticker_returns), replace=True)
        boot_sharpe = (sample.mean() / sample.std()) * np.sqrt(252)
        boot_sharpes.append(boot_sharpe)
    
    lower = np.percentile(boot_sharpes, 2.5)
    upper = np.percentile(boot_sharpes, 97.5)
    bootstrap_results[ticker] = {"lower_95": lower, "upper_95": upper}

st.write(bootstrap_results)
import plotly.express as px
st.header("3️⃣ Strategy Correlation")


st.write("Strategy Correlation Matrix:")

corr_matrix = returns.corr()

st.dataframe(corr_matrix)

fig = px.imshow(
    corr_matrix,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    title="Strategy Correlation Heatmap"
)

st.plotly_chart(fig)
st.header("4️⃣ Drawdown Analysis")
st.write("Drawdown Analysis:")

# Turn returns into a cumulative growth curve (starting at 1.0)
cumulative = (1 + returns).cumprod()

# Track the running maximum (the highest peak so far, at each point in time)
running_max = cumulative.cummax()

# Drawdown = how far below that peak we currently are, as a %
drawdown = (cumulative - running_max) / running_max

st.write("Max Drawdown per strategy:")
st.dataframe(drawdown.min())

fig_dd = px.line(
    drawdown,
    title="Drawdown Over Time (Underwater Chart)"
)
fig_dd.update_layout(yaxis_tickformat=".0%")

st.plotly_chart(fig_dd)
st.header("5️⃣ Regime Performance")
st.write("Regime Performance Attribution:")

# Using SPY's rolling 21-day volatility as our "market mood" indicator
spy_vol = returns["SPY"].rolling(21).std()

# Split into regimes based on whether volatility is above or below its median
vol_median = spy_vol.median()
regime = spy_vol.apply(lambda x: "High Volatility" if x > vol_median else "Low Volatility")

# Attach the regime label to our returns data
returns_with_regime = returns.copy()
returns_with_regime["Regime"] = regime

st.write("Average annualized Sharpe ratio, by regime:")

regime_sharpe = returns_with_regime.groupby("Regime").apply(
    lambda x: (x[tickers].mean() / x[tickers].std()) * np.sqrt(252)
)

st.dataframe(regime_sharpe)
st.header("6️⃣ Capacity Estimation")
st.write("Capacity Estimation (Simplified):")

# Grab average daily dollar volume for each ticker over the same period
volume_data = sf.download(tickers, period="2y")["Volume"]
price_data = data  # we already have this from earlier

avg_daily_volume = volume_data.mean()
avg_price = price_data.mean()

avg_daily_dollar_volume = avg_daily_volume * avg_price

# Assumption: a strategy shouldn't be more than 5% of daily volume, to avoid moving the market
max_participation_rate = 0.05

estimated_capacity = avg_daily_dollar_volume * max_participation_rate

st.write("Estimated daily capacity (assuming 5% max participation):")
st.dataframe(estimated_capacity)

st.caption("Note: this is a simplified illustrative model based on average daily dollar volume and a 5% max participation assumption — real capacity models also factor in market impact curves, order execution strategy, and volatility.")
st.write("---")
st.header("📊 Strategy Selection Summary")

summary = pd.DataFrame({
    "Sharpe Ratio": sharpe_ratios,
    "Max Drawdown": drawdown.min(),
    "Est. Daily Capacity ($)": estimated_capacity,
})

# Rank strategies by Sharpe ratio, best first
summary = summary.sort_values("Sharpe Ratio", ascending=False)

st.dataframe(
    summary.style.format({
        "Sharpe Ratio": "{:.2f}",
        "Max Drawdown": "{:.1%}",
        "Est. Daily Capacity ($)": "${:,.0f}"
    })
)

st.caption("Ranked by Sharpe ratio (highest risk-adjusted return first). Remember: check the significance testing and regime breakdown above before trusting the Sharpe ratio alone!")