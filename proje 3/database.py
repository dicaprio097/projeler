import pymysql

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