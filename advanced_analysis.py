import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Advanced Stock Analytics", layout="wide")

st.title("📊 Advanced Stock Analytics & Transformations")
st.markdown("This dashboard fetches daily stock data and performs technical analysis and data transformations.")

# API key
API_KEY = "2M9U9NCP50GLP3J7"

with st.sidebar:
    st.header("Settings")
    symbol = st.text_input("Enter Stock Symbol", "AAPL").upper()
    ma_window1 = st.slider("Moving Average 1 (Days)", min_value=5, max_value=50, value=10)
    ma_window2 = st.slider("Moving Average 2 (Days)", min_value=10, max_value=200, value=50)
    fetch_btn = st.button("Run Analytics", type="primary")

if fetch_btn:
    with st.spinner(f"Analyzing data for {symbol}..."):
        # API URL
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if "Time Series (Daily)" in data:
                # 1. Load Data
                time_series = data["Time Series (Daily)"]
                df = pd.DataFrame.from_dict(time_series, orient='index')
                df.index = pd.to_datetime(df.index)
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df = df.astype(float)
                df = df.sort_index() # Sort chronologically

                st.success(f"Successfully transformed data for {symbol}!")

                # 2. Transformations & Analysis
                # A. Moving Averages (Smooths out price data to identify trends)
                df[f'SMA_{ma_window1}'] = df['Close'].rolling(window=ma_window1).mean()
                df[f'SMA_{ma_window2}'] = df['Close'].rolling(window=ma_window2).mean()

                # B. Daily Returns (Percentage change from previous day)
                df['Daily_Return_%'] = df['Close'].pct_change() * 100

                # C. Volatility (Standard Deviation of daily returns over a 20-day window)
                df['Volatility'] = df['Daily_Return_%'].rolling(window=20).std()

                # 3. Display Results
                st.subheader("1. Trend Analysis (Moving Averages)")
                st.markdown(f"Comparing the {ma_window1}-day and {ma_window2}-day Simple Moving Averages against the Closing Price.")
                
                # Plot Close and MAs
                chart_data = df[['Close', f'SMA_{ma_window1}', f'SMA_{ma_window2}']]
                st.line_chart(chart_data, width='stretch')

                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("2. Daily Returns Distribution")
                    st.markdown("Shows how volatile the day-to-day price swings are.")
                    st.bar_chart(df['Daily_Return_%'].tail(30), width='stretch') # Show last 30 days

                with col2:
                    st.subheader("3. 20-Day Rolling Volatility")
                    st.markdown("Measures the intensity of price fluctuations over time.")
                    st.line_chart(df['Volatility'].tail(60), width='stretch') # Show last 60 days

                st.divider()

                # Show the Transformed Data Table
                st.subheader("Transformed Dataset")
                st.markdown("Here is the underlying Pandas DataFrame with our new calculated columns added:")
                # Display the most recent data first mathematically by reversing the dataframe
                st.dataframe(df.sort_index(ascending=False).head(50))
                    
            else:
                st.error("Error fetching data. Check the symbol or try again.")
                if "Information" in data:
                    st.warning(data["Information"])
                elif "Note" in data:
                    st.warning(data["Note"])
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
