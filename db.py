import mysql.connector

try:
    conn = mysql.connector.connect(
        host="db-mysql-nyc3-08168-do-user-23255573-0.i.db.ondigitalocean.com",
        user="doadmin",
        password="AVNS_uBINZfU151Az7_ErIt3",
        database="pytracker_db",
        port=25060
    )
    print("Connected!")
    conn.close()
except Exception as e:
    print("FAILED:", e)

def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=int(os.getenv("MYSQL_PORT"))
    )