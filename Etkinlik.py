import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QDialog, QLabel,
    QLineEdit, QComboBox, QMessageBox, QTabWidget, QFrame, QSpinBox,
    QDateTimeEdit, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ===================== ETKİNLİK SİSTEMİ =====================

class Etkinlik:
    """Etkinlik sınıfı - Etkinlik bilgilerini ve katılımcılarını yönetir"""
    _id_counter = 1

    def __init__(self, ad, tarih, kapasite):
        self.etkinlik_id = Etkinlik._id_counter
        Etkinlik._id_counter += 1
        self.ad = ad
        self.tarih = tarih
        self.kapasite = kapasite
        self.katilimcilar = []
        self.yaratilma_tarihi = datetime.now()

    def katilimci_ekle(self, katilimci):
        """Etkinliğe katılımcı ekler"""
        if len(self.katilimcilar) >= self.kapasite:
            return False, "Etkinlik kapasitesi dolu"

        if any(k.katilimci_id == katilimci.katilimci_id for k in self.katilimcilar):
            return False, "Bu katılımcı zaten eklendi"

        self.katilimcilar.append(katilimci)
        return True, "Katılımcı eklendi"

    def katilimci_cikar(self, katilimci_id):
        """Etkinlikten katılımcı çıkarır"""
        for k in self.katilimcilar:
            if k.katilimci_id == katilimci_id:
                self.katilimcilar.remove(k)
                return True
        return False

    def katilimci_sayisi(self):
        """Etkinlikteki katılımcı sayısını döndürür"""
        return len(self.katilimcilar)

    def bos_kapasite(self):
        """Kalan kapasiteyi döndürür"""
        return self.kapasite - len(self.katilimcilar)

    def __str__(self):
        return f"[{self.etkinlik_id}] {self.ad} | {self.tarih} | Kapasite: {self.kapasite} | Katılımcı: {self.katilimci_sayisi()}/{self.kapasite}"


class Katilimci:
    """Katılımcı sınıfı"""
    _id_counter = 1

    def __init__(self, ad, email):
        self.katilimci_id = Katilimci._id_counter
        Katilimci._id_counter += 1
        self.ad = ad
        self.email = email
        self.kayit_tarihi = datetime.now()

    def __str__(self):
        return f"[{self.katilimci_id}] {self.ad} | {self.email}"


class Bilet:
    """Bilet sınıfı - Katılımcı ve etkinlik arasında bağlantı"""
    _id_counter = 1

    def __init__(self, etkinlik, katilimci):
        self.bilet_id = Bilet._id_counter
        Bilet._id_counter += 1
        self.etkinlik = etkinlik
        self.katilimci = katilimci
        self.alim_tarihi = datetime.now()
        self.durumu = "Aktif"

    def iptal_et(self):
        """Bileti iptal eder"""
        self.durumu = "İptal"

    def __str__(self):
        return f"[{self.bilet_id}] {self.etkinlik.ad} → {self.katilimci.ad} | {self.alim_tarihi.strftime('%Y-%m-%d %H:%M')} | {self.durumu}"


