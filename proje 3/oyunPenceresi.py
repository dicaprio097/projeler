from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
import os

class TiklamaOyunuPenceresi(QMainWindow):
    def __init__(self, kullanici):
        super().__init__()
        self.kullanici = kullanici
        self.setWindowTitle("Tıklama Oyunu")

        self.puan = 0
        self.level = 1
        self.puan_per_click = 1
        self.auto_click_enabled = False
        self.auto_click_puan = 0
        self.auto_click_cost = 100
        self.auto_click_upgrade_cost = 100
        self.next_level_puan = 20  # İlk seviyeyi atlamak için gereken puan

        self.load_user_data()

        icerik = QVBoxLayout()
        baslik = QLabel("Tıklama Oyunu")
        baslik.setStyleSheet("font-size: 30px; color: blue;")
        icerik.addWidget(baslik)

        self.puan_label = QLabel(f"Puan: {self.puan}")
        self.puan_label.setAlignment(Qt.AlignCenter)
        self.puan_label.setStyleSheet("font-size: 20px;")
        icerik.addWidget(self.puan_label)

        self.level_label = QLabel(f"Level: {self.level}")
        self.level_label.setAlignment(Qt.AlignCenter)
        self.level_label.setStyleSheet("font-size: 20px;")
        icerik.addWidget(self.level_label)

        self.tikla_buton = QPushButton("Tıkla!")
        self.tikla_buton.setStyleSheet("font-size: 20px;")
        self.tikla_buton.clicked.connect(self.puan_arttir)
        icerik.addWidget(self.tikla_buton)

        self.level_up_buton = QPushButton(f"Level Atla ({self.next_level_puan} puan)")
        self.level_up_buton.setStyleSheet("font-size: 20px;")
        self.level_up_buton.clicked.connect(self.level_atla)
        icerik.addWidget(self.level_up_buton)

        self.auto_click_buton = QPushButton(f"Otomatik Tıklama ({self.auto_click_cost} puan)")
        self.auto_click_buton.setStyleSheet("font-size: 20px;")
        self.auto_click_buton.clicked.connect(self.oto_tiklama_al)
        icerik.addWidget(self.auto_click_buton)

        self.auto_click_upgrade_buton = QPushButton(f"Otomatik Tıklama Yükselt ({self.auto_click_upgrade_cost} puan)")
        self.auto_click_upgrade_buton.setStyleSheet("font-size: 20px;")
        self.auto_click_upgrade_buton.clicked.connect(self.oto_tiklama_yukselt)
        icerik.addWidget(self.auto_click_upgrade_buton)

        araclar = QWidget()
        araclar.setLayout(icerik)
        self.setCentralWidget(araclar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_click)

    def puan_arttir(self):
        self.puan += self.puan_per_click
        self.puan_label.setText(f"Puan: {self.puan}")
        self.save_user_data()

    def level_atla(self):
        if self.puan >= self.next_level_puan:
            self.puan -= self.next_level_puan
            self.level += 1
            self.level_label.setText(f"Level: {self.level}")
            self.update_puan_per_click()
            self.next_level_puan *= 2  # Her seviyede gereken puanı iki katına çıkar
            self.level_up_buton.setText(f"Level Atla ({self.next_level_puan} puan)")
            self.puan_label.setText(f"Puan: {self.puan}")
            self.save_user_data()

            if self.level == 100:
                QMessageBox.information(self, "Tebrikler", "Tebrikler çok iyi gidiyorsunuz!")
                self.puan += 100000
                self.puan_label.setText(f"Puan: {self.puan}")
        else:
            QMessageBox.warning(self, "Hata", "Paranız yeterli değil")

    def update_puan_per_click(self):
        self.puan_per_click = self.level

    def oto_tiklama_al(self):
        if self.level < 10:
            QMessageBox.warning(self, "Hata", "İlk başta 10.level e ulaşmalısın")
            return

        if self.puan >= self.auto_click_cost:
            self.puan -= self.auto_click_cost
            self.auto_click_buton.setText("Otomatik Tıklama SATIN ALINDI")
            self.auto_click_buton.setEnabled(False)
            self.auto_click_enabled = True
            self.timer.start(1000)  # 1 saniyede bir otomatik tıklama
            self.puan_label.setText(f"Puan: {self.puan}")
            self.save_user_data()
        else:
            QMessageBox.warning(self, "Hata", "Paranız yeterli değil")

    def oto_tiklama_yukselt(self):
        if self.level < 10:
            QMessageBox.warning(self, "Hata", "İlk başta 10.level e ulaşmalısın")
            return

        if self.puan >= self.auto_click_upgrade_cost:
            self.puan -= self.auto_click_upgrade_cost
            if self.auto_click_upgrade_cost < 3200:  # İlk 5 aşama için 2 katına çıkar
                self.auto_click_upgrade_cost *= 2
            else:  # Sonraki aşamalar için 4 katına çıkar
                self.auto_click_upgrade_cost *= 4
            self.auto_click_puan += 1
            self.puan_label.setText(f"Puan: {self.puan}")
            self.auto_click_upgrade_buton.setText(f"Otomatik Tıklama Yükselt ({self.auto_click_upgrade_cost} puan)")
            self.save_user_data()
        else:
            QMessageBox.warning(self, "Hata", "Paranız yeterli değil")

    def auto_click(self):
        self.puan += self.auto_click_puan
        self.puan_label.setText(f"Puan: {self.puan}")
        self.save_user_data()

    def load_user_data(self):
        if os.path.exists(f"c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\{self.kullanici}_data.txt"):
            with open(f"c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\{self.kullanici}_data.txt", "r") as file:
                data = file.read().split(",")
                self.puan = int(data[0])
                self.level = int(data[1])
                self.puan_per_click = int(data[2])
                self.auto_click_enabled = data[3] == "True"
                self.auto_click_puan = int(data[4])
                self.auto_click_cost = int(data[5])
                self.auto_click_upgrade_cost = int(data[6])
                self.next_level_puan = int(data[7])

    def save_user_data(self):
        with open(f"c:\\Users\\me097\\OneDrive\\Desktop\\project 3\\projeler\\{self.kullanici}_data.txt", "w") as file:
            file.write(f"{self.puan},{self.level},{self.puan_per_click},{self.auto_click_enabled},{self.auto_click_puan},{self.auto_click_cost},{self.auto_click_upgrade_cost},{self.next_level_puan}")


if __name__ == "__main__":
    uygulama = QApplication([])

    pencere = TiklamaOyunuPenceresi("test_user")
    pencere.show()

    uygulama.exec()