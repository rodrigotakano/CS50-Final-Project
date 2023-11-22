import sqlite3
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Create database
con = sqlite3.connect("database.db", check_same_thread=False)

# Create cursor to manipulate database
c = con.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/view")
def view():
    tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';")    
    return render_template("view.html", tables = tables)

@app.route("/open", methods=["POST"])
def open():
    return render_template("open.html")