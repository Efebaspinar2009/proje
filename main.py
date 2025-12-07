from flask import Flask , render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/deneme")
def deneme():
    isim = "efe"
    x = 10
    return render_template("deneme.html" , isim = isim , x = x)

app.run(debug = True)