# QuarterChart Streamlit Clone

Exact clone of quarterchart.com homepage table using Streamlit, yfinance, Plotly.

## Local Run
```bash
cd quarterchart-clone
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
streamlit run app.py
```

Tested on port 8502 headless.

## Deploy to Streamlit Cloud
1. Create GitHub repo: `quarterchart-clone` (public)
2. `git remote add origin https://github.com/YOURUSERNAME/quarterchart-clone.git`
3. `git push -u origin main`
4. Visit [share.streamlit.io](https://share.streamlit.io), "New app" → connect GitHub → select repo → deploy.

Live URL will be like: https://quarterchart-clone.streamlit.app

## Features
- Top tickers table: NVDA, AAPL etc. (mcap, sector, price, rev/earn, score, 1D sparkline)
- Search, filter sector, sort
- Sidebar nav stubs
- Mock login/paywall
- Responsive, charts