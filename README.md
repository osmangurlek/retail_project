# Retail Analytics Project 🛒📊

Bu proje, perakende satış verilerini analiz etmek için geliştirilmiş kapsamlı bir **ETL (Extract, Transform, Load)** pipeline'ı ve **interaktif dashboard**'dur. Excel formatındaki online retail verilerini PostgreSQL veritabanına yükler, dönüştürür ve Streamlit ile görselleştirir.

## 📋 İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Teknoloji Stack'i](#teknoloji-stacki)
- [Mimari](#mimari)
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Modül Detayları](#modül-detayları)
- [Veri Modeli](#veri-modeli)
- [KPI'lar](#kpılar)
- [Dashboard](#dashboard)
- [Geliştirme](#geliştirme)

## 🎯 Proje Hakkında

Bu proje, online retail işletmelerin satış verilerini sistematik olarak analiz etmek için geliştirilmiştir. Proje, **nesne yönelimli programlama** prensiplerini kullanarak modüler bir yapıda inşa edilmiştir.

### Ana Hedefler:
- ✅ Excel verilerini otomatik veritabanına aktarım
- ✅ Veri kalitesi kontrolü ve validasyon  
- ✅ Star Schema ile optimize edilmiş veri modeli
- ✅ Günlük KPI hesaplamaları
- ✅ İnteraktif dashboard ile görselleştirme
- ✅ Konteynerleştirme ile kolay deployment

## 🛠 Teknoloji Stack'i

### Backend
- **Python 3.11** - Ana programlama dili
- **pandas** - Veri manipülasyonu ve analizi
- **SQLAlchemy** - ORM ve veritabanı bağlantısı
- **PostgreSQL 15** - İlişkisel veritabanı
- **psycopg2-binary** - PostgreSQL adapter
- **openpyxl** - Excel dosya okuma
- **pandera** - Veri şema validasyonu

### Frontend
- **Streamlit** - Web dashboard ve görselleştirme

### DevOps
- **Docker** - Konteynerleştirme
- **Docker Compose** - Çoklu servis orchestration

## 🏗 Mimari

```
📊 Excel Data (online_retail.xlsx)
        ↓
🔄 ETL Pipeline:
   ├── Extract (ingest.py)    → staging table
   ├── Validate (validate.py) → veri kontrolü
   ├── Transform (transform.py) → fact table
   └── Load (kpi.py)         → metrics table
        ↓
📈 Streamlit Dashboard (app.py)
```

### Veri Akışı:
1. **Excel → Staging**: Raw data PostgreSQL'e yüklenir
2. **Validation**: Veri kalitesi pandera ile kontrol edilir
3. **Transform**: Business rules uygulanır (iptal, iade, brüt gelir)
4. **KPI Computation**: Günlük metrikleri hesaplanır
5. **Visualization**: Streamlit dashboard ile gösterilir

## ✨ Özellikler

### 🔍 Veri İşleme
- **Otomatik tip dönüşümleri** (string, datetime, numeric)
- **Null değer temizleme**
- **Business logic hesaplamaları** (iptal, iade detection)
- **Veri kalitesi validasyonu**

### 📊 KPI'lar
- **Günlük Brüt Gelir** (GBP cinsinden)
- **Günlük Farklı Müşteri Sayısı**
- **İptal Edilen Sipariş Oranı** (%)
- **Top 5 Ürünler** (gelir bazında, JSON format)

### 🎨 Dashboard Özellikleri
- **Tarih bazlı filtreleme**
- **Gerçek zamanlı KPI kartları**
- **Zaman serisi grafikleri**
- **Top ürün bar chartları**
- **Responsive tasarım**

## 🚀 Kurulum

### Gereksinimler
- Docker & Docker Compose
- Git

### 1. Projeyi klonlayın
```bash
git clone <repo-url>
cd retail_project
```

### 2. Çevre değişkenlerini ayarlayın
```bash
# .env dosyası oluşturun
cp .env.example .env

# .env dosyasını düzenleyin (gerekirse)
nano .env
```

### 3. Docker Compose ile başlatın
```bash
docker-compose up --build
```

Bu komut:
- ✅ PostgreSQL veritabanını ayaklandırır (port 5432)
- ✅ Python ETL pipeline'ını çalıştırır
- ✅ Gerekli tabloları oluşturur
- ✅ Excel verilerini yükler

### 4. Dashboard'u başlatın
```bash
# Ayrı bir terminal'de
docker exec -it <etl_container_id> streamlit run backend/app.py --server.port 8501 --server.address 0.0.0.0
```

Dashboard: `http://localhost:8501`

## 📖 Kullanım

### Manuel ETL Çalıştırma

```bash
# 1. Veri yükleme
python backend/ingest.py

# 2. Veri doğrulama  
python backend/validate.py

# 3. Dönüştürme
python backend/transform.py

# 4. KPI hesaplama
python backend/kpi.py
```

### Dashboard Kullanımı

1. **Sol panel**: Başlangıç ve bitiş tarihlerini seçin
2. **Ana panel**: KPI kartları ve grafikleri görüntüleyin
3. **Otomatik yenileme**: Veriler cache ile optimize edilir

## 🧩 Modül Detayları

### 📥 ingest.py - Veri Yükleme

```python
# Soyut Source sınıfı ile genişletilebilir mimari
class Source(ABC):
    @abstractmethod
    def read(self) -> pd.DataFrame: pass

class ExcelSource(Source):
    # Excel okuma ve tip dönüşümleri
    # Null değer temizleme
```

**Özellikler:**
- ✅ OOP prensipleri (Abstract Base Class)
- ✅ Genişletilebilir kaynak türleri  
- ✅ Otomatik veri tipi düzeltmeleri
- ✅ Null değer filtreleme

### 🔄 transform.py - Veri Dönüştürme

```python
# Chain of Responsibility pattern
class Transformer(ABC):
    @abstractmethod 
    def transform(self, df: pd.DataFrame) -> pd.DataFrame: pass

# Transformer'lar:
# - CancellationTransformer: "C" ile başlayan faturalar
# - ReturnsTransformer: Negatif quantity kontrolü  
# - GrossValueTransformer: quantity * unit_price
```

**Business Rules:**
- ✅ İptal detection (`InvoiceNo` "C" ile başlıyorsa)
- ✅ İade detection (negatif `Quantity`)
- ✅ Brüt gelir hesabı (`Quantity * UnitPrice`)

### ✅ validate.py - Veri Validasyonu

```python
# Pandera şema tanımları
DataFrameSchema({
    "InvoiceNo": Column(pa.String, nullable=False),
    "Quantity": Column(pa.Int, Check.ne(0)),
    "UnitPrice": Column(pa.Float, Check.ge(0)),
    "CustomerID": Column(pa.Float, nullable=False),
    # ... diğer kontroller
})
```

**Validasyon Kuralları:**
- ✅ InvoiceNo, StockCode, Description, Country: boş olamaz
- ✅ Quantity: sıfır olamaz
- ✅ UnitPrice: negatif olamaz
- ✅ CustomerID: null olamaz

### 📊 kpi.py - KPI Hesaplamaları

```python
class KpiCalculator:
    def compute(self, start_date, end_date) -> pd.DataFrame:
        # Günlük agregasyon sorguları
        # JSON format top-5 ürün listeleri
```

**Hesaplanan Metrikler:**
- `daily_gross_revenue_gbp`: Günlük toplam gelir
- `daily_distinct_customers`: Günlük unique müşteri sayısı  
- `pct_canceled_orders`: İptal edilen sipariş oranı
- `top5_products`: En çok gelir getiren 5 ürün (JSON)

### 🎨 app.py - Streamlit Dashboard

```python
@st.cache_data
def load_kpis(start_date, end_date):
    # PostgreSQL'den KPI verilerini çek
    
# UI Bileşenleri:
# - Sidebar tarih filtreleri
# - Metric kartları  
# - Line chart (zaman serisi)
# - Bar chart (top ürünler)
```

## 🗄 Veri Modeli

### Star Schema Tasarımı

```sql
-- Dimension Tables
dim_customer (customer_key, customer_id, country)
dim_product (product_key, stock_code, description)

-- Fact Table  
fact_sales (
    invoice_no, stock_code_ref, customer_id_ref,
    invoice_date, quantity, unit_price, 
    gross_line_value, is_cancelled,
    customer_key, product_key  -- Foreign Keys
)
```

### Tablolar:

#### 📋 stg_online_retail (Staging)
Ham Excel verilerinin geçici depolandığı tablo

#### 📊 fact_sales (Fact Table)
Dönüştürülmüş satış işlemleri - Star schema'nın merkezi

#### 👥 dim_customer (Dimension)
Müşteri bilgileri (gelecekte genişletilebilir)

#### 🛍 dim_product (Dimension)  
Ürün katalogu (gelecekte genişletilebilir)

## 📈 KPI'lar

### Günlük Bazda Hesaplanan Metrikler:

1. **Daily Gross Revenue (GBP)**
   ```sql
   SUM(gross_line_value) AS daily_gross_revenue_gbp
   ```

2. **Daily Distinct Customers**
   ```sql
   COUNT(DISTINCT customer_id_ref) AS daily_distinct_customers
   ```

3. **Cancelled Orders Percentage**
   ```sql
   SUM(CASE WHEN is_cancelled THEN 1 ELSE 0 END)::float / COUNT(*) 
   AS pct_canceled_orders
   ```

4. **Top 5 Products by Revenue**
   ```sql
   json_agg(json_build_object(
     'stock_code', stock_code_ref,
     'revenue', SUM(gross_line_value)
   ) ORDER BY SUM(gross_line_value) DESC)
   ```

## 🎨 Dashboard

### Ana Özellikler:

#### 🎛 Kontrol Paneli
- **Start Date**: Analiz başlangıç tarihi
- **End Date**: Analiz bitiş tarihi  
- **Otomatik filtreleme**: Seçilen tarihe göre KPI'lar güncellenir

#### 📊 KPI Kartları
- **Total Revenue**: Seçilen dönemdeki toplam gelir
- **Distinct Customers**: Farklı müşteri sayısı
- **% Cancelled Orders**: İptal oranı

#### 📈 Grafikler
- **Line Chart**: Günlük gelir trendi
- **Bar Chart**: En popüler 5 ürün

#### 🔄 Performans
- **@st.cache_data**: Veritabanı sorgularını cache'ler
- **Lazy loading**: Sadece gerekli veriler yüklenir

## 🐳 Docker Konfigürasyonu

### docker-compose.yml
```yaml
services:
  postgres:    # PostgreSQL 15 + persistent volume
  etl:         # Python ETL pipeline
```

### Dockerfile  
```dockerfile
FROM python:3.11-slim
# Requirements yükleme
# Uygulama kopyalama
CMD ["python", "ingest.py"]  # Default: ETL başlatır
```

### Çevre Değişkenleri (.env):
```bash
# Database Configuration
DB_HOST=postgres
DB_PORT=5432  
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_secure_password

# PostgreSQL Settings
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
```

**🔒 Güvenlik**: Database kimlik bilgileri `.env` dosyasında saklanır ve `.gitignore` ile Git'ten hariç tutulur.