from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import random
from dotenv import load_dotenv
import os
import mysql.connector
import calendar
import requests
from abc import ABC, abstractmethod

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pytracker43@gmail.com'
app.config['MAIL_PASSWORD'] = 'ayxg eoaa xkij kiha'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=int(os.getenv("MYSQL_PORT"))
    )

@app.route("/", methods=["GET", "POST"])
def test():
    conn = get_mysql_connection()
    cursor = conn.cursor()

    new_password = input("Enter:")
    id_number = input("Enter")
    cursor.execute("SET SQL_SAFE_UPDATES = 0")
    cursor.execute("UPDATE login_main SET password = %s WHERE id_number = %s", (new_password, id_number))
    



if __name__ == "__main__":
    app.run(debug=True)