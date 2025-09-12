from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="db",        # docker-compose'da mysql servisine verdiğimiz isim
        user="root",
        password="password",
        database="flask_app"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hakkimda")
def about():
    return render_template("about.html")

@app.route("/mesaj-gonder", methods=["GET", "POST"])
def send_message():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/mesajlar")

    return render_template("send_message.html")

@app.route("/mesajlar")
def messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, message, created_at FROM messages ORDER BY id DESC")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("messages.html", messages=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
