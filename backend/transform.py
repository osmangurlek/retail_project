import os
import pandas as pd
from abc import ABC, abstractmethod
from sqlalchemy import create_engine

# ---------------------------
# 1. Transformer Soyut Sınıfı
# ---------------------------
class Transformer(ABC):
    @abstractmethod
    def transfrom(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the DataFrame and return the new DataFrame"""
        pass
    
# ---------------------------
# 2. Somut Transformer: Online Retail
# ---------------------------
class CancellationTransformer(Transformer): # Cancellation flags
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df["is_cancelled"] = df["InvoiceNo"].str.startswith("C")
        return df
    
class ReturnsTransformer(Transformer): # Negative quantity point to return
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df["is_return"] = df["Quantity"] < 0
        return df
    
class GrossValueTransformer(Transformer): # gross value by row
    def transformer(self, df: pd.DataFrame) -> pd.DataFrame:
        df["gross_line_value"] = df["Quantity"] * df["UnitPrice"]
        return df
    

# ---------------------------
# 3. ETL Orkestrasyonu
# ---------------------------
def run_transform():
    # DB connection info
    user = os.getenv('DB_USER')
    pw   = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db   = os.getenv('DB_NAME')
    
    url  = f'postgresql://{user}:{pw}@{host}:{port}/{db}'
    
    # DB connection
    engine = create_engine(url)
    
    with engine.connect() as conn:
        # Read the staging data
        df = pd.read_sql("SELECT * FROM stg_online_retail", conn)
        
        # Apply transformations
        transformers = [
            CancellationTransformer(),
            ReturnsTransformer(),
            GrossValueTransformer()
        ]
        
        for transformer in transformers:
            df = transformer.transform(df)
            
        # Write to fact table
        df.to_sql('fact_sales', conn, if_exists='replace', index=False)
    
    print(f"Transform complete: {len(df)} rows written to fact_sales")
    
if __name__ == "__main__":
    run_transform()
    
    