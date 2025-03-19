from PyQt5.QtWidgets import *
import os
from oyunPenceresi import TiklamaOyunuPenceresi  # TiklamaOyunuPenceresi sınıfını içe aktarın

class girisPenceresi(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Çeviri")

        # Dosya yoksa oluştur
        if not os.path.exists("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt"):
            with open("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt", "w") as file:
                file.write("")

        icerik = QVBoxLayout()
        icerik.addWidget(QLabel("Kullanıcı adı"))
        self.kullanici = QLineEdit()
        icerik.addWidget(self.kullanici)
        
        icerik.addWidget(QLabel("Şifre"))
        self.sifre = QLineEdit()
        self.sifre.setEchoMode(QLineEdit.Password)
        icerik.addWidget(self.sifre)

        self.sifremi_unuttum_buton = QPushButton("Şifremi Unuttum")
        self.sifremi_unuttum_buton.setStyleSheet("color: blue; font-size: 10px; text-align: left;")
        icerik.addWidget(self.sifremi_unuttum_buton)
        self.sifremi_unuttum_buton.clicked.connect(self.sifremi_unuttum)

        self.buton = QPushButton("Giriş yap")
        icerik.addWidget(self.buton)
        self.buton.clicked.connect(self.tiklama)

        self.kayit_buton = QPushButton("Kayıt Ol")
        icerik.addWidget(self.kayit_buton)
        self.kayit_buton.clicked.connect(self.kayit_ol)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)

    def tiklama(self):
        kullanicia = self.kullanici.text()
        sifre = self.sifre.text()
        if not kullanicia or not sifre:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre boş olamaz!")
            return

        if self.kontrol_et(kullanicia, sifre):
            print("Giriş başarılı")
            self.ana_menu = anaMenü(kullanicia)  # Kullanıcı adını ana menüye geçirin
            self.ana_menu.show()
            self.close()
        else:
            girisbasarısız = QMessageBox()
            girisbasarısız.setText("Giriş başarısız")
            girisbasarısız.setWindowTitle("Hata")
            girisbasarısız.setIcon(QMessageBox.Icon.Warning)
            girisbasarısız.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            girisbasarısız.exec()
            print("Giriş başarısız")

    def kayit_ol(self):
        self.kayit_penceresi = kayitPenceresi()
        self.kayit_penceresi.show()

    def sifremi_unuttum(self):
        self.sifre_sifirla_penceresi = SifreSifirlaPenceresi()
        self.sifre_sifirla_penceresi.show()

    def kontrol_et(self, kullanici, sifre):
        if os.path.exists("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt"):
            with open("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt", "r") as file:
                for line in file:
                    kayitli_kullanici, kayitli_sifre = line.strip().split(",")
                    if kullanici == kayitli_kullanici and sifre == kayitli_sifre:
                        return True
        return False


class kayitPenceresi(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")

        icerik = QVBoxLayout()
        icerik.addWidget(QLabel("Kullanıcı adı"))
        self.kullanici = QLineEdit()
        icerik.addWidget(self.kullanici)
        
        icerik.addWidget(QLabel("Şifre"))
        self.sifre = QLineEdit()
        self.sifre.setEchoMode(QLineEdit.Password)
        icerik.addWidget(self.sifre)

        self.buton = QPushButton("Kayıt Ol")
        icerik.addWidget(self.buton)
        self.buton.clicked.connect(self.kayit_yap)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)

    def kayit_yap(self):
        kullanici = self.kullanici.text()
        sifre = self.sifre.text()

        if not kullanici or not sifre:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre boş olamaz!")
            return

        if self.kullanici_var_mi(kullanici):
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten kayıtlı!")
            return

        with open("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt", "a") as file:
            file.write(f"{kullanici},{sifre}\n")
        QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")
        self.close()

    def kullanici_var_mi(self, kullanici):
        if os.path.exists("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt"):
            with open("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt", "r") as file:
                for line in file:
                    kayitli_kullanici, _ = line.strip().split(",")
                    if kullanici == kayitli_kullanici:
                        return True
        return False


class SifreSifirlaPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Şifre Sıfırla")

        icerik = QVBoxLayout()
        icerik.addWidget(QLabel("Kullanıcı adı"))
        self.kullanici = QLineEdit()
        icerik.addWidget(self.kullanici)
        
        icerik.addWidget(QLabel("Yeni Şifre"))
        self.yeni_sifre = QLineEdit()
        self.yeni_sifre.setEchoMode(QLineEdit.Password)
        icerik.addWidget(self.yeni_sifre)

        self.buton = QPushButton("Şifreyi Sıfırla")
        icerik.addWidget(self.buton)
        self.buton.clicked.connect(self.sifre_sifirla)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)

    def sifre_sifirla(self):
        kullanici = self.kullanici.text()
        yeni_sifre = self.yeni_sifre.text()

        if not kullanici or not yeni_sifre:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı ve yeni şifre boş olamaz!")
            return

        if os.path.exists("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt"):
            with open("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt", "r") as file:
                lines = file.readlines()

            with open("c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\kullanicilar.txt", "w") as file:
                for line in lines:
                    kayitli_kullanici, kayitli_sifre = line.strip().split(",")
                    if kayitli_kullanici == kullanici:
                        file.write(f"{kullanici},{yeni_sifre}\n")
                    else:
                        file.write(line)

            QMessageBox.information(self, "Başarılı", "Şifre başarıyla sıfırlandı!")
            self.close()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı bulunamadı!")


class anaMenü(QMainWindow):
    def __init__(self, kullanici):
        super().__init__()
        self.kullanici = kullanici
        self.setWindowTitle("Ana Ekran")
        
        icerik = QVBoxLayout()
        baslik = QLabel("PROGRAM ANA EKRANI")
        baslik.setStyleSheet("font-size: 40px; color: red;")
        icerik.addWidget(baslik)

        self.buton1 = QPushButton("Proje -1")
        self.buton2 = QPushButton("Proje -2")
        self.buton3 = QPushButton("Proje -3")
        self.buton4 = QPushButton("Proje -4")
        self.buton5 = QPushButton("Oyunlar")
        self.buton5.clicked.connect(self.oyunlar)
        self.buton1.clicked.connect(self.goster_proje_mesaj)
        self.buton2.clicked.connect(self.goster_proje_mesaj)
        self.buton3.clicked.connect(self.goster_proje_mesaj)
        self.buton4.clicked.connect(self.goster_proje_mesaj)
        self.label = QLabel("...")

        icerik.addWidget(self.buton1)
        icerik.addWidget(self.buton2)   
        icerik.addWidget(self.buton3)
        icerik.addWidget(self.buton4)
        icerik.addWidget(self.buton5)
        icerik.addWidget(self.label)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)

    def oyunlar(self):
        self.oyun_penceresi = oyunPenceresi(self.kullanici)
        self.oyun_penceresi.show()

    def goster_mesaj(self):
        self.mesaj_penceresi = mesajPenceresi()
        self.mesaj_penceresi.show()

    def goster_proje_mesaj(self):
        self.proje_mesaj_penceresi = projeMesajPenceresi()
        self.proje_mesaj_penceresi.show()

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")


class oyunPenceresi(QMainWindow):
    def __init__(self, kullanici):
        super().__init__()
        self.kullanici = kullanici
        self.setWindowTitle("Oyunlar")

        icerik = QVBoxLayout()
        baslik = QLabel("Oyunlar")
        baslik.setStyleSheet("font-size: 30px; color: blue;")
        icerik.addWidget(baslik)

        self.buton1 = QPushButton("Tiklama Oyunu")
        self.buton2 = QPushButton("Oyun -2")
        self.buton3 = QPushButton("Oyun -3")
        self.label = QLabel("Oyun seçin")

        icerik.addWidget(self.buton1)
        icerik.addWidget(self.buton2)
        icerik.addWidget(self.buton3)
        icerik.addWidget(self.label)

        self.buton1.clicked.connect(self.tiklama_oyunu)
        self.buton2.clicked.connect(self.goster_mesaj)
        self.buton3.clicked.connect(self.goster_mesaj)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)

    def tiklama_oyunu(self):
        self.tiklama_penceresi = TiklamaOyunuPenceresi(self.kullanici)
        self.tiklama_penceresi.show()

    def goster_mesaj(self):
        self.mesaj_penceresi = mesajPenceresi()
        self.mesaj_penceresi.show()


class mesajPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Oyunlar")

        icerik = QVBoxLayout()
        mesaj = QLabel("En güzel oyunlar, en yakın zamanda, BURADA SİZLERLE...")
        mesaj.setStyleSheet("font-size: 30px; color: green;")
        icerik.addWidget(mesaj)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)


class projeMesajPenceresi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proje")

        icerik = QVBoxLayout()
        mesaj = QLabel("Ooops :) görünüşe göre bu sayfa şuanda kullanılamıyor...")
        mesaj.setStyleSheet("font-size: 30px; color: red;")
        icerik.addWidget(mesaj)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)


uygulama = QApplication([])

pencere = girisPenceresi()
pencere.show()

uygulama.exec()