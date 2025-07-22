# Clan Management API

Klan yönetimi için geliştirilmiş basit bir REST API. FastAPI ve PostgreSQL kullanarak klan oluşturma, listeleme, görüntüleme ve silme işlemleri yapar. Google Cloud SQL ile entegre çalışır ve Cloud Run üzerinde deploy edilir.

## Kurulum

### Docker ile (Yerel)
```bash
docker build -t clan-api .
docker run -p 8080:8080 clan-api
```

### Cloud Run Deploy
```bash
gcloud run deploy clan-api --source . --platform managed --region us-central1
```

### Manuel kurulum
```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080
```

Google Cloud SQL PostgreSQL'de uuid extension'ı aktif etmek gerekiyor:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## API Endpoints

### Klan Oluştur
```
POST /clans
{
  "name": "Klan Adı",
  "region": "TR"
}
```

### Klanları Listele
```
GET /clans
GET /clans?sort_by=created_at&sort_order=desc
```

### Klan Detayı
```
GET /clans/{id}
```

### Klan Sil
```
DELETE /clans/{id}
```

## Veritabanı

`clans` tablosu:
- id (UUID, primary key)
- name (string, unique)
- region (string)
- created_at (timestamp)

## Proje Yapısı

```
.
├── Dockerfile
├── README.md
├── app.py                    - Ana uygulama
├── controller/
│   └── clan_controller.py    - API endpoints
├── model/
│   ├── database.py           - Veritabanı bağlantısı
│   ├── schema.py             - Pydantic modelleri
│   └── table_model.py        - SQLAlchemy tabloları
├── requirements.txt          - Python bağımlılıkları
├── schema.sql               - Veritabanı şeması
├── service/
│   └── clan_service.py      - İş mantığı
└── test.py                  - Test dosyası
```

## Özellikler

- Klan oluşturma, silme, listeleme
- UUID tabanlı ID'ler
- Sıralama seçenekleri (created_at, region)
- Hata yönetimi
- Pydantic validasyon