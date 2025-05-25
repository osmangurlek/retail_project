import pandas as pd
from abc import ABC, abstractmethod
import os
from sqlalchemy import create_engine
df1 = pd.read_excel("backend/online_retail.xlsx")
df1.info()

# ---------------------------
# 1. Soyut Sınıflar (OOP)
# ---------------------------
class Source(ABC):
    @abstractmethod
    def read(self) -> pd.DataFrame:
        """Ham veriyi okuyan method"""
        pass

# ---------------------------
# 2. Somut Kaynak: Excel
# ---------------------------
class ExcelSource(Source):
    def __init__(self, filepath: str):
        self.filepath = filepath
    
    def read(self) -> pd.DataFrame:
        # Read the Excel file
        df = pd.read_excel(self.filepath, engine="openpyxl")
        # Remove empty rows
        df = df.dropna(subset=["CustomerID"])
        # Type casts
        df["InvoiceNo"] = df["InvoiceNo"].astype(str)
        df["StockCode"] = df["StockCode"].astype(str)
        df["Description"] = df["Description"].astype(str)
        df["Quantity"] = df["Quantity"].astype(int)
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        df["UnitPrice"] = df["UnitPrice"].astype(float)
        df["CustomerID"] = df["CustomerID"].astype(float)
        df["Country"] = df["Country"].astype(str)
        
        return df
    
# ---------------------------
# 3. Hedef: Staging Yazıcı
# ---------------------------
class StagingWriter:
    def __init__(self, engine, table_name: str):
        self.engine = engine
        self.table_name = table_name
    
    def write(self, df: pd.DataFrame):
        """Veriyi SQL tablosuna yazar"""
        df.to_sql(
            name=self.table_name,
            con=self.engine,
            if_exists="append",
            index=False
        )
        
# ---------------------------
# 4. ETL Orkestrasyonu
# ---------------------------
def run_ingest():
    # Çevre değişkenlerinden DB bağlantısı
    user = os.getenv('DB_USER')
    pw   = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db   = os.getenv('DB_NAME')
    url  = f'postgresql://{user}:{pw}@{host}:{port}/{db}'
    
    engine = create_engine(url)
    
    source = ExcelSource("backend/online_retail.xlsx")
    writer = StagingWriter(engine, "stg_online_retail")
    
    df = source.read()
    writer.write(df)
    
    print(f"Ingest complete: {len(df)} rows written to staging")
    
if __name__ == "__main__":
    run_ingest()