from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# MySQL bağlantısı (Docker Compose ortam değişkenleri üzerinden)
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "secret")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "db")
MYSQL_DB = os.environ.get("MYSQL_DATABASE", "flaskdb")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Mesaj tablosu
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Veritabanını başlat
@app.before_first_request
def init_db():
    db.create_all()

# Ana sayfa
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Form sayfası
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name")
        message_text = request.form.get("message")

        # Veritabanına kaydet
        new_message = Message(name=name, message=message_text)
        db.session.add(new_message)
        db.session.commit()

        return f"<h2>Teşekkürler {name}!</h2><p>Mesajın kaydedildi.</p><a href='/form'>Geri dön</a>"

    return render_template("form.html")

# Mesajları listeleme
@app.route("/messages")
def messages():
    all_messages = Message.query.order_by(Message.id.desc()).all()
    return render_template("messages.html", messages=all_messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
