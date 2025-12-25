from flask import Flask , render_template , request , flash , redirect , url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column , Integer , ForeignKey
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
## form.get kullan
 
##https://stackoverflow.com/questions/20503183/python-flask-working-with-wraps incele
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']  = "skgdgdhgjkhfdjkghkdjfhgkjdhg"

# Mail ayarları
MAIL_SENDER = "mustafaemirkaymaz@gmail.com"
MAIL_PASSWORD = "medk njav jyvi gmbj"
MAIL_RECEIVER = "mustafaemirkaymaz@gmail.com"

db = SQLAlchemy(app)


#databasa in oluşturması
class Kullanici(db.Model):
    __tablename__ = "kullanici"

    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    sifre = db.Column(db.String(255), nullable=False)
    money = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)


class Durum(db.Model):
    __tablename__ = "durum"

    id = db.Column(db.Integer, primary_key=True)
    durum = db.Column(db.String(40), nullable=False)


class UrunTurleri(db.Model):
    __tablename__ = "urun_turleri"

    id = db.Column(db.Integer, primary_key=True)
    tur = db.Column(db.String(50), unique=True, nullable=False)


class Urunler(db.Model):
    __tablename__ = "urunler"

    id = db.Column(db.Integer, primary_key=True)
    urun_adi = db.Column(db.String(100), nullable=False)

    tur_id = db.Column(
        db.Integer,
        db.ForeignKey("urun_turleri.id"),
        nullable=False
    )

    fiyat = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(255))
    aciklama = db.Column(db.String(255))


class Siparis(db.Model):
    __tablename__ = "siparis"

    id = db.Column(db.Integer, primary_key=True)

    kullanici_id = db.Column(
        db.Integer,
        db.ForeignKey("kullanici.id"),
        nullable=False
    )

    durum_id = db.Column(
        db.Integer,
        db.ForeignKey("durum.id"),
        nullable=False
    )

    tutar = db.Column(db.Integer, nullable=False)

# SiparisDetay modeli EKLENDİ
class SiparisDetay(db.Model):
    __tablename__ = "siparis_detay"

    id = db.Column(db.Integer, primary_key=True)
    siparis_id = db.Column(db.Integer, db.ForeignKey("siparis.id"), nullable=False)
    urun_id = db.Column(db.Integer, db.ForeignKey("urunler.id"), nullable=False)
    miktar = db.Column(db.Integer, default=1)

    urun = db.relationship("Urunler")
    
@app.route("/")
def index():

    urunler = db.session.query(
        Urunler.id,
        Urunler.urun_adi,
        Urunler.fiyat,
        Urunler.img,
        Urunler.aciklama,
        UrunTurleri.tur
    ).join(UrunTurleri, Urunler.tur_id == UrunTurleri.id).all()

    return render_template("index.html", urunler=urunler)



@app.route("/x" , methods = ["GET" , "POST"])
def durum_ekle():
    if request.method == "GET": 
        return render_template("a.html")
    else:
        x = request.form.get("durum")
        print(x)
        rafa = Durum(durum = x)
        db.session.add(rafa)
        db.session.commit()
        return render_template("a.html")
    
#kayıt kısmı fronta uyarla
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        kullanici_adi = request.form.get("ad")
        kullanici_mail = request.form.get("email")
        sifre = request.form.get("sifre")

        hashed_sifre = generate_password_hash(
            sifre, method="pbkdf2:sha256"
        )

        yeni_kullanici = Kullanici(
            kullanici_adi=kullanici_adi,
            email=kullanici_mail,
            sifre=hashed_sifre,
            money=0
        )

        try:
            # 1️⃣ DB'ye ekle
            db.session.add(yeni_kullanici)
            db.session.commit()   # <-- ID BURADA OLUŞUR

            # 2️⃣ Artık id VAR
            session["user_id"] = yeni_kullanici.id
            session["username"] = yeni_kullanici.kullanici_adi
            session["is_admin"] = yeni_kullanici.is_admin

            flash("Hoş geldin! Hesabın oluşturuldu", "success")
            return redirect(url_for("index"))

        except IntegrityError:
            db.session.rollback()
            flash("Bu kullanıcı adı veya e-posta zaten kayıtlı.", "danger")

        except Exception as e:
            db.session.rollback()
            print(e)
            flash("Bir hata oluştu", "danger")

    return render_template("register.html")


    return render_template("register.html") 

