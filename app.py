import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="QuarterChart Clone", layout="wide")

# Sidebar navigation stubs
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "Rankings", "Screener", "Watchlist", "Treemap"])

# All features open to everyone
st.session_state.tier = 'Premium'

# Home page
if page == "Home":
        st.title("Top Stock Rankings")

    # Top tickers
        tickers = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'AVGO', 'ASML', 'ORCL']

    data = []
    for symbol in tickers:
                try:
                                ticker = yf.Ticker(symbol)
                                info = ticker.info
                                hist = yf.download(symbol, period='5d', progress=False)['Close']

                    # Basics
                                mcap = info.get('marketCap', 0) / 1e12 if info.get('marketCap') else 0
                                sector = info.get('sector', 'N/A')
                                price = info.get('currentPrice', 0)

                    # Quarterly rev/earn
                                financials = ticker.quarterly_financials
                                rev = financials.loc['Total Revenue'].sum() / 1e9 if 'Total Revenue' in financials.index else 0
                                earn = financials.loc['Net Income'].sum() / 1e9 if 'Net Income' in financials.index else 0

                    # Score
                                pe = info.get('trailingPE', 0)
                                if pe and pe > 0:
                                                    score = min(100, max(0, 50 + (20 / (pe + 1)) * 100))
                else:
                                    score = 50

                    data.append({
                                        'Rank': len(data)+1,
                                        'Ticker': symbol,
                                        'Company': info.get('longName', symbol),
                                        'Sector': sector,
                                        'Price': round(price, 2),
                                        'MCap (T)': round(mcap, 2),
                                        'Rev (B)': round(rev, 1),
                                        'Earn (B)': round(earn, 1),
                                        'Score': round(score, 0),
                    })
except Exception as e:
            data.append({
                                'Rank': len(data)+1,
                                'Ticker': symbol,
                                'Company': symbol,
                                'Sector': 'N/A',
                                'Price': 0,
                                'MCap (T)': 0,
                                'Rev (B)': 0,
                                'Earn (B)': 0,
                                'Score': 0,
            })

    df = pd.DataFrame(data)

    # Search/Filter/Sort
    search = st.text_input("Search tickers/companies")
    if search:
                df = df[df['Ticker'].str.contains(search, case=False) | df['Company'].str.contains(search, case=False)]

    sector_filter = st.multiselect("Filter by Sector", df['Sector'].unique())
    if sector_filter:
                df = df[df['Sector'].isin(sector_filter)]

    # Display table
    st.dataframe(
                df,
                use_container_width=True,
                height=600,
                hide_index=True
    )

    # Charts
    col1, col2 = st.columns(2)
    with col1:
                st.subheader("Revenue Bars (Quarterly)")
        fig_rev = px.bar(df.head(5), x='Ticker', y='Rev (B)', title="Top 5 Revenue")
        st.plotly_chart(fig_rev, use_container_width=True)

    with col2:
                st.subheader("Score Distribution")
        fig_score = px.histogram(df, x='Score', nbins=10, title="Scores")
        st.plotly_chart(fig_score, use_container_width=True)

# Other pages stubs
elif page == "Rankings":
    st.title("Rankings")
    st.info("Rankings page stub. Full features for Pro tier.")

elif page == "Screener":
    st.title("Screener")
    st.info("Advanced screener. Filters, exports for paid users.")

elif page == "Watchlist":
    st.title("Watchlist")
    st.info("Manage your watchlist here.")

elif page == "Treemap":
    st.title("Treemap")
    st.info("Interactive market cap treemap. Pro feature.")

st.sidebar.markdown("---")
st.sidebar.caption("Open to everyone")
