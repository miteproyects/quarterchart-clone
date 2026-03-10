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
    st.title("🏆 Top Stock Rankings")
    
    # Top tickers
    tickers = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'AVGO', 'ASML', 'ORCL']
    
    data = []
    for symbol in tickers:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = yf.download(symbol, period='5d', progress=False)['Close']
        
        # Basics
        mcap = info.get('marketCap', 0) / 1e12 if info.get('marketCap') else 0  # Trillions
        sector = info.get('sector', 'N/A')
        price = info.get('currentPrice', 0)
        
        # Sparkline data
        spark_data = hist.values if not hist.empty else []
        
        # Quarterly rev/earn (mock simplified)
        financials = ticker.quarterly_financials
        rev = financials.loc['Total Revenue'].sum() / 1e9 if 'Total Revenue' in financials.index else 0  # Billions
        earn = financials.loc['Net Income'].sum() / 1e9 if 'Net Income' in financials.index else 0
        
        # Mock DCF/Score (simple formula)
        pe = info.get('trailingPE', 0)
        score = min(100, 50 + (20 / (pe + 1)) * 100 + np.random.randint(-10, 10))  # Mock
        
        data.append({
            'Rank': len(data)+1,
            'Ticker': symbol,
            'Company': info.get('longName', symbol),
            'Sector': sector,
            'Price': f"${price:,.2f}",
            'MCap (T)': f"{mcap:.2f}",
            'Rev (B)': f"{rev:.1f}",
            'Earn (B)': f"{earn:.1f}",
            'Score': f"{score:.0f}",
            '1D Sparkline': spark_data
        })
    
    df = pd.DataFrame(data)
    
    # Search/Filter/Sort
    search = st.text_input("Search tickers/companies")
    if search:
        df = df[df['Ticker'].str.contains(search, case=False) | df['Company'].str.contains(search, case=False)]
    
    sector_filter = st.multiselect("Filter by Sector", df['Sector'].unique())
    if sector_filter:
        df = df[df['Sector'].isin(sector_filter)]
    
    # Score color
    def score_color(val):
        score = float(str(val).replace('%', ''))
        if score >= 90: return 'excellent'
        elif score >= 70: return 'good'
        elif score >= 50: return 'fair'
        elif score >= 30: return 'poor'
        else: return 'very-poor'
    
    # Display table (sortable, responsive)
    st.dataframe(
        df.style.format({
            'Price': '{:.2f}',
            'MCap (T)': '{:.2f}',
            'Rev (B)': '{:.1f}',
            'Earn (B)': '{:.1f}',
            'Score': '{:.0f}'
        }).map(score_color, subset=['Score']),
        use_container_width=True,
        height=600,
        hide_index=True
    )
    
    # Mock charts
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
st.sidebar.caption("🌐 Open to everyone")