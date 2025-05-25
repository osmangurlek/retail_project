import os
import pandas as pd
from sqlalchemy import create_engine
import pandera as pa
from pandera import Column, DataFrameSchema, Check

# ---------------------------
# Veri Doğrulama
# ---------------------------

class StagingValidator:
    """
    Staging tablosundaki verinin temel kalitesini kontrol eder.
    Kurallar:
      1. InvoiceNo, StockCode, Description ve Country boş olamaz.
      2. Quantity != 0
      3. UnitPrice >= 0
      4. CustomerID null olamaz
    """
    def __init__(self, engine):
        self.engine = engine
        # fetch the staging data from the database
        self.df = pd.read_sql("SELECT * FROM stg_online_retail", engine)
        
    def validate(self):
        # Definition the pandera schema
        schema = DataFrameSchema({
            "InvoiceNo": Column(pa.String, nullable=False),
            "StockCode": Column(pa.String, nullable=False),
            "Description": Column(pa.String, nullable=False),
            "Quantity": Column(pa.Int, Check.ne(0), nullable=False),
            "InvoiceDate": Column(pa.DateTime, nullable=False),
            "UnitPrice": Column(pa.Float, Check.ge(0), nullable=False),
            "CustomerID": Column(pa.Float, Check(lambda s: s.notnull()), nullable=False),
            "Country": Column(pa.String, nullable=False)
        }, coerce=True)
        
        result = schema.validate(self.df, lazy=True)
        print(f"Validation passed: {len(self.df)} rows checked.")
        return result

def run_validation():
    # Çevre değişkenlerinden DB bağlantısı
    user = os.getenv('DB_USER')
    pw   = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db   = os.getenv('DB_NAME')
    url  = f'postgresql://{user}:{pw}@{host}:{port}/{db}'
    
    engine = create_engine(url)
    
    validator = StagingValidator(engine)
    validator.validate()
    
if __name__ == "__main__":
    run_validation()