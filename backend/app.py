import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# ---------------------------
# G. Streamlit Dashboard
# ---------------------------

def get_db_engine():
    user = os.getenv('DB_USER')
    pw   = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db   = os.getenv('DB_NAME')
    url  = f"postgresql://{user}:{pw}@{host}:{port}/{db}"
    return create_engine(url)

@st.cache_data
def load_kpis(start_date, end_date):
    engine = get_db_engine()
    query = f"SELECT * FROM daily_metrics WHERE date >= '{start_date}' AND date <= '{end_date}'"
    return pd.read_sql(query, engine, parse_dates=['date'])

@st.cache_data
def load_top_products(start_date, end_date):
    engine = get_db_engine()
    query = f"SELECT date, top5_products FROM daily_metrics WHERE date >= '{start_date}' AND date <= '{end_date}'"
    df = pd.read_sql(query, engine, parse_dates=['date'])
    # JSON dizisinden ilk 5 ürün bilgisi
    df['top5'] = df['top5_products'].apply(lambda arr: arr[:5] if isinstance(arr, list) else [])
    return df.explode('top5').dropna(subset=['top5'])

# Uygulama Başlığı
st.title("Daily Sales Dashboard")

# Yan panelde tarih seçimi
st.sidebar.header("Filter")
start_date = st.sidebar.date_input("Start date", value=pd.to_datetime('2011-01-01'))
end_date   = st.sidebar.date_input("End date",   value=pd.to_datetime('2011-01-07'))

# KPI Verilerini yükle
df_kpi = load_kpis(start_date, end_date)

# Özet Kartlar
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue GBP", f"£{df_kpi['daily_gross_revenue_gbp'].sum():,.2f}")
col2.metric("Distinct Customers", int(df_kpi['daily_distinct_customers'].sum()))
col3.metric("% Cancelled Orders", f"{(df_kpi['pct_canceled_orders'].mean()*100):.2f}%")

st.markdown("---")

# Çizgi Grafiği: Günlük Ciro
st.subheader("Daily Gross Revenue")
st.line_chart(df_kpi.set_index('date')['daily_gross_revenue_gbp'])

st.markdown("---")

# Bar Grafiği: Top-5 Ürünler
df_top = load_top_products(start_date, end_date)
st.subheader("Top 5 Products by Revenue")
# Pivot: product vs revenue sum over period
pivot = (df_top
         .assign(stock_code=lambda x: x['top5'].apply(lambda d: d['stock_code']),
                 revenue=lambda x: x['top5'].apply(lambda d: d['revenue']))
         .groupby('stock_code')['revenue']
         .sum()
         .nlargest(5))
st.bar_chart(pivot)
