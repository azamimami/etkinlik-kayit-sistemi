from datetime import datetime

# ================= GLOBAL IDS =================
kitap_id_counter = 1
uye_id_counter = 1
odunc_id_counter = 1


# ================= KITAP =================
class Kitap:
    def __init__(self, ad, yazar, kategori):
        global kitap_id_counter

        self.kitap_id = kitap_id_counter
        kitap_id_counter += 1

        self.ad = ad
        self.yazar = yazar
        self.kategori = kategori
        self.durum = "Müsait"

    def kitap_durumu_degistir(self, yeni_durum):
        self.durum = yeni_durum

    def __str__(self):
        return f"[{self.kitap_id}] {self.ad} - {self.yazar} ({self.kategori}) | {self.durum}"


# ================= ÜYE =================
class Uye:
    def __init__(self, ad, email):
        global uye_id_counter

        self.uye_id = uye_id_counter
        uye_id_counter += 1

        self.ad = ad
        self.email = email
        self.gecmis = []

    def kitap_odunc_al(self, kitap, sistem):
        if kitap.durum != "Müsait":
            return "Kitap şu anda müsait değil."

        kitap.kitap_durumu_degistir("Ödünçte")

        odunc = Odunc(kitap, self)
        sistem.oduncler.append(odunc)

        self.gecmis.append(odunc)
        return odunc

    def kitap_iade_et(self, kitap, sistem):
        for o in sistem.oduncler:
            if o.kitap == kitap and o.iade_tarihi is None:
                o.iade_tarihi = datetime.now()
                kitap.kitap_durumu_degistir("Müsait")
                return "Kitap iade edildi."

        return "Ödünç kaydı bulunamadı."

    def __str__(self):
        return f"[{self.uye_id}] {self.ad} | {self.email}"


# ================= ÖDÜNÇ =================
class Odunc:
    def __init__(self, kitap, uye):
        global odunc_id_counter

        self.odunc_id = odunc_id_counter
        odunc_id_counter += 1

        self.kitap = kitap
        self.uye = uye
        self.odunc_tarihi = datetime.now()
        self.iade_tarihi = None

    def __str__(self):
        odunc = self.odunc_tarihi.strftime("%Y-%m-%d %H:%M")
        iade = self.iade_tarihi.strftime("%Y-%m-%d %H:%M") if self.iade_tarihi else "Henüz iade edilmedi"

        return f"[{self.odunc_id}] {self.kitap.ad} -> {self.uye.ad} | Ödünç: {odunc} | İade: {iade}"


# ================= SİSTEM =================
class KutuphaneSistemi:
    def __init__(self):
        self.kitaplar = []
        self.uyeler = []
        self.oduncler = []

    def kitap_ekle(self, kitap):
        self.kitaplar.append(kitap)

    def uye_ekle(self, uye):
        self.uyeler.append(uye)

    def kitap_listesi(self):
        return self.kitaplar

    def uye_listesi(self):
        return self.uyeler

    def odunc_listesi(self):
        return self.oduncler


# ================= MENU =================
def menu():
    sistem = KutuphaneSistemi()

    while True:
        print("\n===== KÜTÜPHANE SİSTEMİ =====")
        print("1- Kitap Ekle")
        print("2- Üye Ekle")
        print("3- Kitap Listele")
        print("4- Üye Listele")
        print("5- Kitap Ödünç Al")
        print("6- Kitap İade Et")
        print("7- Ödünç Listele")
        print("8- Çıkış")

        secim = input("Seçim: ")

        # ---------- KITAP ----------
        if secim == "1":
            ad = input("Kitap adı: ")
            yazar = input("Yazar: ")
            kategori = input("Kategori: ")

            k = Kitap(ad, yazar, kategori)
            sistem.kitap_ekle(k)

            print("Kitap eklendi")

        # ---------- ÜYE ----------
        elif secim == "2":
            ad = input("Ad: ")
            email = input("Email: ")

            u = Uye(ad, email)
            sistem.uye_ekle(u)

            print("Üye eklendi")

        # ---------- LIST KITAP ----------
        elif secim == "3":
            for k in sistem.kitap_listesi():
                print(k)

        # ---------- LIST UYE ----------
        elif secim == "4":
            for u in sistem.uye_listesi():
                print(u)

        # ---------- ODUNC AL ----------
        elif secim == "5":
            print("\nKitaplar:")
            for k in sistem.kitaplar:
                print(k)

            kid = int(input("Kitap ID: "))

            print("\nÜyeler:")
            for u in sistem.uyeler:
                print(u)

            uid = int(input("Üye ID: "))

            kitap = next(k for k in sistem.kitaplar if k.kitap_id == kid)
            uye = next(u for u in sistem.uyeler if u.uye_id == uid)

            sonuc = uye.kitap_odunc_al(kitap, sistem)
            print(sonuc)

        # ---------- IADE ----------
        elif secim == "6":
            aktif_oduncler = [o for o in sistem.oduncler if o.iade_tarihi is None]

            if not aktif_oduncler:
                print("İade edilecek kitap yok.")
                continue

            print("\n--- ÖDÜNÇTEKİ KİTAPLAR ---")
            for o in aktif_oduncler:
                print(f"Odunc ID: {o.odunc_id} | Kitap: {o.kitap.ad} | Üye: {o.uye.ad}")

            oid = int(input("İade edilecek Odunc ID: "))

            odunc = next((o for o in sistem.oduncler if o.odunc_id == oid), None)

            if odunc is None or odunc.iade_tarihi is not None:
                print("Geçersiz ödünç ID")
            else:
                odunc.iade_tarihi = datetime.now()
                odunc.kitap.kitap_durumu_degistir("Müsait")
                print("Kitap başarıyla iade edildi")

        # ---------- ODUNC LIST ----------
        elif secim == "7":
            oduncler = sistem.odunc_listesi()

            if len(oduncler) == 0:
                print("Henüz hiç ödünç kayıtı yok.")
            else:
                print("\n--- ÖDÜNÇ LİSTESİ ---")
                for o in oduncler:
                    print(o)

        # ---------- EXIT ----------
        elif secim == "8":
            print("Çıkış yapıldı")
            break

        else:
            print("Geçersiz seçim")


# ================= RUN =================
menu()