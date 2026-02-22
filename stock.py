import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Stock Analysis Explorer", layout="wide")

st.title("📈 Stock Data Analysis")
st.markdown("A simple webpage to fetch and analyze stock data using Alpha Vantage.")

# API key
API_KEY = "2M9U9NCP50GLP3J7"

# Input form
with st.sidebar:
    st.header("Settings")
    symbol = st.text_input("Enter Stock Symbol", "IBM").upper()
    fetch_btn = st.button("Fetch Data", type="primary")

if fetch_btn:
    with st.spinner(f"Fetching data for {symbol}..."):
        # API URL
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
        
        try:
            # Send GET request
            response = requests.get(url)
            data = response.json()
            
            if "Time Series (Daily)" in data:
                time_series = data["Time Series (Daily)"]
                
                # Convert to DataFrame
                df = pd.DataFrame.from_dict(time_series, orient='index')
                df.index = pd.to_datetime(df.index)
                
                # Rename columns and convert to float
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df = df.astype(float)
                
                # Sort index so oldest date is first (better for charts)
                df = df.sort_index()

                st.success(f"Data fetched successfully for {symbol}!")
                
                # Key Metrics
                col1, col2, col3 = st.columns(3)
                latest_close = df['Close'].iloc[-1]
                prev_close = df['Close'].iloc[-2]
                pct_change = ((latest_close - prev_close) / prev_close) * 100
                
                col1.metric("Latest Close Price", f"${latest_close:.2f}", f"{pct_change:.2f}%")
                col2.metric("Period High", f"${df['High'].max():.2f}")
                col3.metric("Period Low", f"${df['Low'].min():.2f}")
                
                st.divider()
                
                # Charts
                st.subheader(f"{symbol} Closing Price Over Time")
                st.line_chart(df['Close'], width='stretch')
                
                # Raw Data
                with st.expander("View Raw Data"):
                    st.dataframe(df.sort_index(ascending=False))
                    
            else:
                st.error("Error fetching data. Check the symbol or try again.")
                if "Information" in data:
                    st.warning(data["Information"])
                elif "Note" in data:
                    st.warning(data["Note"])
                else:
                    st.json(data)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")