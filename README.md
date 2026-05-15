# 🎭 ETKİNLİK YÖNETİM SİSTEMİ

Profesyonel ve kullanıcı dostu bir Etkinlik Yönetim Sistemi. PyQt5 ve Matplotlib kullanarak modern bir arayüz sunmaktadır. SQLite veritabanı desteğine sahiptir.


# 🎯 Özellikler

# 📊 Dashboard
- **🎪 Toplam Etkinlik Sayısı** - Kayıtlı etkinlik sayısı
- **👥 Toplam Katılımcı Sayısı** - Sistemdeki katılımcı sayısı
- **🎫 Toplam Aktif Bilet** - Geçerli bilet sayısı
- **❌ İptal Bilet Sayısı** - İptal edilen bilet sayısı
- Gerçek zamanlı güncelleme (5 saniyede bir)

<img width="1440" height="900" alt="Screenshot 2026-05-15 at 20 08 14" src="https://github.com/user-attachments/assets/5e5821c0-bce5-4f6d-8e02-fac5064eb2c8" />

# 🎪 Etkinlik Yönetimi
- ➕ **Etkinlik Ekle** - Ad, Kategori, Tarih, Yer, Kapasite ile etkinlik oluşturma
- 🗑️ **Etkinlik Sil** - Seçili etkinliği silme (biletleri de silinir)
- 🔍 **Kategori Filtreleme** - Kategoriye göre etkinlik listeleme
- 📋 **Detaylı Liste** - Tüm etkinlik bilgilerini görüntüleme
- 🔄 **Yenile** - Etkinlik listesini güncelleme

# 👥 Katılımcı Yönetimi
- ➕ **Katılımcı Ekle** - Ad, Soyad, Email, Telefon, Şehir ile kayıt
- ✅ **Email Doğrulama** - Benzersiz email kontrolü
- 🗑️ **Katılımcı Sil** - Katılımcı kaydını silme (biletleri de silinir)
- 📋 **Detaylı Liste** - Tüm katılımcı bilgileri
- 🔄 **Yenile** - Katılımcı listesini güncelleme

<img width="1440" height="900" alt="Screenshot 2026-05-15 at 20 08 21" src="https://github.com/user-attachments/assets/80aa5437-6281-4c8f-9edc-7bd62c8a8a5e" />



# 🎫 Bilet Yönetimi
- ➕ **Bilet Oluştur** - Etkinlik ve katılımcı seçerek bilet oluşturma
- 🔢 **Benzersiz Bilet Kodu** - 10 haneli otomatik kod üretimi
- ✅ **Kapasite Kontrolü** - Etkinlik kapasitesi dolduğunda uyarı
- ❌ **Bilet İptal** - Aktif bileti iptal etme
- 🎨 **Durum Göstergesi** - Aktif (Yeşil) / İptal (Kırmızı)
- 🔄 **Yenile** - Bilet listesini güncelleme

<img width="1440" height="900" alt="Screenshot 2026-05-15 at 20 08 30" src="https://github.com/user-attachments/assets/0df44dc2-b891-4790-877c-6dbf8cc92f90" />



# 📊 Grafikler & İstatistikler
- 🥧 **Pasta Grafik** - Kategori bazlı etkinlik dağılımı
- 🥧 **Pasta Grafik** - Aktif/İptal bilet durumu
- 🎨 **Koyu Tema** - Profesyonel ve modern görünüm
- 📈 **Otomatik Güncelleme** - Veri değişikliklerinde yenileme

<img width="1440" height="900" alt="Statistik" src="https://github.com/user-attachments/assets/a98a7838-5d84-495f-8ebb-41add5fcce77" />



# 💾 Veritabanı
- 🗄️ **SQLite** - Hafif ve hızlı veritabanı
- 💾 **Kalıcı Veri** - Uygulama kapansa bile veriler kaybolmaz
- 📁 **Tek Dosya** - `etkinlik_sistemi.db` dosyasında saklanır


# 🖥️ Teknolojiler

| Teknoloji | Kullanım Alanı |
|-----------|----------------|
| Python 3.9+ | Ana programlama dili |
| PyQt5 | GUI Framework (Modern arayüz) |
| SQLite3 | Veritabanı yönetimi |
| Matplotlib | Grafik ve görselleştirme |