@app.route("/login" , methods = ["GET" , "POST"])
def login():
    if request.method == "POST":
        kullanici_email = request.form["email"]
        kullanici_sifre = request.form["sifre"]
        kullanici = Kullanici.query.filter(
            (Kullanici.email == kullanici_email)
        ).first()
        
        if kullanici:
            if check_password_hash(kullanici.sifre , kullanici_sifre):
                session["user_id"] = kullanici.id
                session["username"] = kullanici.kullanici_adi
                session["is_admin"] = kullanici.is_admin
                flash(f"Hoş geldiniz, {kullanici.kullanici_adi}! Giriş başarılı.", "success")
                return redirect(url_for("index"))
            
            else:
                flash("hatalı giriş." , "danger")
                return render_template("login.html")
                
        else:
            flash("kullanıcı adı veya e-posta bulunamadı" , "danger")
            return render_template("login.html")
        
    return render_template("login.html")

@app.route("/market")
def market():
    urunler = db.session.query(
        Urunler.id,
        Urunler.urun_adi,
        Urunler.fiyat,
        Urunler.img,
        Urunler.aciklama,
        UrunTurleri.tur
    ).join(UrunTurleri, Urunler.tur_id == UrunTurleri.id).all()

    return render_template("market.html", urunler=urunler)

@app.route("/siparis")
def siparis():
    # Giriş kontrolü
    if "user_id" not in session:
        flash("Önce giriş yapmalısınız.", "danger")
        return redirect(url_for("login"))

    # Kullanıcıyı DB'den al
    kullanici = Kullanici.query.get(session["user_id"])

    # Kullanıcı DB'de yoksa (None hatasını BURADA kesiyoruz)
    if kullanici is None:
        flash("Kullanıcı bulunamadı. Lütfen tekrar giriş yapın.", "danger")
        session.clear()
        return redirect(url_for("login"))

    # Beklemedeki siparişi al
    siparis = Siparis.query.filter_by(
        kullanici_id=kullanici.id,
        durum_id=1
    ).first()

    # Sipariş detayı
    if siparis:
        siparis_detay = SiparisDetay.query.filter_by(
            siparis_id=siparis.id
        ).all()
    else:
        siparis_detay = []

    return render_template(
        "siparis.html",
        siparis=siparis,
        siparis_detay=siparis_detay
    )

@app.route("/sıkça_sorulan_sorular")
def sss():
    return render_template("sss.html")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = Kullanici.query.get(session["user_id"])
    turler = UrunTurleri.query.all()
    return render_template("profile.html", user=user, turler=turler)

#çıkış ekle
@app.route("/cikis")
def cikis():
    session.clear()
    return redirect(url_for("login"))

#çıkış ekle
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("is_admin"):
        flash("Bu sayfaya erişim yetkiniz yok!", "danger")
        return redirect(url_for("index"))
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        form_tipi = request.form.get("form_tipi")

        try:
            # TÜR EKLE
            if form_tipi == "tur":
                tur = request.form.get("tur")
                if tur:
                    db.session.add(UrunTurleri(tur=tur))

            # ÜRÜN EKLE
            elif form_tipi == "urun":
                urun_adi = request.form.get("urun_adi")
                tur_id = int(request.form.get("urun_turu"))
                fiyat = int(request.form.get("fiyat"))
                img = request.form.get("img")
                aciklama = request.form.get("aciklama")

                yeni_urun = Urunler(
                    urun_adi=urun_adi,
                    tur_id=tur_id,
                    fiyat=fiyat,
                    img=img,
                    aciklama=aciklama
                )
                db.session.add(yeni_urun)

            db.session.commit()
            flash("Başarıyla kaydedildi", "success")

        except Exception as e:
            db.session.rollback()
            flash(f"Hata: {e}", "danger")

    urunler = db.session.query(
        Urunler.id,
        Urunler.urun_adi,
        Urunler.fiyat,
        UrunTurleri.tur
    ).join(UrunTurleri).all()

    turler = UrunTurleri.query.all()

    return render_template("admin.html", urunler=urunler, turler=turler)

@app.route("/urun_sil/<int:id>", methods=["POST"])
def urun_sil(id):
    urun = Urunler.query.get_or_404(id)
    db.session.delete(urun)
    db.session.commit()
    flash("Ürün silindi", "success")
    return redirect(url_for("admin"))

@app.route("/para_yukle", methods=["POST"])
def para_yukle():
    if "user_id" not in session:
        flash("Önce giriş yapmalısınız.", "danger")
        return redirect(url_for("login"))

    miktar = request.form.get("miktar")
    try:
        miktar = int(miktar)
        if miktar <= 0:
            flash("Geçersiz miktar", "danger")
            return redirect(url_for("profile"))
    except:
        flash("Geçersiz miktar", "danger")
        return redirect(url_for("profile"))

    kullanici = Kullanici.query.get(session["user_id"])
    kullanici.money += miktar
    db.session.commit()
    flash(f"{miktar}₺ bakiyeniz başarıyla yüklendi!", "success")
    return redirect(url_for("profile"))
