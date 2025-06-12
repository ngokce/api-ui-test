# 🧪 JSONPlaceholder Test Otomasyonu Projesi

Bu proje, **JSONPlaceholder** uygulamasının hem API hem de UI testlerini içeren kapsamlı bir test otomasyonu projesidir.

## 🎯 Test Edilen Uygulama
- **Uygulama**: JSONPlaceholder (https://jsonplaceholder.typicode.com/)
- **API**: JSONPlaceholder REST API
- **UI**: JSONPlaceholder Web Sitesi

## 📋 Test Kapsamı

### 🔌 API Testleri (15 Test)
- **Posts API**: CRUD operasyonları, validasyon (6 test)
- **Users API**: Kullanıcı verileri, validasyon (5 test)
- **Comments API**: Yorum işlemleri, validasyon (4 test)

### 🖥️ UI Testleri (8 Test)
- **Site Navigasyonu**: Ana sayfa, endpoint linkleri
- **JSON Response Görüntüleme**: Browser'da API yanıtları
- **Endpoint Erişilebilirliği**: API endpoint'leri
- **Format Validasyonu**: JSON yapısı kontrolü

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
```bash
pip install -r requirements.txt
```

### Testleri Çalıştırma
```bash
# Tüm testleri çalıştır
pytest tests/ -v

# Sadece API testleri
pytest tests/api/ -v

# Sadece UI testleri  
pytest tests/test_fullstack_ui.py -v
```

## 📊 Test Sonuçları
- **Toplam Test**: 23
- **API Testleri**: 15 ✅
- **UI Testleri**: 8 ✅
- **Başarı Oranı**: %100

## 📁 Proje Yapısı
```
├── tests/
│   ├── api/                    # API testleri
│   └── test_fullstack_ui.py    # UI testleri
├── utils/
│   ├── api_client.py          # API istemci
│   └── ui_helpers.py          # UI yardımcıları
├── run_tests.py               # Test çalıştırıcı
└── PROJE_RAPORU.md           # Detaylı rapor
```

## 🔧 Teknolojiler
- **Python 3.10+**
- **pytest**: Test framework
- **Selenium**: UI test otomasyonu
- **requests**: API testleri

## 📝 Raporlama
- HTML rapor: `pytest --html=report.html`
- Detaylı analiz: `PROJE_RAPORU.md` 