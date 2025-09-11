from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)


# Veritabanını başlatmak için
def init_db():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")

        # Veritabanına kaydet
        conn = sqlite3.connect("messages.db")
        c = conn.cursor()
        c.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
        conn.commit()
        conn.close()

        return f"<h2>Teşekkürler {name}!</h2><p>Mesajın kaydedildi.</p><a href='/form'>Geri dön</a>"

    return render_template("form.html")


@app.route("/messages")
def messages():
    conn = sqlite3.connect("messages.db")
    c = conn.cursor()
    c.execute("SELECT name, message FROM messages ORDER BY id DESC")
    all_messages = c.fetchall()
    conn.close()

    return render_template("messages.html", messages=all_messages)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

