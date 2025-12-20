from flask import Flask , render_template , request , flash , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column , Integer , ForeignKey
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash 
## form.get kullan
 
##https://stackoverflow.com/questions/20503183/python-flask-working-with-wraps incele
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']  = "skgdgdhgjkhfdjkghkdjfhgkjdhg"

db = SQLAlchemy(app)

#databasa in oluşturması
class Kullanici(db.Model):
    __tablename__ = "kullanici"

    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    sifre = db.Column(db.String(255), nullable=False)
    money = db.Column(db.Integer, default=0)


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
    
@app.route("/")
def index():
    return render_template("index.html")



@app.route("/x" , methods = ["GET" , "POST"])
def a():
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
@app.route("/register" , methods = ["GET" , "POST"])
def register():
    if request.method == "POST":
        kullanici_adi  = request.form["ad"]
        kullanici_mail = request.form["email"]
        hashed_sifre = generate_password_hash(request.form["sifre"] , method = "pbkdf2:sha256")
        money = 0
        yeni_kullanici = Kullanici(kullanici_adi = kullanici_adi , email = kullanici_mail , sifre = hashed_sifre  , money = money)
        
        try:
            db.session.add(yeni_kullanici)
            db.session.commit()
            flash("kayıt başarılı" , "success")
            return redirect(url_for("login"))
            
        except IntegrityError:
            flash("Bu kullanıcı adı veya e-posta zaten kayıtlı." ,"danger")
            return render_template("register.html")
    
        except:
            flash("Bir hata var", "danger")
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
    return render_template("market.html")

@app.route("/siparis")
def siparis():
    return render_template("orders.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

#çıkış ekle
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        form_tipi = request.form.get("form_tipi")

        try:
            if form_tipi == "tur":
                tur = request.form.get("tur")
                yeni_tur = UrunTurleri(tur=tur)
                db.session.add(yeni_tur)

            elif form_tipi == "urun":
                urun_adi = request.form.get("urun_adi")
                urun_turu = request.form.get("urun_turu")
                fiyat = request.form.get("fiyat")
                img = request.form.get("img")
                aciklama = request.form.get("aciklama")

                tur = UrunTurleri.query.filter_by(tur=urun_turu).first()
                if not tur:
                    flash("Ürün türü bulunamadı")
                    return redirect(url_for("admin"))

                yeni_urun = Urunler(
                    urun_adi=urun_adi,
                    tur_id=tur.id,
                    fiyat=fiyat,
                    img=img,
                    aciklama=aciklama
                )

                db.session.add(yeni_urun)

            db.session.commit()
            flash("Başarıyla eklendi")

        except Exception as e:
            db.session.rollback()
            flash(f"Hata: {e}")

    return render_template("admin.html")
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug = True)

