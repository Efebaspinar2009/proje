from flask import Flask , render_template , request , flash , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column , Integer , ForeignKey
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
## form.get kullan
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']  = "skgdgdhgjkhfdjkghkdjfhgkjdhg"

db = SQLAlchemy(app)

durumlar =  ["hazır" , "beklemede" , "hazırlanıyor" , "tamamlandı"]
#databasa in oluşturması
class Kullanici(db.Model):
    id = db.Column(db.Integer , primary_key = True )
    kullanici_adi = db.Column(db.String(50) , unique = True , nullable = False)
    email = db.Column(db.String(50) , unique = True , nullable = False)
    sifre = db.Column(db.String(20) , nullable = False)
    money = db.Column(db.Integer)

class Durum(db.Model):
    __tablename__ =  "durum"
    durum  = db.Column(db.String(40))
    id = db.Column(db.Integer ,  primary_key = True)

class Siparis(db.Model):
    __tablename__ = "sipariş"
    sipariş_id = db.Column(db.String , primary_key = True)
    kullanici_id = db.Column(db.Integer , ForeignKey("kullanici.id"))
    durum_id = db.Column(db.Integer , ForeignKey("durum.id"))
    tutar = db.Column(db.Integer)
    tur = db.Column(db.String , ForeignKey("urun_turleri.id"))

class Urun_turleri(db.Model):
    __tablename__ = "urun_turleri"
    tur = db.Column(db.String)
    id = db.Column(db. Integer , primary_key = True)
    
class Urunler(db.Model):
    __tablename__ = "urunler"
    urun_adi = db.Column(db.String)
    tur = db.Column(db.String , ForeignKey("urun_turleri.id"))
    id  = db.Column(db.Integer , primary_key = True)
    fiyat = db.Column(db.Integer)
    img = db.Column(db.String)
    
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
            return render_template("login.html")
            
        except:
            flash("zaten eklisiniz lütfen kayıt olunuz" ,"danger")
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
            
            
        else:
            flash("kullanıcı adı veya e-posta bulunamadı" , "danger")
        
    return render_template("login.html")

@app.route("/deneme")
def deneme():
    isim = "efe"
    x = 10
    return render_template("deneme.html" , isim = isim , x = x)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug = True)


