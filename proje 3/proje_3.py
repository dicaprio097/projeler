from PyQt5.QtWidgets import *
import pymysql
from PyQt5.QtCore import QDate, QTime
import os
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp

# Veritabanı bağlantısı ve tablo oluşturma fonksiyonları
def veritabani_baglanti():
    return pymysql.connect(
        host='localhost',
        user='root',  # MySQL kullanıcı adınızı buraya yazın
        password='1234',  # MySQL şifrenizi buraya yazın
        database='my_database'  # Oluşturduğunuz veritabanı adını buraya yazın
    )

def tablo_olustur():
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kullanici_adi VARCHAR(255) UNIQUE,
            sifre VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hasta_bilgileri (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kullanici_adi VARCHAR(255),
            ad VARCHAR(255),
            soyad VARCHAR(255),
            tc_kimlik_no VARCHAR(255),
            telefon VARCHAR(255),
            yas INT,
            boy INT,
            kilo INT,
            kan_grubu VARCHAR(255),
            cinsiyet VARCHAR(255),
            sehir VARCHAR(255),
            ilce VARCHAR(255),
            adres TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bolumler (
            id INT AUTO_INCREMENT PRIMARY KEY,
            bolum_adi VARCHAR(255) UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doktorlar (
            id INT AUTO_INCREMENT PRIMARY KEY,
            bolum_id INT,
            doktor_adi VARCHAR(255),
            FOREIGN KEY (bolum_id) REFERENCES bolumler(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS randevu_bilgileri (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kullanici_adi VARCHAR(255),
            randevu_tarihi DATE,
            randevu_saati TIME,
            doktor_adi VARCHAR(255),
            aciklama TEXT
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

def kullanici_dogrula(kullanici_adi, sifre):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=%s AND sifre=%s", (kullanici_adi, sifre))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None

def kullanici_var_mi(kullanici_adi):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=%s", (kullanici_adi,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result is not None

def kullanici_kaydet(kullanici_adi, sifre):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (%s, %s)", (kullanici_adi, sifre))
    connection.commit()
    cursor.close()
    connection.close()

def hasta_bilgileri_kaydet(kullanici_adi, bilgiler):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO hasta_bilgileri (kullanici_adi, ad, soyad, tc_kimlik_no, telefon, yas, boy, kilo, kan_grubu, cinsiyet, sehir, ilce, adres)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (kullanici_adi, *bilgiler))
    connection.commit()
    cursor.close()
    connection.close()

def hasta_bilgileri_oku(kullanici_adi):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM hasta_bilgileri WHERE kullanici_adi=%s", (kullanici_adi,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def randevu_bilgileri_guncelle(randevu_id, randevu_tarihi, randevu_saati, bolum_adi, doktor_adi, aciklama):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE randevu_bilgileri
        SET randevu_tarihi=%s, randevu_saati=%s, bolum_adi=%s, doktor_adi=%s, aciklama=%s
        WHERE id=%s
    """, (randevu_tarihi, randevu_saati, bolum_adi, doktor_adi, aciklama, randevu_id))
    connection.commit()
    cursor.close()
    connection.close()

def bolum_ekle(bolum_adi):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO bolumler (bolum_adi) VALUES (%s)", (bolum_adi,))
    connection.commit()
    cursor.close()
    connection.close()

def doktor_ekle(bolum_adi, doktor_adi):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM bolumler WHERE bolum_adi=%s", (bolum_adi,))
    bolum_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO doktorlar (bolum_id, doktor_adi) VALUES (%s, %s)", (bolum_id, doktor_adi))
    connection.commit()
    cursor.close()
    connection.close()

def bolum_ve_doktorlari_ekle():
    connection = veritabani_baglanti()
    cursor = connection.cursor()

def kullanici_guncelle(eski_kullanici_adi, yeni_kullanici_adi, yeni_sifre):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE kullanicilar
        SET kullanici_adi=%s, sifre=%s
        WHERE kullanici_adi=%s
    """, (yeni_kullanici_adi, yeni_sifre, eski_kullanici_adi))
    connection.commit()
    cursor.close()
    connection.close()
    
    # Bölümler tablosunun boş olup olmadığını kontrol et
    cursor.execute("SELECT COUNT(*) FROM bolumler")
    count = cursor.fetchone()[0]
    
    if count == 0:
        bolumler = {
            "Kardiyoloji": ["Dr. Selim Yılmaz", "Dr. Ahmet Demir", "Dr. Zeynep Çalışkan"],
            "Nöroloji": ["Dr. Ayşe Kaya", "Dr. Hüseyin Gürkan"],
            "Ortopedi": ["Dr. Kemal Karataş", "Dr. Seda Altın", "Dr. Hakan Demirtaş", "Dr. Meryem Yılmaz"],
            "Dermatoloji": ["Dr. Zeynep Çelik", "Dr. Canan Yıldız", "Dr. Ali Koç"],
            "Genel Cerrahi": ["Dr. Fatma Demirtaş", "Dr. Ahmet Türker"],
            "Pediatri (Çocuk Sağlığı)": ["Dr. Ayşe Yıldız", "Dr. Hüsamettin Acar", "Dr. Elif Erdoğan", "Dr. İsmail Bektaş"],
            "Diş Hekimliği": ["Dr. Hakan İsmailoğlu", "Dr. Seda Karabekir", "Dr. Gülseren Yılmaz"],
            "Kadın Hastalıkları ve Doğum": ["Dr. Merve Başaran"],
            "Göz Hastalıkları (Oftalmoloji)": ["Dr. Murat Yavuz", "Dr. Zeynep Öztürk"],
            "Psikiyatri": ["Dr. İsmail Bayraktar", "Dr. Elif Can", "Dr. Murat Kaplan", "Dr. Hüseyin Çelebi"]
        }

        for bolum, doktorlar in bolumler.items():
            bolum_ekle(bolum)
            for doktor in doktorlar:
                doktor_ekle(bolum, doktor)
    
    cursor.close()
    connection.close()

def randevu_bilgileri_oku(kullanici_adi):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM randevu_bilgileri WHERE kullanici_adi=%s", (kullanici_adi,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# Veritabanı tablolarını oluştur
tablo_olustur()

class GirisPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setGeometry(850, 500, 400, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Kullanıcı Adı"))
        self.kullanici_adi = QLineEdit()
        layout.addWidget(self.kullanici_adi)

        layout.addWidget(QLabel("Şifre"))
        self.sifre = QLineEdit()
        self.sifre.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.sifre)

        self.giris_buton = QPushButton("Giriş Yap")
        self.giris_buton.clicked.connect(self.giris_yap)
        layout.addWidget(self.giris_buton)

        self.kayit_buton = QPushButton("Kayıt Ol")
        self.kayit_buton.clicked.connect(self.kayit_ol)
        layout.addWidget(self.kayit_buton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def giris_yap(self):
        kullanici_adi = self.kullanici_adi.text()
        sifre = self.sifre.text()
        if kullanici_dogrula(kullanici_adi, sifre):
            self.ana_menu_penceresi = AnaMenuPenceresi(kullanici_adi)
            self.ana_menu_penceresi.show()
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

    def kayit_ol(self):
        self.kayit_penceresi = KayitPenceresi()
        self.kayit_penceresi.show()

class KayitPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(850, 500, 400, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Kullanıcı Adı"))
        self.kullanici_adi = QLineEdit()
        layout.addWidget(self.kullanici_adi)

        layout.addWidget(QLabel("Şifre"))
        self.sifre = QLineEdit()
        self.sifre.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.sifre)

        self.kayit_buton = QPushButton("Kayıt Ol")
        self.kayit_buton.clicked.connect(self.kayit_ol)
        layout.addWidget(self.kayit_buton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def kayit_ol(self):
        kullanici_adi = self.kullanici_adi.text()
        sifre = self.sifre.text()
        if not kullanici_adi or not sifre:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre boş olamaz!")
            return

        if kullanici_var_mi(kullanici_adi):
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten kayıtlı!")
            return

        kullanici_kaydet(kullanici_adi, sifre)
        QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")
        self.close()

class RandevuAlPenceresi(QMainWindow):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.kullanici_adi = kullanici_adi
        self.setWindowTitle("Randevu Al")
        self.setGeometry(850, 500, 400, 300)

        layout = QVBoxLayout()

        self.randevu_tarihi = QDateEdit()
        self.randevu_tarihi.setCalendarPopup(True)
        self.randevu_tarihi.setMinimumDate(QDate.currentDate())  # Minimum tarih olarak bugünü ayarla
        layout.addWidget(QLabel("Randevu Tarihi"))
        layout.addWidget(self.randevu_tarihi)

        self.randevu_saati = QComboBox()
        self.randevu_saati.addItem("")  # Boş seçenek ekle
        self.randevu_saati.addItems([
            "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00"
        ])
        layout.addWidget(QLabel("Randevu Saati"))
        layout.addWidget(self.randevu_saati)

        self.bolum = QComboBox()
        self.bolum.addItem("")  # Boş seçenek ekle
        self.bolum.addItems(self.bolumleri_getir())
        self.bolum.currentIndexChanged.connect(self.doktorlari_guncelle)
        layout.addWidget(QLabel("Bölüm"))
        layout.addWidget(self.bolum)

        self.doktor_adi = QComboBox()
        self.doktor_adi.addItem("")  # Boş seçenek ekle
        layout.addWidget(QLabel("Doktor Adı"))
        layout.addWidget(self.doktor_adi)

        self.aciklama = QTextEdit()
        layout.addWidget(QLabel("Açıklama"))
        layout.addWidget(self.aciklama)

        self.kaydet_buton = QPushButton("Kaydet")
        self.kaydet_buton.clicked.connect(self.kaydet)
        layout.addWidget(self.kaydet_buton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def bolumleri_getir(self):
        connection = veritabani_baglanti()
        cursor = connection.cursor()
        cursor.execute("SELECT bolum_adi FROM bolumler")
        bolumler = [row[0] for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return bolumler

    def doktorlari_guncelle(self):
        bolum_adi = self.bolum.currentText()
        connection = veritabani_baglanti()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT doktor_adi FROM doktorlar
            JOIN bolumler ON doktorlar.bolum_id = bolumler.id
            WHERE bolumler.bolum_adi = %s
        """, (bolum_adi,))
        doktorlar = [row[0] for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        self.doktor_adi.clear()
        self.doktor_adi.addItem("")  # Boş seçenek ekle
        self.doktor_adi.addItems(doktorlar)

    def kaydet(self):
        randevu_tarihi = self.randevu_tarihi.date().toString("yyyy-MM-dd")
        randevu_saati = self.randevu_saati.currentText() + ":00"
        doktor_adi = self.doktor_adi.currentText()
        aciklama = self.aciklama.toPlainText()

        if not doktor_adi or not aciklama:
            QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalıdır!")
            return

        randevu_bilgileri_kaydet(self.kullanici_adi, randevu_tarihi, randevu_saati, doktor_adi, aciklama)
        QMessageBox.information(self, "Başarılı", "Randevu kaydedildi!")
        self.close()

def randevu_bilgileri_kaydet(kullanici_adi, randevu_tarihi, randevu_saati, doktor_adi, aciklama):
    connection = veritabani_baglanti()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO randevu_bilgileri (kullanici_adi, randevu_tarihi, randevu_saati, doktor_adi, aciklama)
        VALUES (%s, %s, %s, %s, %s)
    """, (kullanici_adi, randevu_tarihi, randevu_saati, doktor_adi, aciklama))
    connection.commit()
    cursor.close()
    connection.close()

class AnaMenuPenceresi(QMainWindow):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.kullanici_adi = kullanici_adi
        self.setWindowTitle("Ana Menü")
        self.setGeometry(850, 500, 400, 200)

        layout = QVBoxLayout()

        self.hasta_bilgileri_buton = QPushButton("Yeni Hasta Kaydı")
        self.hasta_bilgileri_buton.clicked.connect(self.hasta_bilgileri)
        layout.addWidget(self.hasta_bilgileri_buton)

        self.randevu_bilgileri_buton = QPushButton("Randevu Bilgileri")
        self.randevu_bilgileri_buton.clicked.connect(self.randevu_bilgileri)
        layout.addWidget(self.randevu_bilgileri_buton)

        self.randevu_al_buton = QPushButton("Randevu Al")
        self.randevu_al_buton.clicked.connect(self.randevu_al)
        layout.addWidget(self.randevu_al_buton)

        self.ilac_receteleri_buton = QPushButton("İlaç Reçeteleri")
        self.ilac_receteleri_buton.clicked.connect(self.ilac_receteleri)
        layout.addWidget(self.ilac_receteleri_buton)

        self.bilgilerim_buton = QPushButton("Bilgilerim")
        self.bilgilerim_buton.clicked.connect(self.bilgilerim)
        layout.addWidget(self.bilgilerim_buton)

        self.hesap_bilgileri_buton = QPushButton("Hesap Bilgilerini Düzenle")
        self.hesap_bilgileri_buton.clicked.connect(self.hesap_bilgileri)
        layout.addWidget(self.hesap_bilgileri_buton)

        self.cikis_buton = QPushButton("Çıkış")
        self.cikis_buton.clicked.connect(self.cikis)
        layout.addWidget(self.cikis_buton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def hasta_bilgileri(self):
        self.hasta_kayit_penceresi = HastaKayitPenceresi(self.kullanici_adi)
        self.hasta_kayit_penceresi.show()

    def randevu_bilgileri(self):
        self.randevu_bilgileri_penceresi = RandevuBilgileriPenceresi(self.kullanici_adi)
        self.randevu_bilgileri_penceresi.show()

    def randevu_al(self):
        self.randevu_al_penceresi = RandevuAlPenceresi(self.kullanici_adi)
        self.randevu_al_penceresi.show()

    def ilac_receteleri(self):
        self.ilac_receteleri_penceresi = IlacReceteleriPenceresi(self.kullanici_adi)
        self.ilac_receteleri_penceresi.show()

    def bilgilerim(self):
        try:
            self.bilgi_penceresi = BilgiPenceresi(self.kullanici_adi)
            self.bilgi_penceresi.show()
        except FileNotFoundError:
            QMessageBox.warning(self, "Hata", "Hasta'nın bilgileri bulunamadı!")

    def hesap_bilgileri(self):
        self.hesap_bilgileri_penceresi = HesapBilgileriPenceresi(self.kullanici_adi)
        self.hesap_bilgileri_penceresi.show()

    def cikis(self):
        self.close()

class HastaKayitPenceresi(QMainWindow):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.kullanici_adi = kullanici_adi
        self.setWindowTitle("Hasta Kayıt Formu")
        self.setGeometry(850, 500, 400, 300)

        tab_widget = QTabWidget()

        # Kimlik Bilgileri Sekmesi
        kimlik_bilgileri = QWidget()
        kimlik_layout = QVBoxLayout()
        kimlik_layout.addWidget(QLabel("Ad"))
        self.ad = QLineEdit()
        kimlik_layout.addWidget(self.ad)

        kimlik_layout.addWidget(QLabel("Soyad"))
        self.soyad = QLineEdit()
        kimlik_layout.addWidget(self.soyad)

        kimlik_layout.addWidget(QLabel("TC Kimlik No"))
        self.tc_kimlik_no = QLineEdit()
        self.tc_kimlik_no.setValidator(QRegExpValidator(QRegExp(r'\d{11}')))  # Sadece 11 haneli sayısal girişe izin ver
        kimlik_layout.addWidget(self.tc_kimlik_no)

        kimlik_layout.addWidget(QLabel("Telefon Numarası"))
        self.telefon = QLineEdit()
        kimlik_layout.addWidget(self.telefon)

        kimlik_bilgileri.setLayout(kimlik_layout)
        tab_widget.addTab(kimlik_bilgileri, "Kimlik Bilgileri")

        # Fiziksel Bilgiler Sekmesi
        fiziksel_bilgiler = QWidget()
        fiziksel_layout = QVBoxLayout()
        fiziksel_layout.addWidget(QLabel("Yaş"))
        self.yas = QLineEdit()
        fiziksel_layout.addWidget(self.yas)

        fiziksel_layout.addWidget(QLabel("Boy (cm)"))
        self.boy = QLineEdit()
        fiziksel_layout.addWidget(self.boy)

        fiziksel_layout.addWidget(QLabel("Kilo (kg)"))
        self.kilo = QLineEdit()
        fiziksel_layout.addWidget(self.kilo)

        fiziksel_layout.addWidget(QLabel("Kan Grubu"))
        self.kan_grubu = QComboBox()
        self.kan_grubu.addItems(["A+", "A-", "B+", "B-", "AB+", "AB-", "0+", "0-"])
        fiziksel_layout.addWidget(self.kan_grubu)

        fiziksel_layout.addWidget(QLabel("Cinsiyet"))
        self.cinsiyet = QComboBox()
        self.cinsiyet.addItems(["Erkek", "Kadın", "Diğer"])
        fiziksel_layout.addWidget(self.cinsiyet)

        fiziksel_bilgiler.setLayout(fiziksel_layout)
        tab_widget.addTab(fiziksel_bilgiler, "Fiziksel Bilgiler")

        # Adres Bilgileri Sekmesi
        adres_bilgileri = QWidget()
        adres_layout = QVBoxLayout()
        adres_layout.addWidget(QLabel("Şehir"))
        self.sehir = QComboBox()
        self.sehir.addItems([
            "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", 
            "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", 
            "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", 
            "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", 
            "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir", 
            "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", 
            "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", 
            "Şanlıurfa", "Şırnak", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", 
            "Zonguldak"
        ])
        self.sehir.currentIndexChanged.connect(self.sehir_degisti)
        adres_layout.addWidget(self.sehir)

        adres_layout.addWidget(QLabel("İlçe"))
        self.ilce = QLineEdit()
        adres_layout.addWidget(self.ilce)

        adres_layout.addWidget(QLabel("Açık Adres"))
        self.adres = QTextEdit()
        adres_layout.addWidget(self.adres)

        adres_bilgileri.setLayout(adres_layout)
        tab_widget.addTab(adres_bilgileri, "Adres Bilgileri")

        # Kaydet Butonu
        self.kaydet_buton = QPushButton("Kaydet")
        self.kaydet_buton.clicked.connect(self.kaydet)
        adres_layout.addWidget(self.kaydet_buton)

        self.setCentralWidget(tab_widget)

    def sehir_degisti(self):
        # Şehir değiştiğinde yapılacak işlemler
        pass

    def kaydet(self):
        ad = self.ad.text()
        soyad = self.soyad.text()
        tc_kimlik_no = self.tc_kimlik_no.text()
        telefon = self.telefon.text()
        yas = self.yas.text()
        boy = self.boy.text()
        kilo = self.kilo.text()
        kan_grubu = self.kan_grubu.currentText()
        cinsiyet = self.cinsiyet.currentText()
        sehir = self.sehir.currentText()
        ilce = self.ilce.text()
        adres = self.adres.toPlainText()

        if not ad or not soyad or not tc_kimlik_no or not telefon or not yas or not boy or not kilo or not sehir or not ilce or not adres:
            QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalıdır!")
            return

        bilgiler = [ad, soyad, tc_kimlik_no, telefon, yas, boy, kilo, kan_grubu, cinsiyet, sehir, ilce, adres]
        hasta_bilgileri_kaydet(self.kullanici_adi, bilgiler)
        QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")
        self.close()

        self.bilgileri_goster()

    def bilgileri_goster(self):
        self.bilgi_penceresi = BilgiPenceresi(self.kullanici_adi)
        self.bilgi_penceresi.show()

class RandevuBilgileriPenceresi(QMainWindow):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.kullanici_adi = kullanici_adi
        self.setWindowTitle("Randevu Bilgileri")
        self.setGeometry(850, 500, 400, 300)

        layout = QVBoxLayout()

        randevular = randevu_bilgileri_oku(self.kullanici_adi)
        if randevular:
            for randevu in randevular:
                if len(randevu) == 6:  # Randevu tuple'ının beklenen uzunlukta olup olmadığını kontrol et
                    layout.addWidget(QLabel(f"Tarih: {randevu[2]}"))
                    layout.addWidget(QLabel(f"Saati: {randevu[3]}"))
                    layout.addWidget(QLabel(f"Doktor: {randevu[4]}"))
                    layout.addWidget(QLabel(f"Açıklama: {randevu[5]}"))
                    iptal_buton = QPushButton("İptal Et")
                    iptal_buton.clicked.connect(lambda _, randevu_id=randevu[0]: self.randevu_iptal(randevu_id))
                    layout.addWidget(iptal_buton)
                    layout.addWidget(QLabel("----------"))
                else:
                    layout.addWidget(QLabel("Randevu bilgisi eksik!"))
        else:
            layout.addWidget(QLabel("Randevu bilgisi bulunamadı!"))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def randevu_iptal(self, randevu_id):
        connection = veritabani_baglanti()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM randevu_bilgileri WHERE id=%s", (randevu_id,))
        connection.commit()
        cursor.close()
        connection.close()
        QMessageBox.information(self, "Başarılı", "Randevu iptal edildi!")
        self.close()
        self.__init__(self.kullanici_adi)
        self.show()

class BilgiPenceresi(QMainWindow):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.kullanici_adi = kullanici_adi
        self.setWindowTitle("Bilgilerim")
        self.setGeometry(850, 500, 400, 300)

        layout = QVBoxLayout()

        bilgiler = hasta_bilgileri_oku(self.kullanici_adi)

        if bilgiler:
            layout.addWidget(QLabel(f"Ad: {bilgiler[2]}"))
            layout.addWidget(QLabel(f"Soyad: {bilgiler[3]}"))
            layout.addWidget(QLabel(f"TC Kimlik No: {bilgiler[4]}"))
            layout.addWidget(QLabel(f"Telefon: {bilgiler[5]}"))
            layout.addWidget(QLabel(f"Yaş: {bilgiler[6]}"))
            layout.addWidget(QLabel(f"Boy: {bilgiler[7]}"))
            layout.addWidget(QLabel(f"Kilo: {bilgiler[8]}"))
            layout.addWidget(QLabel(f"Kan Grubu: {bilgiler[9]}"))
            layout.addWidget(QLabel(f"Cinsiyet: {bilgiler[10]}"))
            layout.addWidget(QLabel(f"Şehir: {bilgiler[11]}"))
            layout.addWidget(QLabel(f"İlçe: {bilgiler[12]}"))
            layout.addWidget(QLabel(f"Açık Adres: {bilgiler[13]}"))

            self.duzenle_buton = QPushButton("Düzenle")
            self.duzenle_buton.clicked.connect(self.duzenle)
            layout.addWidget(self.duzenle_buton)
        else:
            layout.addWidget(QLabel("Hasta'nın bilgileri bulunamadı!"))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def duzenle(self):
        self.duzenle_penceresi = HastaKayitPenceresi(self.kullanici_adi)
        self.duzenle_penceresi.show()
        self.close()

class IlacReceteleriPenceresi(QMainWindow):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.kullanici_adi = kullanici_adi
        self.setWindowTitle("İlaç Reçeteleri")
        self.setGeometry(850, 500, 80, 60)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Reçeteniz BULUNMAMAKTADIR"))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

class HesapBilgileriPenceresi(QMainWindow):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.kullanici_adi = kullanici_adi
        self.setWindowTitle("Hesap Bilgileri")
        self.setGeometry(850, 500, 400, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Mevcut Kullanıcı Adı"))
        self.mevcut_kullanici_adi = QLineEdit()
        self.mevcut_kullanici_adi.setText(self.kullanici_adi)
        self.mevcut_kullanici_adi.setReadOnly(True)
        layout.addWidget(self.mevcut_kullanici_adi)

        layout.addWidget(QLabel("Mevcut Şifre"))
        self.mevcut_sifre = QLineEdit()
        self.mevcut_sifre.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.mevcut_sifre)

        layout.addWidget(QLabel("Yeni Kullanıcı Adı"))
        self.yeni_kullanici_adi = QLineEdit()
        layout.addWidget(self.yeni_kullanici_adi)

        layout.addWidget(QLabel("Yeni Şifre"))
        self.yeni_sifre = QLineEdit()
        self.yeni_sifre.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.yeni_sifre)

        self.guncelle_buton = QPushButton("Güncelle")
        self.guncelle_buton.clicked.connect(self.guncelle)
        layout.addWidget(self.guncelle_buton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def guncelle(self):
        mevcut_sifre = self.mevcut_sifre.text()
        yeni_kullanici_adi = self.yeni_kullanici_adi.text()
        yeni_sifre = self.yeni_sifre.text()

        if not mevcut_sifre or not yeni_kullanici_adi or not yeni_sifre:
            QMessageBox.warning(self, "Hata", "Tüm alanlar doldurulmalıdır!")
            return

        if not kullanici_dogrula(self.kullanici_adi, mevcut_sifre):
            QMessageBox.warning(self, "Hata", "Mevcut şifre yanlış!")
            return

        if kullanici_var_mi(yeni_kullanici_adi):
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten kayıtlı!")
            return

        kullanici_guncelle(self.kullanici_adi, yeni_kullanici_adi, yeni_sifre)
        QMessageBox.information(self, "Başarılı", "Hesap bilgileri güncellendi!")
        self.kullanici_adi = yeni_kullanici_adi
        self.close()

# Ana uygulama başlatma
if __name__ == "__main__":
    tablo_olustur()
    bolum_ve_doktorlari_ekle()
    
    app = QApplication([])
    pencere = GirisPenceresi()
    pencere.show()
    app.exec()