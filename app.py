from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from utils.stock_analysis import get_stock_data
from utils.prediction import predict_trend

app = Flask(__name__)
app.secret_key = "secret"

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS portfolio (username TEXT, stock TEXT, price REAL)")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?)",(u,p))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p))
        if c.fetchone():
            session["user"] = u
            return redirect("/dashboard")
        return "Invalid"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT stock, price FROM portfolio WHERE username=?", (session["user"],))
    data = c.fetchall()
    conn.close()

    return render_template("dashboard.html", stocks=data)

@app.route("/analyze", methods=["POST"])
def analyze():
    stock = request.form["stock"]
    data = get_stock_data(stock)
    pred = predict_trend(stock)
    return render_template("result.html", stock=stock, data=data, prediction=pred)

@app.route("/save", methods=["POST"])
def save():
    stock = request.form["stock"]
    price = get_stock_data(stock)["price"]
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO portfolio VALUES (?,?,?)",(session["user"],stock,price))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