class EtkinlikSistemi:
    """Etkinlik yönetim sistemi"""

    def __init__(self):
        self.etkinlikler = []
        self.katilimcilar = []
        self.biletler = []

    def etkinlik_ekle(self, ad, tarih, kapasite):
        """Yeni etkinlik ekler"""
        if kapasite <= 0:
            return False, "Kapasite pozitif olmalıdır"
        etkinlik = Etkinlik(ad, tarih, kapasite)
        self.etkinlikler.append(etkinlik)
        return True, etkinlik

    def etkinlik_sil(self, etkinlik_id):
        """Etkinlik siler"""
        for e in self.etkinlikler:
            if e.etkinlik_id == etkinlik_id:
                # İlgili biletleri sil
                self.biletler = [b for b in self.biletler if b.etkinlik.etkinlik_id != etkinlik_id]
                self.etkinlikler.remove(e)
                return True, "Etkinlik silindi"
        return False, "Etkinlik bulunamadı"

    def etkinlik_bul(self, etkinlik_id):
        """Etkinlik bulur"""
        for e in self.etkinlikler:
            if e.etkinlik_id == etkinlik_id:
                return e
        return None

    def katilimci_ekle(self, ad, email):
        """Yeni katılımcı ekler"""
        if not ad or not email:
            return False, "Ad ve Email boş olamaz"
        if "@" not in email:
            return False, "Geçerli bir email girin"

        katilimci = Katilimci(ad, email)
        self.katilimcilar.append(katilimci)
        return True, katilimci

    def katilimci_sil(self, katilimci_id):
        """Katılımcı siler"""
        for k in self.katilimcilar:
            if k.katilimci_id == katilimci_id:
                # İlgili biletleri sil
                for e in self.etkinlikler:
                    e.katilimci_cikar(katilimci_id)
                self.biletler = [b for b in self.biletler if b.katilimci.katilimci_id != katilimci_id]
                self.katilimcilar.remove(k)
                return True, "Katılımcı silindi"
        return False, "Katılımcı bulunamadı"

    def katilimci_bul(self, katilimci_id):
        """Katılımcı bulur"""
        for k in self.katilimcilar:
            if k.katilimci_id == katilimci_id:
                return k
        return None

    def bilet_olustur(self, etkinlik_id, katilimci_id):
        """Bilet oluşturur"""
        etkinlik = self.etkinlik_bul(etkinlik_id)
        katilimci = self.katilimci_bul(katilimci_id)

        if not etkinlik:
            return False, "Etkinlik bulunamadı"
        if not katilimci:
            return False, "Katılımcı bulunamadı"

        basarili, mesaj = etkinlik.katilimci_ekle(katilimci)
        if not basarili:
            return False, mesaj

        bilet = Bilet(etkinlik, katilimci)
        self.biletler.append(bilet)
        return True, bilet

    def bilet_iptal(self, bilet_id):
        """Bileti iptal eder"""
        for b in self.biletler:
            if b.bilet_id == bilet_id and b.durumu == "Aktif":
                b.iptal_et()
                b.etkinlik.katilimci_cikar(b.katilimci.katilimci_id)
                return True, "Bilet iptal edildi"
        return False, "Bilet bulunamadı veya zaten iptal edilmiş"

    def raporlar(self):
        """Sistem raporları oluşturur"""
        toplam_etkinlik = len(self.etkinlikler)
        toplam_katilimci = len(self.katilimcilar)
        toplam_bilet = len([b for b in self.biletler if b.durumu == "Aktif"])
        iptal_bilet = len([b for b in self.biletler if b.durumu == "İptal"])

        return {
            "toplam_etkinlik": toplam_etkinlik,
            "toplam_katilimci": toplam_katilimci,
            "toplam_bilet": toplam_bilet,
            "iptal_bilet": iptal_bilet,
            "etkinlik_detaylari": [(e.ad, e.katilimci_sayisi(), e.kapasite) for e in self.etkinlikler]
        }


# ===================== DIALOG PENCERELERİ =====================

