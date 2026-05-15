import sys
import sqlite3
import random
import string
from datetime import datetime
from contextlib import contextmanager
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLabel,
    QLineEdit, QComboBox, QMessageBox, QTabWidget, QFrame, QSpinBox,
    QDateTimeEdit, QTextEdit, QHeaderView, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ===================== VERİTABANI YÖNETİCİSİ =====================

class DatabaseManager:
    def __init__(self, db_name="etkinlik_sistemi.db"):
        self.db_name = db_name
        self.create_tables()
        self.ornek_veri_ekle()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS etkinlikler (
                    etkinlik_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ad TEXT NOT NULL,
                    kategori TEXT NOT NULL,
                    tarih TEXT NOT NULL,
                    yer TEXT,
                    kapasite INTEGER NOT NULL,
                    aciklama TEXT,
                    olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS katilimcilar (
                    katilimci_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ad TEXT NOT NULL,
                    soyad TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    telefon TEXT,
                    sehir TEXT,
                    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS biletler (
                    bilet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bilet_kodu TEXT UNIQUE NOT NULL,
                    etkinlik_id INTEGER NOT NULL,
                    katilimci_id INTEGER NOT NULL,
                    alim_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    durum TEXT DEFAULT 'Aktif',
                    FOREIGN KEY (etkinlik_id) REFERENCES etkinlikler(etkinlik_id),
                    FOREIGN KEY (katilimci_id) REFERENCES katilimcilar(katilimci_id)
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kategoriler (
                    kategori_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kategori_adi TEXT UNIQUE NOT NULL
                )
            ''')

            kategoriler = ['Konser', 'Konferans', 'Spor', 'Tiyatro', 'Sergi',
                          'Seminer', 'Festival', 'Workshop', 'Parti', 'Diğer']
            for kategori in kategoriler:
                cursor.execute('INSERT OR IGNORE INTO kategoriler (kategori_adi) VALUES (?)', (kategori,))

    def ornek_veri_ekle(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM etkinlikler')
            if cursor.fetchone()[0] > 0:
                return

            # 15 Örnek etkinlik
            ornek_etkinlikler = [
                ("Rock Müzik Festivali", "Konser", "2026-06-15 20:00", "İstanbul Beşiktaş Stadyumu", 15000, "Yerli ve yabancı rock grupları"),
                ("Caz Gecesi", "Konser", "2026-05-20 21:00", "İstanbul Caz Merkezi", 500, "Ünlü caz sanatçıları"),
                ("Teknoloji Zirvesi", "Konferans", "2026-05-25 09:00", "İstanbul Kongre Merkezi", 2000, "Yapay zeka ve gelecek teknolojiler"),
                ("Dijital Pazarlama Konferansı", "Konferans", "2026-06-10 10:00", "Wyndham Hotel İstanbul", 500, "SEO, Sosyal Medya, E-ticaret"),
                ("Maraton İstanbul", "Spor", "2026-11-07 08:00", "İstanbul", 30000, "Uluslararası İstanbul Maratonu"),
                ("Basketbol Şampiyonası", "Spor", "2026-06-01 19:00", "Sinan Erdem Spor Salonu", 12000, "Final maçı"),
                ("Hamlet", "Tiyatro", "2026-05-18 20:00", "İstanbul Şehir Tiyatrosu", 400, "Shakespeare uyarlaması"),
                ("Keşanlı Ali Destanı", "Tiyatro", "2026-06-10 19:30", "Ankara Devlet Tiyatrosu", 350, "Haldun Taner"),
                ("Modern Sanat Sergisi", "Sergi", "2026-05-10 10:00", "İstanbul Modern", 2000, "Çağdaş sanatçılar"),
                ("Fotoğraf Bienali", "Sergi", "2026-06-05 09:00", "Beyoğlu Sanat Merkezi", 1500, "Dünya fotoğrafçıları"),
                ("Girişimcilik Semineri", "Seminer", "2026-05-12 14:00", "İstanbul Teknokent", 200, "Startup kurma rehberi"),
                ("İstanbul Film Festivali", "Festival", "2026-04-15 10:00", "İstanbul", 10000, "Uluslararası film festivali"),
                ("Resim Atölyesi", "Workshop", "2026-05-05 14:00", "Sanat Akademisi", 30, "Yağlı boya kursu"),
                ("Yılbaşı Partisi", "Parti", "2026-12-31 21:00", "Hilton İstanbul", 1000, "Muhteşem yılbaşı"),
                ("Yaz Buluşması", "Diğer", "2026-07-15 14:00", "Sahil Park", 500, "Yaz etkinliği"),
            ]

            for etkinlik in ornek_etkinlikler:
                cursor.execute('''
                    INSERT INTO etkinlikler (ad, kategori, tarih, yer, kapasite, aciklama)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', etkinlik)

            # 10 Örnek katılımcı
            ornek_katilimcilar = [
                ("Ahmet", "Yılmaz", "ahmet.yilmaz@email.com", "5551234567", "İstanbul"),
                ("Ayşe", "Demir", "ayse.demir@email.com", "5552345678", "Ankara"),
                ("Mehmet", "Kaya", "mehmet.kaya@email.com", "5553456789", "İzmir"),
                ("Fatma", "Çelik", "fatma.celik@email.com", "5554567890", "Bursa"),
                ("Ali", "Öztürk", "ali.ozturk@email.com", "5555678901", "Antalya"),
                ("Zeynep", "Arslan", "zeynep.arslan@email.com", "5556789012", "Kocaeli"),
                ("Mustafa", "Doğan", "mustafa.dogan@email.com", "5557890123", "İstanbul"),
                ("Elif", "Yıldız", "elif.yildiz@email.com", "5558901234", "Ankara"),
                ("Hakan", "Şahin", "hakan.sahin@email.com", "5559012345", "İzmir"),
                ("Merve", "Aydın", "merve.aydin@email.com", "5550123456", "Bursa"),
            ]

            for katilimci in ornek_katilimcilar:
                cursor.execute('''
                    INSERT OR IGNORE INTO katilimcilar (ad, soyad, email, telefon, sehir)
                    VALUES (?, ?, ?, ?, ?)
                ''', katilimci)

    def etkinlik_ekle(self, ad, kategori, tarih, yer, kapasite, aciklama):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO etkinlikler (ad, kategori, tarih, yer, kapasite, aciklama)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ad, kategori, tarih, yer, kapasite, aciklama))
            return cursor.lastrowid

    def etkinlik_sil(self, etkinlik_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM biletler WHERE etkinlik_id = ?', (etkinlik_id,))
            cursor.execute('DELETE FROM etkinlikler WHERE etkinlik_id = ?', (etkinlik_id,))
            return True

    def etkinlikleri_getir(self, kategori=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if kategori and kategori != "Tümü":
                cursor.execute('SELECT * FROM etkinlikler WHERE kategori = ? ORDER BY tarih', (kategori,))
            else:
                cursor.execute('SELECT * FROM etkinlikler ORDER BY tarih')
            return [dict(row) for row in cursor.fetchall()]

    def katilimci_ekle(self, ad, soyad, email, telefon, sehir):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO katilimcilar (ad, soyad, email, telefon, sehir)
                VALUES (?, ?, ?, ?, ?)
            ''', (ad, soyad, email, telefon, sehir))
            return cursor.lastrowid

    def katilimci_sil(self, katilimci_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM biletler WHERE katilimci_id = ?', (katilimci_id,))
            cursor.execute('DELETE FROM katilimcilar WHERE katilimci_id = ?', (katilimci_id,))
            return True

    def katilimcilari_getir(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM katilimcilar ORDER BY kayit_tarihi DESC')
            return [dict(row) for row in cursor.fetchall()]

    def bilet_olustur(self, etkinlik_id, katilimci_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT kapasite FROM etkinlikler WHERE etkinlik_id = ?', (etkinlik_id,))
            etkinlik = cursor.fetchone()
            if not etkinlik:
                return False, "Etkinlik bulunamadı!"

            cursor.execute('SELECT COUNT(*) as sayi FROM biletler WHERE etkinlik_id = ? AND durum = "Aktif"', (etkinlik_id,))
            bilet_sayisi = cursor.fetchone()['sayi']

            if bilet_sayisi >= etkinlik['kapasite']:
                return False, "Etkinlik kapasitesi dolu!"

            bilet_kodu = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

            cursor.execute('''
                INSERT INTO biletler (bilet_kodu, etkinlik_id, katilimci_id, durum)
                VALUES (?, ?, ?, 'Aktif')
            ''', (bilet_kodu, etkinlik_id, katilimci_id))
            return True, cursor.lastrowid

    def bilet_iptal(self, bilet_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE biletler SET durum = "İptal" WHERE bilet_id = ?', (bilet_id,))
            return True

    def biletleri_getir(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT b.*, e.ad as etkinlik_adi, e.kategori as etkinlik_kategori,
                       k.ad as katilimci_ad, k.soyad as katilimci_soyad
                FROM biletler b
                JOIN etkinlikler e ON b.etkinlik_id = e.etkinlik_id
                JOIN katilimcilar k ON b.katilimci_id = k.katilimci_id
                ORDER BY b.alim_tarihi DESC
            ''')
            return [dict(row) for row in cursor.fetchall()]

    def kategorileri_getir(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT kategori_adi FROM kategoriler ORDER BY kategori_adi')
            return [row['kategori_adi'] for row in cursor.fetchall()]

    def raporlar(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as toplam_etkinlik FROM etkinlikler')
            toplam_etkinlik = cursor.fetchone()['toplam_etkinlik']

            cursor.execute('SELECT COUNT(*) as toplam_katilimci FROM katilimcilar')
            toplam_katilimci = cursor.fetchone()['toplam_katilimci']

            cursor.execute('SELECT COUNT(*) as toplam_bilet FROM biletler WHERE durum = "Aktif"')
            toplam_bilet = cursor.fetchone()['toplam_bilet']

            cursor.execute('SELECT COUNT(*) as iptal_bilet FROM biletler WHERE durum = "İptal"')
            iptal_bilet = cursor.fetchone()['iptal_bilet']

            cursor.execute('SELECT kategori, COUNT(*) as sayi FROM etkinlikler GROUP BY kategori ORDER BY sayi DESC')
            kategori_dagilimi = [dict(row) for row in cursor.fetchall()]

            return {
                "toplam_etkinlik": toplam_etkinlik,
                "toplam_katilimci": toplam_katilimci,
                "toplam_bilet": toplam_bilet,
                "iptal_bilet": iptal_bilet,
                "kategori_dagilimi": kategori_dagilimi
            }


# ===================== DİALOG PENCERELERİ =====================

class EtkinlikEkleDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("🎭 Etkinlik Ekle")
        self.setGeometry(100, 100, 500, 550)
        self.setStyleSheet("""
            QDialog { background-color: #2d2d3a; }
            QLabel { color: #e0e0e0; font-weight: bold; }
            QLineEdit, QComboBox, QSpinBox, QDateTimeEdit, QTextEdit {
                background-color: #3d3d4a;
                color: #e0e0e0;
                border: 1px solid #5d5d6a;
                border-radius: 5px;
                padding: 8px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateTimeEdit:focus {
                border: 1px solid #6B3AA0;
            }
        """)
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(QLabel("Etkinlik Adı:"), 0, 0)
        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Etkinlik adını girin")
        grid.addWidget(self.ad_input, 0, 1)

        grid.addWidget(QLabel("Kategori:"), 1, 0)
        self.kategori_combo = QComboBox()
        self.kategori_combo.addItems(self.db.kategorileri_getir())
        grid.addWidget(self.kategori_combo, 1, 1)

        grid.addWidget(QLabel("Tarih:"), 2, 0)
        self.tarih_input = QDateTimeEdit()
        self.tarih_input.setDateTime(QDateTime.currentDateTime())
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        grid.addWidget(self.tarih_input, 2, 1)

        grid.addWidget(QLabel("Yer:"), 3, 0)
        self.yer_input = QLineEdit()
        self.yer_input.setPlaceholderText("Etkinlik yeri")
        grid.addWidget(self.yer_input, 3, 1)

        grid.addWidget(QLabel("Kapasite:"), 4, 0)
        self.kapasite_input = QSpinBox()
        self.kapasite_input.setMinimum(1)
        self.kapasite_input.setMaximum(50000)
        self.kapasite_input.setValue(100)
        grid.addWidget(self.kapasite_input, 4, 1)

        grid.addWidget(QLabel("Açıklama:"), 5, 0)
        self.aciklama_input = QTextEdit()
        self.aciklama_input.setMaximumHeight(100)
        grid.addWidget(self.aciklama_input, 5, 1)

        layout.addLayout(grid)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        ekle_btn = QPushButton("✅ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)
        iptal_btn = QPushButton("❌ İptal")
        iptal_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        ad = self.ad_input.text().strip()
        kategori = self.kategori_combo.currentText()
        tarih = self.tarih_input.dateTime().toString("yyyy-MM-dd HH:mm")
        yer = self.yer_input.text().strip()
        kapasite = self.kapasite_input.value()
        aciklama = self.aciklama_input.toPlainText().strip()

        if not ad:
            QMessageBox.warning(self, "Hata", "Etkinlik adı giriniz!")
            return
        if not yer:
            QMessageBox.warning(self, "Hata", "Yer bilgisi giriniz!")
            return

        self.result = (ad, kategori, tarih, yer, kapasite, aciklama)
        self.accept()


class KatilimciEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("👤 Katılımcı Ekle")
        self.setGeometry(100, 100, 450, 450)
        self.setStyleSheet("""
            QDialog { background-color: #2d2d3a; }
            QLabel { color: #e0e0e0; font-weight: bold; }
            QLineEdit, QComboBox {
                background-color: #3d3d4a;
                color: #e0e0e0;
                border: 1px solid #5d5d6a;
                border-radius: 5px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 1px solid #6B3AA0;
            }
        """)
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(QLabel("Ad:"), 0, 0)
        self.ad_input = QLineEdit()
        self.ad_input.setPlaceholderText("Ad")
        grid.addWidget(self.ad_input, 0, 1)

        grid.addWidget(QLabel("Soyad:"), 1, 0)
        self.soyad_input = QLineEdit()
        self.soyad_input.setPlaceholderText("Soyad")
        grid.addWidget(self.soyad_input, 1, 1)

        grid.addWidget(QLabel("Email:"), 2, 0)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ornek@email.com")
        grid.addWidget(self.email_input, 2, 1)

        grid.addWidget(QLabel("Telefon:"), 3, 0)
        self.tel_input = QLineEdit()
        self.tel_input.setPlaceholderText("5XX XXX XX XX")
        grid.addWidget(self.tel_input, 3, 1)

        grid.addWidget(QLabel("Şehir:"), 4, 0)
        self.sehir_input = QLineEdit()
        self.sehir_input.setPlaceholderText("Şehir")
        grid.addWidget(self.sehir_input, 4, 1)

        layout.addLayout(grid)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        ekle_btn = QPushButton("✅ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)
        iptal_btn = QPushButton("❌ İptal")
        iptal_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        ad = self.ad_input.text().strip()
        soyad = self.soyad_input.text().strip()
        email = self.email_input.text().strip()
        telefon = self.tel_input.text().strip()
        sehir = self.sehir_input.text().strip()

        if not ad or not soyad or not email:
            QMessageBox.warning(self, "Hata", "Ad, Soyad ve Email zorunludur!")
            return

        if "@" not in email:
            QMessageBox.warning(self, "Hata", "Geçerli bir email adresi giriniz!")
            return

        self.result = (ad, soyad, email, telefon, sehir)
        self.accept()


class BiletOlusturDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("🎫 Bilet Oluştur")
        self.setGeometry(100, 100, 450, 300)
        self.setStyleSheet("""
            QDialog { background-color: #2d2d3a; }
            QLabel { color: #e0e0e0; font-weight: bold; }
            QComboBox {
                background-color: #3d3d4a;
                color: #e0e0e0;
                border: 1px solid #5d5d6a;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        grid = QGridLayout()
        grid.setSpacing(12)

        grid.addWidget(QLabel("Etkinlik:"), 0, 0)
        self.etkinlik_combo = QComboBox()
        for e in self.db.etkinlikleri_getir():
            self.etkinlik_combo.addItem(f"{e['ad']} - {e['kategori']}", e['etkinlik_id'])
        grid.addWidget(self.etkinlik_combo, 0, 1)

        grid.addWidget(QLabel("Katılımcı:"), 1, 0)
        self.katilimci_combo = QComboBox()
        for k in self.db.katilimcilari_getir():
            self.katilimci_combo.addItem(f"{k['ad']} {k['soyad']} - {k['email']}", k['katilimci_id'])
        grid.addWidget(self.katilimci_combo, 1, 1)

        layout.addLayout(grid)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        olustur_btn = QPushButton("✅ Oluştur")
        olustur_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        olustur_btn.clicked.connect(self.olustur)
        iptal_btn = QPushButton("❌ İptal")
        iptal_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(olustur_btn)
        button_layout.addWidget(iptal_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def olustur(self):
        etkinlik_id = self.etkinlik_combo.currentData()
        katilimci_id = self.katilimci_combo.currentData()

        if etkinlik_id is None or katilimci_id is None:
            QMessageBox.warning(self, "Hata", "Lütfen etkinlik ve katılımcı seçin!")
            return

        self.result = (etkinlik_id, katilimci_id)
        self.accept()


# ===================== GRAFİKLER =====================

class StatisticsWidget(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.figure = Figure(figsize=(12, 5), dpi=100, facecolor='#2d2d3a')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #2d2d3a;")
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_charts(self):
        self.figure.clear()

        raporlar = self.db.raporlar()

        # Kategori dağılımı
        ax1 = self.figure.add_subplot(121)
        ax1.set_facecolor('#3d3d4a')
        if raporlar['kategori_dagilimi']:
            kategoriler = [k['kategori'] for k in raporlar['kategori_dagilimi']]
            sayilar = [k['sayi'] for k in raporlar['kategori_dagilimi']]
            colors = ['#6B3AA0', '#2196F3', '#4CAF50', '#FF9800', '#f44336',
                      '#9C27B0', '#00BCD4', '#795548', '#E91E63', '#607D8B']
            wedges, texts, autotexts = ax1.pie(sayilar, labels=kategoriler, autopct='%1.1f%%',
                                                colors=colors[:len(kategoriler)], startangle=90)
            for text in texts:
                text.set_color('#e0e0e0')
                text.set_fontsize(9)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            ax1.set_title('📊 Kategori Dağılımı', fontsize=12, fontweight='bold', color='#e0e0e0')

        # Bilet durumu
        ax2 = self.figure.add_subplot(122)
        ax2.set_facecolor('#3d3d4a')
        aktif = raporlar['toplam_bilet']
        iptal = raporlar['iptal_bilet']
        if aktif + iptal > 0:
            labels = ['Aktif Biletler', 'İptal Biletler']
            sizes = [aktif, iptal]
            colors = ['#4CAF50', '#f44336']
            explode = (0.05, 0)
            wedges, texts, autotexts = ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
                                                 colors=colors, explode=explode, startangle=90)
            for text in texts:
                text.set_color('#e0e0e0')
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            ax2.set_title('🎫 Bilet Durumu', fontsize=12, fontweight='bold', color='#e0e0e0')
        else:
            ax2.text(0.5, 0.5, 'Henüz Bilet Yok', ha='center', va='center', fontsize=12, color='#e0e0e0')
            ax2.set_title('🎫 Bilet Durumu', fontsize=12, fontweight='bold', color='#e0e0e0')

        self.figure.tight_layout()
        self.canvas.draw()


# ===================== ANA PENCERE =====================

class EtkinlikYonetimUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.setWindowTitle("🎭 ETKİNLİK YÖNETİM SİSTEMİ")
        self.setGeometry(100, 100, 1400, 800)

        # Ana pencere stili - KOYU TEMA
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QWidget { background-color: #1a1a2e; }
            QLabel { color: #e0e0e0; }
            QTabWidget::pane { background-color: #2d2d3a; border: none; border-radius: 5px; }
            QTabBar::tab {
                background-color: #2d2d3a;
                color: #e0e0e0;
                padding: 10px 25px;
                border-radius: 5px;
                font-weight: bold;
                margin-right: 3px;
            }
            QTabBar::tab:selected {
                background-color: #6B3AA0;
                color: white;
            }
            QTableWidget {
                background-color: #2d2d3a;
                alternate-background-color: #3d3d4a;
                color: #e0e0e0;
                gridline-color: #4d4d5a;
                border: none;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #3d3d4a;
                color: #6B3AA0;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
            QPushButton {
                background-color: #3d3d4a;
                color: #e0e0e0;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4d4d5a;
            }
            QComboBox, QLineEdit, QSpinBox, QDateTimeEdit, QTextEdit {
                background-color: #3d3d4a;
                color: #e0e0e0;
                border: 1px solid #5d5d6a;
                border-radius: 5px;
                padding: 8px;
            }
            QComboBox:focus, QLineEdit:focus, QSpinBox:focus {
                border: 1px solid #6B3AA0;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #3d3d4a;
                color: #e0e0e0;
                selection-background-color: #6B3AA0;
            }
        """)

        self.init_ui()
        self.load_data()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Başlık
        header = QLabel("🎭 ETKİNLİK YÖNETİM SİSTEMİ")
        header_font = QFont("Arial", 20, QFont.Bold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #6B3AA0; padding: 15px; background-color: transparent;")

        # Dashboard Kartları
        dashboard_layout = QHBoxLayout()
        dashboard_layout.setSpacing(20)

        etkinlik_card = self.create_stat_card("🎭 Etkinlikler", "0", "#6B3AA0")
        katilimci_card = self.create_stat_card("👥 Katılımcılar", "0", "#2196F3")
        bilet_card = self.create_stat_card("🎫 Aktif Biletler", "0", "#4CAF50")
        iptal_card = self.create_stat_card("❌ İptal Biletler", "0", "#f44336")

        dashboard_layout.addWidget(etkinlik_card)
        dashboard_layout.addWidget(katilimci_card)
        dashboard_layout.addWidget(bilet_card)
        dashboard_layout.addWidget(iptal_card)

        self.etkinlik_label = etkinlik_card.findChild(QLabel, "value_label")
        self.katilimci_label = katilimci_card.findChild(QLabel, "value_label")
        self.bilet_label = bilet_card.findChild(QLabel, "value_label")
        self.iptal_label = iptal_card.findChild(QLabel, "value_label")

        # Sekmeler
        self.tabs = QTabWidget()

        # Kategori filtresi
        filter_widget = QWidget()
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Kategori Filtresi:"))
        self.kategori_filter = QComboBox()
        self.kategori_filter.addItem("Tümü")
        self.kategori_filter.addItems(self.db.kategorileri_getir())
        self.kategori_filter.currentTextChanged.connect(self.etkinlikleri_goster)
        filter_layout.addWidget(self.kategori_filter)
        filter_layout.addStretch()
        filter_widget.setLayout(filter_layout)

        # Etkinlikler sekmesi
        self.etkinlik_tab = self.create_etkinlik_tab()
        self.etkinlik_tab.layout().insertWidget(0, filter_widget)
        self.tabs.addTab(self.etkinlik_tab, "🎭 Etkinlikler")

        # Katılımcılar sekmesi
        self.katilimci_tab = self.create_katilimci_tab()
        self.tabs.addTab(self.katilimci_tab, "👥 Katılımcılar")

        # Biletler sekmesi
        self.bilet_tab = self.create_bilet_tab()
        self.tabs.addTab(self.bilet_tab, "🎫 Biletler")

        # Grafikler sekmesi
        self.stats_widget = StatisticsWidget(self.db)
        self.tabs.addTab(self.stats_widget, "📊 İstatistikler")

        main_layout.addWidget(header)
        main_layout.addLayout(dashboard_layout)
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(5000)

    def create_stat_card(self, title, value, color):
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
                min-width: 180px;
            }}
        """)
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; background-color: transparent;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 24, QFont.Bold))
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("color: white; background-color: transparent;")
        value_label.setObjectName("value_label")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)
        return card

    def create_etkinlik_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Etkinlik Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        ekle_btn.clicked.connect(self.etkinlik_ekle)

        sil_btn = QPushButton("🗑️ Seçili Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        sil_btn.clicked.connect(self.etkinlik_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        yenile_btn.clicked.connect(self.etkinlikleri_goster)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)
        button_layout.addStretch()

        self.etkinlik_table = QTableWidget()
        self.etkinlik_table.setColumnCount(7)
        self.etkinlik_table.setHorizontalHeaderLabels(["ID", "Etkinlik Adı", "Kategori", "Tarih", "Yer", "Kapasite", "Açıklama"])
        self.etkinlik_table.setAlternatingRowColors(True)
        self.etkinlik_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(button_layout)
        layout.addWidget(self.etkinlik_table)
        widget.setLayout(layout)
        return widget

    def create_katilimci_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Katılımcı Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        ekle_btn.clicked.connect(self.katilimci_ekle)

        sil_btn = QPushButton("🗑️ Seçili Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        sil_btn.clicked.connect(self.katilimci_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        yenile_btn.clicked.connect(self.katilimcilari_goster)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)
        button_layout.addStretch()

        self.katilimci_table = QTableWidget()
        self.katilimci_table.setColumnCount(6)
        self.katilimci_table.setHorizontalHeaderLabels(["ID", "Ad", "Soyad", "Email", "Telefon", "Şehir"])
        self.katilimci_table.setAlternatingRowColors(True)
        self.katilimci_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(button_layout)
        layout.addWidget(self.katilimci_table)
        widget.setLayout(layout)
        return widget

    def create_bilet_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        button_layout = QHBoxLayout()
        olustur_btn = QPushButton("➕ Bilet Oluştur")
        olustur_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        olustur_btn.clicked.connect(self.bilet_olustur)

        iptal_btn = QPushButton("❌ Bileti İptal Et")
        iptal_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        iptal_btn.clicked.connect(self.bilet_iptal)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 20px; border-radius: 5px; font-weight: bold;")
        yenile_btn.clicked.connect(self.biletleri_goster)

        button_layout.addWidget(olustur_btn)
        button_layout.addWidget(iptal_btn)
        button_layout.addWidget(yenile_btn)
        button_layout.addStretch()

        self.bilet_table = QTableWidget()
        self.bilet_table.setColumnCount(7)
        self.bilet_table.setHorizontalHeaderLabels(["ID", "Bilet Kodu", "Etkinlik", "Katılımcı", "Kategori", "Tarih", "Durum"])
        self.bilet_table.setAlternatingRowColors(True)
        self.bilet_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(button_layout)
        layout.addWidget(self.bilet_table)
        widget.setLayout(layout)
        return widget

    def load_data(self):
        self.etkinlikleri_goster()
        self.katilimcilari_goster()
        self.biletleri_goster()
        self.update_dashboard()

    def refresh_all(self):
        self.etkinlikleri_goster()
        self.katilimcilari_goster()
        self.biletleri_goster()
        self.update_dashboard()
        self.stats_widget.update_charts()

    def update_dashboard(self):
        raporlar = self.db.raporlar()
        self.etkinlik_label.setText(str(raporlar["toplam_etkinlik"]))
        self.katilimci_label.setText(str(raporlar["toplam_katilimci"]))
        self.bilet_label.setText(str(raporlar["toplam_bilet"]))
        self.iptal_label.setText(str(raporlar["iptal_bilet"]))

    def etkinlikleri_goster(self):
        kategori = self.kategori_filter.currentText()
        etkinlikler = self.db.etkinlikleri_getir(kategori if kategori != "Tümü" else None)
        self.etkinlik_table.setRowCount(0)

        for e in etkinlikler:
            row = self.etkinlik_table.rowCount()
            self.etkinlik_table.insertRow(row)
            self.etkinlik_table.setItem(row, 0, QTableWidgetItem(str(e['etkinlik_id'])))
            self.etkinlik_table.setItem(row, 1, QTableWidgetItem(e['ad']))
            self.etkinlik_table.setItem(row, 2, QTableWidgetItem(e['kategori']))
            self.etkinlik_table.setItem(row, 3, QTableWidgetItem(e['tarih']))
            self.etkinlik_table.setItem(row, 4, QTableWidgetItem(e['yer']))
            self.etkinlik_table.setItem(row, 5, QTableWidgetItem(str(e['kapasite'])))
            aciklama = (e['aciklama'][:50] + '...') if e['aciklama'] and len(e['aciklama']) > 50 else (e['aciklama'] or '')
            self.etkinlik_table.setItem(row, 6, QTableWidgetItem(aciklama))

    def etkinlik_ekle(self):
        dialog = EtkinlikEkleDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            self.db.etkinlik_ekle(*dialog.result)
            QMessageBox.information(self, "Başarılı", "✅ Etkinlik başarıyla eklendi!")
            self.etkinlikleri_goster()
            self.update_dashboard()
            self.stats_widget.update_charts()

    def etkinlik_sil(self):
        row = self.etkinlik_table.currentRow()
        if row >= 0:
            etkinlik_id = int(self.etkinlik_table.item(row, 0).text())
            etkinlik_adi = self.etkinlik_table.item(row, 1).text()

            reply = QMessageBox.question(self, "Silme Onayı",
                                        f"'{etkinlik_adi}' etkinliğini silmek istediğinize emin misiniz?\n\nBu etkinliğe ait tüm biletler de silinecektir!",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db.etkinlik_sil(etkinlik_id)
                QMessageBox.information(self, "Başarılı", "✅ Etkinlik silindi!")
                self.etkinlikleri_goster()
                self.biletleri_goster()
                self.update_dashboard()
                self.stats_widget.update_charts()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek etkinliği seçin!")

    def katilimcilari_goster(self):
        katilimcilar = self.db.katilimcilari_getir()
        self.katilimci_table.setRowCount(0)

        for k in katilimcilar:
            row = self.katilimci_table.rowCount()
            self.katilimci_table.insertRow(row)
            self.katilimci_table.setItem(row, 0, QTableWidgetItem(str(k['katilimci_id'])))
            self.katilimci_table.setItem(row, 1, QTableWidgetItem(k['ad']))
            self.katilimci_table.setItem(row, 2, QTableWidgetItem(k['soyad']))
            self.katilimci_table.setItem(row, 3, QTableWidgetItem(k['email']))
            self.katilimci_table.setItem(row, 4, QTableWidgetItem(k['telefon'] or '-'))
            self.katilimci_table.setItem(row, 5, QTableWidgetItem(k['sehir'] or '-'))

    def katilimci_ekle(self):
        dialog = KatilimciEkleDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            try:
                self.db.katilimci_ekle(*dialog.result)
                QMessageBox.information(self, "Başarılı", "✅ Katılımcı başarıyla eklendi!")
                self.katilimcilari_goster()
                self.update_dashboard()
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Hata", "Bu email adresi zaten kayıtlı!")

    def katilimci_sil(self):
        row = self.katilimci_table.currentRow()
        if row >= 0:
            katilimci_id = int(self.katilimci_table.item(row, 0).text())
            katilimci_adi = f"{self.katilimci_table.item(row, 1).text()} {self.katilimci_table.item(row, 2).text()}"

            reply = QMessageBox.question(self, "Silme Onayı",
                                        f"'{katilimci_adi}' katılımcısını silmek istediğinize emin misiniz?\n\nBu katılımcıya ait tüm biletler de silinecektir!",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db.katilimci_sil(katilimci_id)
                QMessageBox.information(self, "Başarılı", "✅ Katılımcı silindi!")
                self.katilimcilari_goster()
                self.biletleri_goster()
                self.update_dashboard()
                self.stats_widget.update_charts()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek katılımcıyı seçin!")

    def biletleri_goster(self):
        biletler = self.db.biletleri_getir()
        self.bilet_table.setRowCount(0)

        for b in biletler:
            row = self.bilet_table.rowCount()
            self.bilet_table.insertRow(row)
            self.bilet_table.setItem(row, 0, QTableWidgetItem(str(b['bilet_id'])))
            self.bilet_table.setItem(row, 1, QTableWidgetItem(b['bilet_kodu']))
            self.bilet_table.setItem(row, 2, QTableWidgetItem(b['etkinlik_adi']))
            self.bilet_table.setItem(row, 3, QTableWidgetItem(f"{b['katilimci_ad']} {b['katilimci_soyad']}"))
            self.bilet_table.setItem(row, 4, QTableWidgetItem(b['etkinlik_kategori']))
            self.bilet_table.setItem(row, 5, QTableWidgetItem(b['alim_tarihi']))

            durum_item = QTableWidgetItem(b['durum'])
            if b['durum'] == 'Aktif':
                durum_item.setBackground(QColor("#4CAF50"))
                durum_item.setForeground(QColor("white"))
            else:
                durum_item.setBackground(QColor("#f44336"))
                durum_item.setForeground(QColor("white"))
            self.bilet_table.setItem(row, 6, durum_item)

    def bilet_olustur(self):
        etkinlikler = self.db.etkinlikleri_getir()
        katilimcilar = self.db.katilimcilari_getir()

        if not etkinlikler:
            QMessageBox.warning(self, "Uyarı", "Önce etkinlik ekleyin!")
            return
        if not katilimcilar:
            QMessageBox.warning(self, "Uyarı", "Önce katılımcı ekleyin!")
            return

        dialog = BiletOlusturDialog(self.db, self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            basarili, sonuc = self.db.bilet_olustur(*dialog.result)
            if basarili:
                QMessageBox.information(self, "Başarılı", "✅ Bilet başarıyla oluşturuldu!")
            else:
                QMessageBox.warning(self, "Hata", sonuc)
            self.biletleri_goster()
            self.update_dashboard()
            self.stats_widget.update_charts()

    def bilet_iptal(self):
        row = self.bilet_table.currentRow()
        if row >= 0:
            bilet_id = int(self.bilet_table.item(row, 0).text())
            bilet_kodu = self.bilet_table.item(row, 1).text()
            durum = self.bilet_table.item(row, 6).text()

            if durum == "İptal":
                QMessageBox.warning(self, "Uyarı", "Bu bilet zaten iptal edilmiş!")
                return

            reply = QMessageBox.question(self, "İptal Onayı",
                                        f"'{bilet_kodu}' numaralı bileti iptal etmek istediğinize emin misiniz?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.db.bilet_iptal(bilet_id)
                QMessageBox.information(self, "Başarılı", "✅ Bilet iptal edildi!")
                self.biletleri_goster()
                self.update_dashboard()
                self.stats_widget.update_charts()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen iptal edilecek bileti seçin!")


# ===================== MAIN =====================

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = EtkinlikYonetimUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
