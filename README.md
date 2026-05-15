# 🎭 ETKİNLİK YÖNETİM SİSTEMİ

Profesyonel ve kullanıcı dostu bir Etkinlik Yönetim Sistemi. PyQt5 ve Matplotlib kullanarak modern bir arayüz sunmaktadır. SQLite veritabanı desteğine sahiptir.


# 🎯 Özellikler

# 📊 Dashboard
- **🎪 Toplam Etkinlik Sayısı** - Kayıtlı etkinlik sayısı
- **👥 Toplam Katılımcı Sayısı** - Sistemdeki katılımcı sayısı
- **🎫 Toplam Aktif Bilet** - Geçerli bilet sayısı
- **❌ İptal Bilet Sayısı** - İptal edilen bilet sayısı
- Gerçek zamanlı güncelleme (5 saniyede bir)

<img width="1440" height="900" alt="Screenshot 2026-05-15 at 20 38 02" src="https://github.com/user-attachments/assets/0835638b-f5bf-407c-a0c5-003bd745afe4" />

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

<img width="1440" height="900" alt="Screenshot 2026-05-15 at 20 38 22" src="https://github.com/user-attachments/assets/4625e1ab-9a8f-418f-b043-276ae50077b1" />




# 🎫 Bilet Yönetimi
- ➕ **Bilet Oluştur** - Etkinlik ve katılımcı seçerek bilet oluşturma
- 🔢 **Benzersiz Bilet Kodu** - 10 haneli otomatik kod üretimi
- ✅ **Kapasite Kontrolü** - Etkinlik kapasitesi dolduğunda uyarı
- ❌ **Bilet İptal** - Aktif bileti iptal etme
- 🎨 **Durum Göstergesi** - Aktif (Yeşil) / İptal (Kırmızı)
- 🔄 **Yenile** - Bilet listesini güncelleme


<img width="1440" height="900" alt="Screenshot 2026-05-15 at 20 38 37" src="https://github.com/user-attachments/assets/749261a2-c7a3-4e26-8a36-5d4dd2c670af" />




# 📊 Grafikler & İstatistikler
- 🥧 **Pasta Grafik** - Kategori bazlı etkinlik dağılımı
- 🥧 **Pasta Grafik** - Aktif/İptal bilet durumu
- 🎨 **Koyu Tema** - Profesyonel ve modern görünüm
- 📈 **Otomatik Güncelleme** - Veri değişikliklerinde yenileme
<img width="1440" height="900" alt="Screenshot 2026-05-15 at 20 38 46" src="https://github.com/user-attachments/assets/c7e7ab40-3467-4b7e-a9f0-d9c71a1f5b1d" />





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