class EtkinlikEkleDialog(QDialog):
    """Etkinlik ekleme dialogu"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Etkinlik Ekle")
        self.setGeometry(100, 100, 450, 350)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ad
        ad_label = QLabel("Etkinlik Adı:")
        ad_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.ad_input = QLineEdit()
        self.ad_input.setStyleSheet("padding: 8px; border: 2px solid #ccc; border-radius: 4px;")
        self.ad_input.setPlaceholderText("Örn: Yazılım Konferansı")

        # Tarih
        tarih_label = QLabel("Tarih:")
        tarih_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.tarih_input = QLineEdit()
        self.tarih_input.setStyleSheet("padding: 8px; border: 2px solid #ccc; border-radius: 4px;")
        self.tarih_input.setPlaceholderText("Örn: 2026-05-20 14:00")

        # Kapasite
        kapasite_label = QLabel("Kapasite:")
        kapasite_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.kapasite_input = QSpinBox()
        self.kapasite_input.setMinimum(1)
        self.kapasite_input.setMaximum(10000)
        self.kapasite_input.setValue(100)
        self.kapasite_input.setStyleSheet("padding: 8px; border: 2px solid #ccc; border-radius: 4px;")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(ad_label)
        layout.addWidget(self.ad_input)
        layout.addWidget(tarih_label)
        layout.addWidget(self.tarih_input)
        layout.addWidget(kapasite_label)
        layout.addWidget(self.kapasite_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        ad = self.ad_input.text().strip()
        tarih = self.tarih_input.text().strip()
        kapasite = self.kapasite_input.value()

        if not ad or not tarih:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")
            return

        self.result = (ad, tarih, kapasite)
        self.accept()


class KatilimciEkleDialog(QDialog):
    """Katılımcı ekleme dialogu"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Katılımcı Ekle")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Ad
        ad_label = QLabel("Ad Soyad:")
        ad_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.ad_input = QLineEdit()
        self.ad_input.setStyleSheet("padding: 8px; border: 2px solid #ccc; border-radius: 4px;")
        self.ad_input.setPlaceholderText("Örn: Ahmet Yılmaz")

        # Email
        email_label = QLabel("Email:")
        email_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("padding: 8px; border: 2px solid #ccc; border-radius: 4px;")
        self.email_input.setPlaceholderText("Örn: ahmet@email.com")

        # Butonlar
        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("✓ Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.ekle)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(ad_label)
        layout.addWidget(self.ad_input)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def ekle(self):
        ad = self.ad_input.text().strip()
        email = self.email_input.text().strip()

        if not ad or not email:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")
            return

        if "@" not in email:
            QMessageBox.warning(self, "Hata", "Geçerli bir email girin!")
            return

        self.result = (ad, email)
        self.accept()


class BiletOlusturDialog(QDialog):
    """Bilet oluşturma dialogu"""

    def __init__(self, sistem, parent=None):
        super().__init__(parent)
        self.sistem = sistem
        self.setWindowTitle("Bilet Oluştur")
        self.setGeometry(100, 100, 450, 350)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.result = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Etkinlik seçimi
        etkinlik_label = QLabel("Etkinlik:")
        etkinlik_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.etkinlik_combo = QComboBox()
        self.etkinlik_combo.setStyleSheet("padding: 8px; border: 2px solid #ccc; border-radius: 4px;")

        if self.sistem.etkinlikler:
            for e in self.sistem.etkinlikler:
                self.etkinlik_combo.addItem(f"{e.ad} ({e.bos_kapasite()}/{e.kapasite})", e.etkinlik_id)
        else:
            self.etkinlik_combo.addItem("Etkinlik yok", None)
            self.etkinlik_combo.setEnabled(False)

        # Katılımcı seçimi
        katilimci_label = QLabel("Katılımcı:")
        katilimci_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.katilimci_combo = QComboBox()
        self.katilimci_combo.setStyleSheet("padding: 8px; border: 2px solid #ccc; border-radius: 4px;")

        if self.sistem.katilimcilar:
            for k in self.sistem.katilimcilar:
                self.katilimci_combo.addItem(f"{k.ad} ({k.email})", k.katilimci_id)
        else:
            self.katilimci_combo.addItem("Katılımcı yok", None)
            self.katilimci_combo.setEnabled(False)

        # Butonlar
        button_layout = QHBoxLayout()
        olustur_btn = QPushButton("✓ Oluştur")
        olustur_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        olustur_btn.clicked.connect(self.olustur)

        iptal_btn = QPushButton("✕ İptal")
        iptal_btn.setStyleSheet("background-color: #9E9E9E; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.reject)

        button_layout.addWidget(olustur_btn)
        button_layout.addWidget(iptal_btn)

        layout.addWidget(etkinlik_label)
        layout.addWidget(self.etkinlik_combo)
        layout.addWidget(katilimci_label)
        layout.addWidget(self.katilimci_combo)
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


# ===================== GRAFIKLER =====================

class StatisticsWidget(QWidget):
    """İstatistik grafikleri widget"""

    def __init__(self, sistem, parent=None):
        super().__init__(parent)
        self.sistem = sistem
        self.figure = Figure(figsize=(12, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_charts(self):
        """Grafikleri günceller"""
        self.figure.clear()

        # Etkinlik kapasitesi kullanım
        ax1 = self.figure.add_subplot(121)
        if self.sistem.etkinlikler:
            etkinlik_adlari = [e.ad[:15] + "..." if len(e.ad) > 15 else e.ad for e in self.sistem.etkinlikler]
            katilimci_sayilari = [e.katilimci_sayisi() for e in self.sistem.etkinlikler]
            bos_kapasiteler = [e.bos_kapasite() for e in self.sistem.etkinlikler]

            x = range(len(etkinlik_adlari))
            ax1.bar([i - 0.2 for i in x], katilimci_sayilari, width=0.4, label="Katılımcı", color="#4CAF50")
            ax1.bar([i + 0.2 for i in x], bos_kapasiteler, width=0.4, label="Boş Kapasite", color="#FF9800")
            ax1.set_xlabel("Etkinlikler", fontsize=10, fontweight="bold")
            ax1.set_ylabel("Sayı", fontsize=10, fontweight="bold")
            ax1.set_title("📊 Etkinlik Kapasitesi Kullanımı", fontsize=12, fontweight="bold")
            ax1.set_xticks(x)
            ax1.set_xticklabels(etkinlik_adlari, rotation=45, ha="right")
            ax1.legend()
            ax1.grid(axis="y", alpha=0.3)
        else:
            ax1.text(0.5, 0.5, "Etkinlik Yok", ha="center", va="center", fontsize=14)

        # Bilet istatistikleri
        ax2 = self.figure.add_subplot(122)
        aktif_bilet = len([b for b in self.sistem.biletler if b.durumu == "Aktif"])
        iptal_bilet = len([b for b in self.sistem.biletler if b.durumu == "İptal"])

        labels = ["Aktif", "İptal"]
        sizes = [aktif_bilet, iptal_bilet]
        colors = ["#4CAF50", "#f44336"]
        explode = (0.1, 0)

        if sum(sizes) > 0:
            ax2.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, explode=explode, startangle=90)
            ax2.set_title("🎫 Bilet Durumu", fontsize=12, fontweight="bold")
        else:
            ax2.text(0.5, 0.5, "Bilet Yok", ha="center", va="center", fontsize=14)

        self.canvas.draw()


# ===================== ANA PENCERE =====================

class EtkinlikYonetimUI(QMainWindow):
    """Ana uygulama penceresi"""

    def __init__(self):
        super().__init__()
        self.sistem = EtkinlikSistemi()
        self.setWindowTitle("🎭 ETKİNLİK YÖNETİM SİSTEMİ")
        self.setGeometry(0, 0, 1500, 850)
        self.setStyleSheet("background-color: #ffffff;")
        self.init_ui()

    def init_ui(self):
        """Arayüzü başlatır"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Başlık
        header = QLabel("🎭 ETKİNLİK YÖNETİM SİSTEMİ")
        header_font = QFont()
        header_font.setPointSize(22)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #6B3AA0; padding: 20px;")

        # Dashboard
        dashboard_layout = QHBoxLayout()
        etkinlik_card = self.create_stat_card("🎭 Etkinlikler", "0", "#6B3AA0")
        katilimci_card = self.create_stat_card("👥 Katılımcılar", "0", "#2196F3")
        bilet_card = self.create_stat_card("🎫 Biletler", "0", "#4CAF50")
        iptal_card = self.create_stat_card("❌ İptal Edilen", "0", "#f44336")

        dashboard_layout.addWidget(etkinlik_card)
        dashboard_layout.addWidget(katilimci_card)
        dashboard_layout.addWidget(bilet_card)
        dashboard_layout.addWidget(iptal_card)

        self.etkinlik_label = etkinlik_card.findChild(QLabel, "value_label")
        self.katilimci_label = katilimci_card.findChild(QLabel, "value_label")
        self.bilet_label = bilet_card.findChild(QLabel, "value_label")
        self.iptal_label = iptal_card.findChild(QLabel, "value_label")

        # Sekme penceresi
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #6B3AA0;
                color: white;
            }
        """)

        # Etkinlikler sekmesi
        self.etkinlik_tab = self.create_etkinlik_tab()
        self.tabs.addTab(self.etkinlik_tab, "🎭 Etkinlikler")

        # Katılımcılar sekmesi
        self.katilimci_tab = self.create_katilimci_tab()
        self.tabs.addTab(self.katilimci_tab, "👥 Katılımcılar")

        # Biletler sekmesi
        self.bilet_tab = self.create_bilet_tab()
        self.tabs.addTab(self.bilet_tab, "🎫 Biletler")

        # Grafikler sekmesi
        self.stats_widget = StatisticsWidget(self.sistem)
        self.tabs.addTab(self.stats_widget, "📊 Grafikler")

        main_layout.addWidget(header)
        main_layout.addLayout(dashboard_layout)
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start(500)

    def create_stat_card(self, title, value, color):
        """İstatistik kartı oluşturur"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 20px;
                color: white;
            }}
        """)

        layout = QVBoxLayout()
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setObjectName("value_label")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        card.setLayout(layout)

        return card

    def create_etkinlik_tab(self):
        """Etkinlik sekmesini oluşturur"""
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Etkinlik Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.etkinlik_ekle)

        sil_btn = QPushButton("🗑️ Seçili Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        sil_btn.clicked.connect(self.etkinlik_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.etkinlikleri_goster)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)

        self.etkinlik_table = QTableWidget()
        self.etkinlik_table.setColumnCount(5)
        self.etkinlik_table.setHorizontalHeaderLabels(["ID", "Ad", "Tarih", "Kapasitesi", "Katılımcı/Kapasite"])
        self.etkinlik_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.etkinlik_table)
        widget.setLayout(layout)

        return widget

    def create_katilimci_tab(self):
        """Katılımcı sekmesini oluşturur"""
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        ekle_btn = QPushButton("➕ Katılımcı Ekle")
        ekle_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        ekle_btn.clicked.connect(self.katilimci_ekle)

        sil_btn = QPushButton("🗑️ Seçili Sil")
        sil_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        sil_btn.clicked.connect(self.katilimci_sil)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.katilimcilari_goster)

        button_layout.addWidget(ekle_btn)
        button_layout.addWidget(sil_btn)
        button_layout.addWidget(yenile_btn)

        self.katilimci_table = QTableWidget()
        self.katilimci_table.setColumnCount(4)
        self.katilimci_table.setHorizontalHeaderLabels(["ID", "Ad", "Email", "Kayıt Tarihi"])
        self.katilimci_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.katilimci_table)
        widget.setLayout(layout)

        return widget

    def create_bilet_tab(self):
        """Bilet sekmesini oluşturur"""
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        olustur_btn = QPushButton("➕ Bilet Oluştur")
        olustur_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        olustur_btn.clicked.connect(self.bilet_olustur)

        iptal_btn = QPushButton("❌ Bileti İptal Et")
        iptal_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        iptal_btn.clicked.connect(self.bilet_iptal)

        yenile_btn = QPushButton("🔄 Yenile")
        yenile_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        yenile_btn.clicked.connect(self.biletleri_goster)

        button_layout.addWidget(olustur_btn)
        button_layout.addWidget(iptal_btn)
        button_layout.addWidget(yenile_btn)

        self.bilet_table = QTableWidget()
        self.bilet_table.setColumnCount(5)
        self.bilet_table.setHorizontalHeaderLabels(["ID", "Etkinlik", "Katılımcı", "Alım Tarihi", "Durum"])
        self.bilet_table.setStyleSheet("border: 1px solid #ccc; border-radius: 4px;")

        layout.addLayout(button_layout)
        layout.addWidget(self.bilet_table)
        widget.setLayout(layout)

        return widget

    # ===================== ETKINLIK METODLARı =====================

    def etkinlik_ekle(self):
        """Yeni etkinlik ekler"""
        dialog = EtkinlikEkleDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            ad, tarih, kapasite = dialog.result
            basarili, etkinlik = self.sistem.etkinlik_ekle(ad, tarih, kapasite)
            if basarili:
                QMessageBox.information(self, "Başarılı", "Etkinlik eklendi!")
                self.etkinlikleri_goster()
            else:
                QMessageBox.warning(self, "Hata", etkinlik)

    def etkinlik_sil(self):
        """Seçili etkinliği siler"""
        row = self.etkinlik_table.currentRow()
        if row >= 0:
            try:
                etkinlik_id = int(self.etkinlik_table.item(row, 0).text())
                reply = QMessageBox.question(self, "Onay", f"Etkinlik silinsin mi?\n\n⚠️ Tüm biletler de silinecek!",
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    basarili, mesaj = self.sistem.etkinlik_sil(etkinlik_id)
                    if basarili:
                        QMessageBox.information(self, "Başarılı", mesaj)
                        self.etkinlikleri_goster()
                    else:
                        QMessageBox.warning(self, "Hata", mesaj)
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Bir hata oluştu: {str(e)}")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir etkinlik seçin!")

    def etkinlikleri_goster(self):
        """Etkinlikleri tabloda gösterir"""
        self.etkinlik_table.setRowCount(0)
        for e in self.sistem.etkinlikler:
            row = self.etkinlik_table.rowCount()
            self.etkinlik_table.insertRow(row)
            self.etkinlik_table.setItem(row, 0, QTableWidgetItem(str(e.etkinlik_id)))
            self.etkinlik_table.setItem(row, 1, QTableWidgetItem(e.ad))
            self.etkinlik_table.setItem(row, 2, QTableWidgetItem(e.tarih))
            self.etkinlik_table.setItem(row, 3, QTableWidgetItem(str(e.kapasite)))
            self.etkinlik_table.setItem(row, 4, QTableWidgetItem(f"{e.katilimci_sayisi()}/{e.kapasite}"))

    # ===================== KATILIMCI METODLARı =====================

    def katilimci_ekle(self):
        """Yeni katılımcı ekler"""
        dialog = KatilimciEkleDialog(self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            ad, email = dialog.result
            basarili, katilimci = self.sistem.katilimci_ekle(ad, email)
            if basarili:
                QMessageBox.information(self, "Başarılı", "Katılımcı eklendi!")
                self.katilimcilari_goster()
            else:
                QMessageBox.warning(self, "Hata", katilimci)

    def katilimci_sil(self):
        """Seçili katılımcıyı siler"""
        row = self.katilimci_table.currentRow()
        if row >= 0:
            try:
                katilimci_id = int(self.katilimci_table.item(row, 0).text())
                reply = QMessageBox.question(self, "Onay", f"Katılımcı silinsin mi?\n\n⚠️ Tüm biletleri de silinecek!",
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    basarili, mesaj = self.sistem.katilimci_sil(katilimci_id)
                    if basarili:
                        QMessageBox.information(self, "Başarılı", mesaj)
                        self.katilimcilari_goster()
                    else:
                        QMessageBox.warning(self, "Hata", mesaj)
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Bir hata oluştu: {str(e)}")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir katılımcı seçin!")

    def katilimcilari_goster(self):
        """Katılımcıları tabloda gösterir"""
        self.katilimci_table.setRowCount(0)
        for k in self.sistem.katilimcilar:
            row = self.katilimci_table.rowCount()
            self.katilimci_table.insertRow(row)
            self.katilimci_table.setItem(row, 0, QTableWidgetItem(str(k.katilimci_id)))
            self.katilimci_table.setItem(row, 1, QTableWidgetItem(k.ad))
            self.katilimci_table.setItem(row, 2, QTableWidgetItem(k.email))
            self.katilimci_table.setItem(row, 3, QTableWidgetItem(k.kayit_tarihi.strftime('%Y-%m-%d %H:%M')))

    # ===================== BİLET METODLARı =====================

    def bilet_olustur(self):
        """Yeni bilet oluşturur"""
        if not self.sistem.etkinlikler or not self.sistem.katilimcilar:
            QMessageBox.warning(self, "Hata", "Etkinlik ve katılımcı ekleyin!")
            return

        dialog = BiletOlusturDialog(self.sistem, self)
        if dialog.exec_() == QDialog.Accepted and dialog.result:
            etkinlik_id, katilimci_id = dialog.result
            try:
                basarili, sonuc = self.sistem.bilet_olustur(etkinlik_id, katilimci_id)
                if basarili:
                    QMessageBox.information(self, "Başarılı", f"Bilet #{sonuc.bilet_id} oluşturuldu!")
                    self.biletleri_goster()
                else:
                    QMessageBox.warning(self, "Hata", sonuc)
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Bir hata oluştu: {str(e)}")

    def bilet_iptal(self):
        """Seçili bileti iptal eder"""
        row = self.bilet_table.currentRow()
        if row >= 0:
            try:
                bilet_id = int(self.bilet_table.item(row, 0).text())
                reply = QMessageBox.question(self, "Onay", "Bilet iptal edilsin mi?",
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    basarili, mesaj = self.sistem.bilet_iptal(bilet_id)
                    if basarili:
                        QMessageBox.information(self, "Başarılı", mesaj)
                        self.biletleri_goster()
                    else:
                        QMessageBox.warning(self, "Hata", mesaj)
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Bir hata oluştu: {str(e)}")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir bilet seçin!")

    def biletleri_goster(self):
        """Biletleri tabloda gösterir"""
        self.bilet_table.setRowCount(0)
        for b in self.sistem.biletler:
            row = self.bilet_table.rowCount()
            self.bilet_table.insertRow(row)
            self.bilet_table.setItem(row, 0, QTableWidgetItem(str(b.bilet_id)))
            self.bilet_table.setItem(row, 1, QTableWidgetItem(b.etkinlik.ad))
            self.bilet_table.setItem(row, 2, QTableWidgetItem(b.katilimci.ad))
            self.bilet_table.setItem(row, 3, QTableWidgetItem(b.alim_tarihi.strftime('%Y-%m-%d %H:%M')))

            durumu_label = QTableWidgetItem(b.durumu)
            if b.durumu == "İptal":
                durumu_label.setBackground(QColor("#f44336"))
                durumu_label.setForeground(QColor("white"))
            else:
                durumu_label.setBackground(QColor("#4CAF50"))
                durumu_label.setForeground(QColor("white"))

            self.bilet_table.setItem(row, 4, durumu_label)

    # ===================== REFRESH =====================

    def refresh_all(self):
        """Tüm verileri günceller"""
        raporlar = self.sistem.raporlar()
        self.etkinlik_label.setText(str(raporlar["toplam_etkinlik"]))
        self.katilimci_label.setText(str(raporlar["toplam_katilimci"]))
        self.bilet_label.setText(str(raporlar["toplam_bilet"]))
        self.iptal_label.setText(str(raporlar["iptal_bilet"]))
        self.stats_widget.update_charts()


# ===================== MAIN =====================

def main():
    app = QApplication(sys.argv)
    window = EtkinlikYonetimUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
