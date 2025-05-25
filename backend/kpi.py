import os
import pandas as pd
from sqlalchemy import create_engine

# ---------------------------
# F. KPI Hesaplama
# ---------------------------
class KpiCalculator:
    """
    Fact_sales tablosundan günlük KPI'ları hesaplar:
      - daily_gross_revenue_gbp (günlük brüt gelir gbp cinsinden)
      - daily_distinct_customers (günlük işlem yapan farklı müşteri sayısı)
      - pct_canceled_orders (iade edilen siparişlerin yüzdesi)
      - top 5 ürünler JSON formatında (bonus)
    """
    def __init__(self, engine):
        self.engine = engine

    def compute(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        # Tarih filtresi
        date_filter = []
        if start_date:
            date_filter.append(f"invoice_date >= '{start_date}'")
        if end_date:
            date_filter.append(f"invoice_date < '{end_date}'")
        where_clause = ' AND '.join(date_filter)
        if where_clause:
            where_clause = 'WHERE ' + where_clause

        # Ana KPI sorgusu
        kpi_query = f"""
        SELECT
          date_trunc('day', invoice_date) AS kpi_date,
          SUM(gross_line_value) AS daily_gross_revenue_gbp,
          COUNT(DISTINCT customer_id_ref) AS daily_distinct_customers,
          SUM(CASE WHEN is_cancelled THEN 1 ELSE 0 END)::float / COUNT(*) AS pct_canceled_orders
        FROM fact_sales
        {where_clause}
        GROUP BY kpi_date
        ORDER BY kpi_date;
        """
        df_kpi = pd.read_sql(kpi_query, self.engine)

        # Bonus: Top-5 ürünler günlük
        top5_query = f"""
        SELECT
          date_trunc('day', invoice_date) AS kpi_date,
          json_agg(
            json_build_object(
              'stock_code', stock_code_ref,
              'revenue', SUM(gross_line_value)
            ) ORDER BY SUM(gross_line_value) DESC
          ) FILTER (WHERE true) OVER (PARTITION BY date_trunc('day', invoice_date)) AS top5_products
        FROM fact_sales
        {where_clause}
        GROUP BY kpi_date, stock_code_ref
        ORDER BY kpi_date;
        """
        df_top5 = pd.read_sql(top5_query, self.engine)

        # Sadece ilk 5 JSON elemanı al
        df_top5 = (df_top5.groupby('kpi_date')['top5_products']
                       .first()
                       .reset_index())

        # Birleştir
        df = pd.merge(df_kpi, df_top5, on='kpi_date', how='left')
        df.rename(columns={'kpi_date': 'date'}, inplace=True)
        return df


def run_kpis(start_date: str = None, end_date: str = None, output_path: str = 'kpis/daily_metrics.csv'):
    # DB bağlantısı
    user = os.getenv('DB_USER')
    pw   = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db   = os.getenv('DB_NAME')
    url  = f"postgresql://{user}:{pw}@{host}:{port}/{db}"
    engine = create_engine(url)

    # KPI hesaplama
    calculator = KpiCalculator(engine)
    df = calculator.compute(start_date, end_date)

    # Klasörü oluştur
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # CSV olarak kaydet
    df.to_csv(output_path, index=False)
    print(f"KPI hesaplandı ve '{output_path}' konumuna yazıldı.")

if __name__ == '__main__':
    # Örnek: 2011-01-01 -> 2011-01-07 arası
    run_kpis('2011-01-01', '2011-01-08')
