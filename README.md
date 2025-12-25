# 🌲 Ormanın Kalbi — Büyülü Orman E-Ticaret Projesi

**Ormanın Kalbi**, büyülü orman temalı mistik eşyaların satıldığı, oyun atmosferine sahip bir **Flask tabanlı e-ticaret ve market sistemidir**.  
Proje; kullanıcı kayıt & giriş, admin paneli, ürün yönetimi, market, profil, sipariş ve destek sistemi gibi modern web uygulaması özelliklerini içerir.

---

## ✨ Tema & Atmosfer

Bu proje klasik bir e-ticaret sitesinden farklı olarak:

- 🌿 **Büyülü Orman evreninde** geçer  
- 🧙‍♂️ Elfler, ruhlar, iksirler ve kadim objeler temalıdır  
- 🎮 Oyun hissi veren bir arayüze sahiptir  
- 🌙 Fantastik, karanlık-yeşil renk paleti kullanır  

---

## 🚀 Özellikler

### 👤 Kullanıcı Sistemi
- Kayıt olma (Register)
- Giriş yapma (Login)
- Çıkış yapma (Logout)
- **Kayıt sonrası otomatik giriş**
- Kullanıcı profili
- Kullanıcıya ait para (money) sistemi

---

### 🛒 Market Sistemi
- Veritabanından ürünleri otomatik çekme
- Ürün adı, açıklama, fiyat ve görsel
- Fantastik ürün kategorileri (iksir, dekor, ritüel eşyası vb.)
- Günün öne çıkan ürünü
- Sepet altyapısı (geliştirilebilir)

---

### 🧙‍♂️ Admin Paneli
- **Sadece admin yetkisine sahip kullanıcılar görebilir**
- Ürün ekleme
- Ürün silme
- Ürün düzenleme
- Ürün görseli yükleme (upload)
- Tür (kategori) yönetimi

> Admin kontrolü `is_admin` alanı ile yapılır.

---

### 🖼 Ürün Görselleri
- Fantastik dijital çizim tarzı
- Büyülü orman temasına uygun
- PNG / JPG destekli
- Görsel yoksa otomatik placeholder

---

### 📦 Siparişler
- Kullanıcıya ait siparişleri listeleme
- Satın alınan ürünleri görme
- Sipariş geçmişi altyapısı

---

### ✉️ Destek Sistemi
- Destek formu
- Konu & mesaj alanı
- **Gmail App Password ile %100 çalışan mail gönderimi**
- Mesajlar doğrudan admin mail adresine gider

---

## 🛠 Kullanılan Teknolojiler

- **Python 3**
- **Flask**
- **SQLite**
- **SQLAlchemy**
- **HTML5**
- **CSS3**
- **Jinja2**
- **SMTP (Gmail App Password)**

---

## 🗂 Proje Klasör Yapısı
```bash
proje-main/
│

├── main.py # Ana Flask uygulaması

├── site.db # SQLite veritabanı


│
├── templates/
│       ├── index.html

│       ├── market.html

│       ├── profile.html

│       ├── login.html

│       ├── register.html

│       ├── admin.html

│       ├── orders.html

│       ├── destek.html

│       └── sss.html


│
├── static/
│       ├── css/

│         │   └── style.css

│       └── img/

│         └── ürün görselleri

│
└── README.md
```
---

## ⚙️ Kurulum

```bash
git clone https://github.com/kullanici-adi/ormanin-kalbi.git
cd ormanin-kalbi
python3 -m venv venv
source venv/bin/activate
pip install flask flask_sqlalchemy
python main.py
```
## 🔐 Admin Yetkisi

Bir kullanıcının admin olması için:
```bash
UPDATE kullanici SET is_admin = 1 WHERE email = 'admin@mail.com;
```
Admin kullanıcı:
	•	Admin panelini görür
	•	Ürünleri yönetebilir
	•	Sistemi kontrol edebilir

## 👑 Geliştirici

Mustafa Emir Kaymaz
🧙‍♂️ Ormanın Kalbi Evreninin Mimarı
Efe Başpinar
🧙‍♂️ Ormanın Kalbi Evreninin Düzenliyicisi


⸻

🌿 “Orman fısıldar… onu dinleyen kazanır.”
