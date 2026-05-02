from datetime import datetime

# ================= GLOBAL IDS =================
etkinlik_id_counter = 1
katilimci_id_counter = 1
bilet_id_counter = 1


# ================= ETKİNLİK =================
class Etkinlik:
    def __init__(self, ad, tarih, kapasite):
        global etkinlik_id_counter

        self.etkinlik_id = etkinlik_id_counter
        etkinlik_id_counter += 1

        self.ad = ad
        self.tarih = tarih
        self.kapasite = kapasite
        self.katilimcilar = []

    def katilimci_ekle(self, katilimci):
        if len(self.katilimcilar) >= self.kapasite:
            return "Etkinlik kapasitesi dolu."

        self.katilimcilar.append(katilimci)
        return "Katılımcı eklendi."

    def katilimci_sayisi(self):
        return len(self.katilimcilar)

    def __str__(self):
        return f"[{self.etkinlik_id}] {self.ad} | {self.tarih} | Kapasite: {self.kapasite} | Katılımcı: {self.katilimci_sayisi()}"


# ================= KATILIMCI =================
class Katilimci:
    def __init__(self, ad, email):
        global katilimci_id_counter

        self.katilimci_id = katilimci_id_counter
        katilimci_id_counter += 1

        self.ad = ad
        self.email = email

    def __str__(self):
        return f"[{self.katilimci_id}] {self.ad} | {self.email}"


# ================= BİLET =================
class Bilet:
    def __init__(self, etkinlik, katilimci):
        global bilet_id_counter

        self.bilet_id = bilet_id_counter
        bilet_id_counter += 1

        self.etkinlik = etkinlik
        self.katilimci = katilimci
        self.alim_tarihi = datetime.now()

    def __str__(self):
        return f"[{self.bilet_id}] {self.etkinlik.ad} -> {self.katilimci.ad} | {self.alim_tarihi.strftime('%Y-%m-%d %H:%M')}"


# ================= SİSTEM =================
class EtkinlikSistemi:
    def __init__(self):
        self.etkinlikler = []
        self.katilimcilar = []
        self.biletler = []

    def etkinlik_ekle(self, etkinlik):
        self.etkinlikler.append(etkinlik)

    def katilimci_ekle(self, katilimci):
        self.katilimcilar.append(katilimci)

    def bilet_olustur(self, etkinlik, katilimci):
        sonuc = etkinlik.katilimci_ekle(katilimci)

        if sonuc == "Etkinlik kapasitesi dolu.":
            return sonuc

        bilet = Bilet(etkinlik, katilimci)
        self.biletler.append(bilet)

        return bilet

    def rapor(self):
        print("\n--- ETKİNLİK RAPORU ---")
        for e in self.etkinlikler:
            print(f"{e.ad} -> Katılımcı Sayısı: {e.katilimci_sayisi()}")


# ================= MENU =================
def menu():
    sistem = EtkinlikSistemi()

    while True:
        print("\n===== ETKİNLİK SİSTEMİ =====")
        print("1- Etkinlik Ekle")
        print("2- Katılımcı Ekle")
        print("3- Etkinlik Listele")
        print("4- Katılımcı Listele")
        print("5- Bilet Oluştur")
        print("6- Rapor")
        print("7- Çıkış")

        secim = input("Seçim: ")

        # ---------- ETKİNLİK ----------
        if secim == "1":
            ad = input("Etkinlik adı: ")
            tarih = input("Tarih (YYYY-AA-GG): ")
            kapasite = int(input("Kapasite: "))

            e = Etkinlik(ad, tarih, kapasite)
            sistem.etkinlik_ekle(e)

            print("Etkinlik eklendi")

        # ---------- KATILIMCI ----------
        elif secim == "2":
            ad = input("Ad: ")
            email = input("Email: ")

            k = Katilimci(ad, email)
            sistem.katilimci_ekle(k)

            print("Katılımcı eklendi")

        # ---------- LIST ETKİNLİK ----------
        elif secim == "3":
            for e in sistem.etkinlikler:
                print(e)

        # ---------- LIST KATILIMCI ----------
        elif secim == "4":
            for k in sistem.katilimcilar:
                print(k)

        # ---------- BİLET ----------
        elif secim == "5":
            print("\nEtkinlikler:")
            for e in sistem.etkinlikler:
                print(e)

            eid = int(input("Etkinlik ID: "))

            print("\nKatılımcılar:")
            for k in sistem.katilimcilar:
                print(k)

            kid = int(input("Katılımcı ID: "))

            etkinlik = next(e for e in sistem.etkinlikler if e.etkinlik_id == eid)
            katilimci = next(k for k in sistem.katilimcilar if k.katilimci_id == kid)

            sonuc = sistem.bilet_olustur(etkinlik, katilimci)
            print(sonuc)

        # ---------- RAPOR ----------
        elif secim == "6":
            sistem.rapor()

        # ---------- EXIT ----------
        elif secim == "7":
            print("Çıkış yapıldı")
            break

        else:
            print("Geçersiz seçim")


# ================= RUN =================
menu()