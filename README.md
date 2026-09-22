# Quantitative Risk Dashboard

A strategy evaluation and comparison platform built with Streamlit, Plotly, and Python.
Built as part of the ZeTheta Algorithms quantitative risk training project.

## Live App
[View the deployed dashboard](https://mcnb3vsdp3yuu7axf3jey4.streamlit.app/)

## Features

1. **Custom Strategy Input** — enter any tickers via the sidebar (comma separated); SPY is always included in the background as a market benchmark
2. **Sharpe Ratio Calculation** — annualized risk-adjusted return per strategy
3. **Sharpe Ratio Significance Testing** — bootstrap resampling (1,000 iterations) to build 95% confidence intervals, testing whether a strategy's edge is statistically real or just noise
4. **Strategy Correlation Analysis** — pairwise correlation matrix + heatmap, for assessing diversification
5. **Drawdown Analysis** — max drawdown and underwater equity curves per strategy
6. **Regime Performance Attribution** — splits history into high/low volatility regimes (based on SPY's rolling 21-day volatility) and recalculates Sharpe ratios per regime
7. **Capacity Estimation** — simplified daily capital capacity estimate based on average daily dollar volume and a 5% max market participation assumption
8. **Strategy Selection Summary** — combines all metrics into one ranked table
9. **Graceful error handling** — invalid or missing tickers show a clear warning instead of crashing the app

## Tech Stack
- **Streamlit** — dashboard framework
- **yfinance** — real market data
- **Pandas / NumPy** — data processing
- **SciPy** — statistical calculations
- **Plotly** — interactive visualizations

## Methodology Notes
- Sharpe ratios are annualized using √252 (trading days per year)
- Significance testing uses bootstrap resampling rather than a parametric t-test, since it makes no distributional assumptions about returns
- Capacity estimation is a simplified illustrative model (average daily dollar volume × 5% max participation) — real-world capacity models also incorporate market impact curves and execution strategy
- Regime classification is based on a simple median split of rolling volatility; a production version could use more robust regime-detection methods (e.g. HMMs)

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author
Vijeta Shrivastava