@app.route("/satinal", methods=["POST"])
def satinal():
    if "user_id" not in session:
        flash("Önce giriş yapmalısınız.", "danger")
        return redirect(url_for("login"))

    urun_id = int(request.form.get("urun_id"))
    kullanici = Kullanici.query.get(session["user_id"])
    urun = Urunler.query.get(urun_id)

    if not urun:
        flash("Ürün bulunamadı.", "danger")
        return redirect(request.referrer or url_for("market"))

    if kullanici.money < urun.fiyat:
        flash("Yeterli bakiyeniz yok.", "danger")
        return redirect(request.referrer or url_for("market"))

    # Sepet kontrolü: Beklemede sipariş var mı?
    siparis = Siparis.query.filter_by(kullanici_id=kullanici.id, durum_id=1).first()
    if not siparis:
        siparis = Siparis(kullanici_id=kullanici.id, durum_id=1, tutar=0)
        db.session.add(siparis)
        db.session.commit()

    # Sipariş detayını ekle
    detay = SiparisDetay.query.filter_by(
        siparis_id=siparis.id,
        urun_id=urun.id
    ).first()
    if detay:
        detay.miktar += 1
    else:
        detay = SiparisDetay(
            siparis_id=siparis.id,
            urun_id=urun.id,
            miktar=1
        )
        db.session.add(detay)

    # Kullanıcı bakiyesi düşürülür
    kullanici.money -= urun.fiyat
    siparis.tutar += urun.fiyat
    db.session.commit()

    # Sepetteki ürün sayısını session’a kaydet
    session["cart_count"] = sum(
        d.miktar for d in SiparisDetay.query.filter_by(siparis_id=siparis.id).all()
    )

    flash(f"{urun.urun_adi} sepete eklendi!", "success")
    return redirect(request.referrer or url_for("market"))


@app.route("/siparis_onayla", methods=["POST"])
def siparis_onayla():
    if "user_id" not in session:
        flash("Önce giriş yapmalısınız.", "danger")
        return redirect(url_for("login"))

    kullanici = Kullanici.query.get(session["user_id"])
    siparis = Siparis.query.filter_by(kullanici_id=kullanici.id, durum_id=1).first()
    if not siparis:
        flash("Sepetiniz boş.", "danger")
        return redirect(url_for("siparis"))

    siparis.durum_id = 2  # Onaylandı
    db.session.commit()

    # Sepet sayısını sıfırla
    session["cart_count"] = 0

    flash("Siparişiniz onaylandı!", "success")
    return redirect(url_for("siparis"))

@app.route("/destek", methods=["GET", "POST"])
def destek():
    if request.method == "POST":
        email = request.form.get("email")
        konu = request.form.get("konu")
        mesaj = request.form.get("mesaj")

        try:
            msg = MIMEMultipart()
            msg["From"] = MAIL_SENDER
            msg["To"] = MAIL_RECEIVER
            msg["Subject"] = f"Destek Talebi: {konu}"

            body = f"""
Gönderen E-posta: {email}

Mesaj:
{mesaj}
"""
            msg.attach(MIMEText(body, "plain", "utf-8"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(MAIL_SENDER, MAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

            flash("Mesajınız başarıyla gönderildi.", "success")
            return redirect(url_for("destek"))

        except Exception as e:
            flash(f"E-posta gönderilemedi: {e}", "danger")
            return redirect(url_for("destek"))

    return render_template("destek.html")
@app.route("/kullanici_urun_ekle", methods=["POST"])
def kullanici_urun_ekle():
    if "user_id" not in session:
        flash("Önce giriş yapmalısınız.", "danger")
        return redirect(url_for("login"))

    urun_adi = request.form.get("urun_adi")
    tur_id = int(request.form.get("urun_turu"))
    fiyat = int(request.form.get("fiyat"))
    img = request.form.get("img")
    aciklama = request.form.get("aciklama")

    yeni_urun = Urunler(
        urun_adi=urun_adi,
        tur_id=tur_id,
        fiyat=fiyat,
        img=img,
        aciklama=aciklama
    )
    
    turler = UrunTurleri.query.all()

    try:
        db.session.add(yeni_urun)
        db.session.commit()
        flash(f"{urun_adi} başarıyla eklendi!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Hata: {e}", "danger")

    return redirect(url_for("profile"))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug = True)

