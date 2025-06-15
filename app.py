from flask import Flask, render_template, request, redirect, url_for, session, make_response
#from db import db, User
from flask_mail import Mail, Message
import random
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import datetime, timedelta
import calendar
import requests
from flask import jsonify, session
from sqlalchemy import func

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pytracker43@gmail.com'
app.config['MAIL_PASSWORD'] = 'ayxg eoaa xkij kiha'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)



def send_otp_email(recipient, otp):
    msg = Message('Your OTP Code',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[recipient])
    msg.body = f'Your OTP is: {otp}'
    mail.send(msg)

def generate_otp():
    """Generate a 6-digit numeric OTP as a string."""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=int(os.getenv("MYSQL_PORT"))
    )


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ezekieldb123@localhost/pytrack_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.init_app(app)

app.secret_key = '123123123'

@app.route("/", methods=["GET", "POST"])
def login():
    # Initialize error message and get remembered credentials from cookies
    error = None
    remembered_id = request.cookies.get('remember_id', '')
    remembered_password = request.cookies.get('remember_password', '')
    if request.method == "POST":
        # Get user input from the login form
        id_number = request.form.get("identification", "").strip()
        password = request.form.get("password", "").strip()
        remember = request.form.get("remember_me")

        # Connect to MySQL and query for the user by id_number
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login_main WHERE id_number = %s", (id_number,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Check if the password matches
            if user['password'] == password:
                # Store user's name in session
                session['user'] = user['name']
                # Redirect based on user type in id_number
                resp = make_response(
                    redirect(
                        url_for('adminUI') if "AD" in id_number else
                        url_for('profUI') if "TC" in id_number else
                        url_for('studentUI') if "SD" in id_number else
                        url_for('login')
                    )
                )
                # Handle "Remember Me" cookies
                if remember:
                    resp.set_cookie('remember_id', id_number, max_age=60*60*24*30)
                    resp.set_cookie('remember_password', password, max_age=60*60*24*30)
                else:
                    resp.set_cookie('remember_id', '', expires=0)
                    resp.set_cookie('remember_password', '', expires=0)
                return resp
            else:
                # Password is incorrect
                error = "Incorrect password."
        else:
            # No user found with that id_number
            error = "Account not found."
    # Render the login page with any error messages and remembered credentials
    return render_template("login.html", error=error, remembered_id=remembered_id, remembered_password=remembered_password)




@app.route("/admin")
def adminUI():
    return render_template("adminUI.html")


""""
@app.route("/prof")
def profUI():
    prof_name = None
    attendance_calendar = {}
    histogram_counts = {
        "Absent": 0,
        "Late": 0,
        "No Classes/Excused": 0,
        "Attended": 0,
        "Days Remaining": 0
    }
    today = datetime.today()
    # School year start (adjust as needed)
    school_year_start = datetime(today.year if today.month >= 6 else today.year - 1, 6, 1)
    school_days_passed = 0
    total_school_days = 180

    # Calculate school days passed (Mon-Fri, skip weekends)
    d = school_year_start
    while d <= today:
        if d.weekday() < 5:  # Mon-Fri
            school_days_passed += 1
        d += timedelta(days=1)
    days_remaining = max(0, total_school_days - school_days_passed)
    histogram_counts["Days Remaining"] = days_remaining

    # Calculate calendar range: -2 months to +5 months
    months = []
    for i in range(-2, 6):
        month = (today.month + i - 1) % 12 + 1
        year = today.year + ((today.month + i - 1) // 12)
        months.append((year, month))

    if 'user' in session:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, id_number FROM login_main WHERE name = %s", (session['user'],))
        result = cursor.fetchone()
        if result:
            prof_name = result['name']
            prof_id = result['id_number']
            # Get all classes for this professor
            cursor.execute("SELECT class_ID FROM classes_database WHERE teacher_ID = %s", (prof_id,))
            class_ids = [row['class_ID'] for row in cursor.fetchall()]
            # Build calendar days
            calendar_days = []
            for year, month in months:
                _, last_day = calendar.monthrange(year, month)
                for day in range(1, last_day + 1):
                    d = datetime(year, month, day)
                    calendar_days.append(d)
            # Query attendance for these classes and days
            attendance_map = {}
            for d in calendar_days:
                date_str = d.strftime("%Y-%m-%d")
                found = False
                for class_id in class_ids:
                    cursor.execute("SELECT 1 FROM attendance_database WHERE class_ID = %s AND date = %s LIMIT 1", (class_id, date_str))
                    if cursor.fetchone():
                        found = True
                        break
                attendance_map[date_str] = found
            attendance_calendar = {
                "months": months,
                "days": calendar_days,
                "attendance": attendance_map
            }
            # Histogram: count attendance statuses for this professor's classes
            if class_ids:
                format_strings = ','.join(['%s'] * len(class_ids))
                cursor.execute(f"SELECT status FROM attendance_database WHERE class_ID IN ({format_strings})", tuple(class_ids))
                for row in cursor.fetchall():
                    status = row['status'].strip().lower()
                    if status == "present":
                        histogram_counts["Attended"] += 1
                    elif status == "late":
                        histogram_counts["Late"] += 1
                    elif status == "absent":
                        histogram_counts["Absent"] += 1
                    else:
                        histogram_counts["No Classes/Excused"] += 1
        cursor.close()
        conn.close()
    return render_template(
    "profUI.html",
    prof_name=prof_name,
    attendance_calendar=attendance_calendar,
    histogram_counts=histogram_counts,
    datetime=datetime,
    calendar=calendar
)
"""

@app.route("/prof")
def profUI():
    prof_name = None
    attendance_calendar = {}
    histogram_counts = {
        "Absent": 0,
        "Late": 0,
        "No Classes/Excused": 0,
        "Attended": 0,
        "Days Remaining": 0
    }
    today = datetime.today()
    # School year start (adjust as needed)
    school_year_start = datetime(today.year if today.month >= 6 else today.year - 1, 6, 1)
    school_days_passed = 0
    total_school_days = 180

    # Calculate school days passed (Mon-Fri, skip weekends)
    d = school_year_start
    while d <= today:
        if d.weekday() < 5:  # Mon-Fri
            school_days_passed += 1
        d += timedelta(days=1)
    days_remaining = max(0, total_school_days - school_days_passed)
    histogram_counts["Days Remaining"] = days_remaining

    # Calculate calendar range: -2 months to +5 months
    months = []
    for i in range(-2, 6):
        month = (today.month + i - 1) % 12 + 1
        year = today.year + ((today.month + i - 1) // 12)
        months.append((year, month))

    if 'user' in session:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        # Get professor's name and ID
        cursor.execute("SELECT name, id_number FROM login_main WHERE name = %s", (session['user'],))
        prof_row = cursor.fetchone()
        prof_name = prof_row['name'] if prof_row else None
        prof_id_test = prof_row['id_number'] if prof_row else None
        # Get class IDs for this professor
        class_ids = None
        if prof_id_test:
            cursor.execute("SELECT class_ID FROM classes_database WHERE teacher_ID = %s", (prof_id_test,))
            class_rows = cursor.fetchall()
            class_ids = [row['class_ID'] for row in class_rows] if class_rows else None
        cursor.close()
        conn.close()
    return render_template(
        "profUI.html",
        prof_name=prof_name,
        attendance_calendar=attendance_calendar,
        histogram_counts=histogram_counts,
        datetime=datetime,
        calendar=calendar
    )

@app.route("/student")
def studentUI():
    return render_template("studentUI.html")




@app.route("/step2")
def step2():
    return render_template("role.html")

@app.route("/credentials", methods=["GET", "POST"])
def register():
    role = None
    if request.method == "POST":
        role = request.form.get("role")
    return render_template("register.html", role=role)

@app.route("/register2", methods=["GET", "POST"])
def register2():
    role = request.form.get("role") or request.args.get("role") or None
    return render_template("register2.html", role=role)




@app.route('/otp', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        email = request.form.get('email')
        otp_code = generate_otp()
        session['otp'] = otp_code
        session['email'] = email
        send_otp_email(email, otp_code)
        return render_template("verify.html", email=email)
    return redirect(url_for('register2'))

@app.route("/weather")
def get_weather():
    # Example: Manila coordinates
    latitude = 14.5995
    longitude = 120.9842
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        "&daily=weathercode,temperature_2m_max,temperature_2m_min"
        "&timezone=Asia/Manila"
    )
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        today = {
            "date": data["daily"]["time"][0],
            "weathercode": data["daily"]["weathercode"][0],
            "temp_max": data["daily"]["temperature_2m_max"][0],
            "temp_min": data["daily"]["temperature_2m_min"][0],
        }
        tomorrow = {
            "date": data["daily"]["time"][1],
            "weathercode": data["daily"]["weathercode"][1],
            "temp_max": data["daily"]["temperature_2m_max"][1],
            "temp_min": data["daily"]["temperature_2m_min"][1],
        }
        return jsonify({"today": today, "tomorrow": tomorrow})
    except Exception as e:
        return jsonify({"error": "Weather unavailable"}), 500

# Example SQLAlchemy model (adjust as needed)

@app.route("/histogram_data")
def histogram_data():
    # Use session['user'] to get the professor's name, then get their ID
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 401

    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    # Get professor's ID
    cursor.execute("SELECT id_number FROM login_main WHERE name = %s", (session['user'],))
    prof = cursor.fetchone()
    if not prof:
        cursor.close()
        conn.close()
        return jsonify({"error": "Professor not found"}), 404
    prof_id = prof['id_number']

    # Get all class_IDs for this professor
    cursor.execute("SELECT class_ID FROM classes_database WHERE teacher_ID = %s", (prof_id,))
    class_ids = [row['class_ID'] for row in cursor.fetchall()]
    if not class_ids:
        cursor.close()
        conn.close()
        return jsonify({
            "Absent": 0,
            "Late": 0,
            "No Classes/Excused": 0,
            "Attended": 0,
            "Days Remaining": 180
        })

    format_strings = ','.join(['%s'] * len(class_ids))

    # Count statuses
    cursor.execute(f"SELECT status, COUNT(*) as count FROM attendance_database WHERE class_ID IN ({format_strings}) GROUP BY status", tuple(class_ids))
    status_counts = {row['status'].strip().lower(): row['count'] for row in cursor.fetchall()}

    absent = status_counts.get('absent', 0)
    late = status_counts.get('late', 0)
    attended = status_counts.get('attended', 0) + status_counts.get('present', 0)
    excused = status_counts.get('no classes/excused', 0)

    # Days remaining (assuming 180 total school days)
    cursor.execute(f"SELECT COUNT(DISTINCT date) as days_recorded FROM attendance_database WHERE class_ID IN ({format_strings})", tuple(class_ids))
    days_recorded = cursor.fetchone()['days_recorded']
    days_remaining = max(0, 180 - days_recorded)

    cursor.close()
    conn.close()

    return jsonify({
        "Absent": absent,
        "Late": late,
        "No Classes/Excused": excused,
        "Attended": attended,
        "Days Remaining": days_remaining
    })

@app.route("/attendance_heatmap_data")
def attendance_heatmap_data():
    if 'user' not in session:
        return jsonify({})

    # Get professor's ID
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_number FROM login_main WHERE name = %s", (session['user'],))
    prof = cursor.fetchone()
    if not prof:
        cursor.close()
        conn.close()
        return jsonify({})
    prof_id = prof['id_number']

    # Get all class_IDs for this professor
    cursor.execute("SELECT class_ID FROM classes_database WHERE teacher_ID = %s", (prof_id,))
    class_ids = [row['class_ID'] for row in cursor.fetchall()]
    if not class_ids:
        cursor.close()
        conn.close()
        return jsonify({})

    # Calculate date range: 2 months before to 5 months after current month
    today = datetime.today()
    start_month = today.month - 2
    start_year = today.year
    if start_month <= 0:
        start_month += 12
        start_year -= 1
    start_date = datetime(start_year, start_month, 1)
    end_month = today.month + 5
    end_year = today.year
    if end_month > 12:
        end_month -= 12
        end_year += 1
    last_day = calendar.monthrange(end_year, end_month)[1]
    end_date = datetime(end_year, end_month, last_day)

    # Build all dates in range
    date_map = {}
    d = start_date
    while d <= end_date:
        date_map[d.strftime("%Y-%m-%d")] = 0  # default: not attended
        d += timedelta(days=1)

    # For all class_IDs, get all attendance dates where at least one student attended
    format_strings = ','.join(['%s'] * len(class_ids))
    cursor.execute(
        f"SELECT DISTINCT date FROM attendance_database WHERE class_ID IN ({format_strings}) AND date BETWEEN %s AND %s",
        tuple(class_ids) + (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    )
    attended_dates = set(row['date'] for row in cursor.fetchall())

    # Mark attended dates as green (1)
    for date_str in attended_dates:
        if date_str in date_map:
            date_map[date_str] = 1

    cursor.close()
    conn.close()
    return jsonify(date_map)

@app.route("/get_classes")
def get_classes():
    if 'user' not in session:
        print("No user in session for /get_classes")
        return jsonify([])
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    # Get professor's id_number robustly
    cursor.execute("""
        SELECT id_number FROM login_main
        WHERE TRIM(LOWER(name)) = TRIM(LOWER(%s))
    """, (session['user'],))
    prof = cursor.fetchone()
    if not prof:
        print(f"Professor not found for user: {session['user']}")
        cursor.close()
        conn.close()
        return jsonify([])
    prof_id = prof['id_number']
    # Now robustly get classes
    cursor.execute("""
        SELECT class_ID, subject, semester FROM classes_database
        WHERE TRIM(teacher_ID) = TRIM(%s)
    """, (prof_id,))
    classes = [
        {
            "class_ID": row['class_ID'],
            "subject": row['subject'],
            "semester": row['semester']
        }
        for row in cursor.fetchall()
    ]
    print(f"Classes found for {session['user']} ({prof_id}): {classes}")
    cursor.close()
    conn.close()
    return jsonify(classes)

@app.route("/get_subjects")
def get_subjects():
    class_id = request.args.get("class_id")
    print("Received class_id for /get_subjects:", class_id)
    if not class_id:
        return jsonify([])
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT subject FROM classes_database WHERE class_ID = %s", (class_id,))
    subjects = [row['subject'] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(subjects)

@app.route("/get_sections")
def get_sections():
    class_id = request.args.get("class_id")
    if not class_id:
        return jsonify([])
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT semester FROM classes_database WHERE class_ID = %s", (class_id,))
    sections = [row['semester'] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(sections)

@app.route("/get_students")
def get_students():
    class_id = request.args.get("class_id")
    subject = request.args.get("subject")
    section = request.args.get("section")
    if not class_id or not subject or not section:
        return jsonify({})  # Return empty dict for grouping

    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    # Get all student_IDs enrolled in this class
    cursor.execute("SELECT student_ID FROM enrollment_database WHERE class_ID = %s", (class_id,))
    student_ids = [row['student_ID'] for row in cursor.fetchall()]
    if not student_ids:
        cursor.close()
        conn.close()
        return jsonify({})

    format_strings = ','.join(['%s'] * len(student_ids))
    cursor.execute(
        f"SELECT name, id_number, course, year_section FROM login_main WHERE id_number IN ({format_strings})",
        tuple(student_ids)
    )
    students = cursor.fetchall()
    cursor.close()
    conn.close()

    # Group students by first letter of last name
    grouped = {}
    for stu in students:
        # Assume last name is the last word in the name field
        last_name = stu['name'].split()[-1].upper()
        initial = last_name[0]
        if initial not in grouped:
            grouped[initial] = []
        grouped[initial].append(stu)
    # Sort each group by last name, then first name
    for initial in grouped:
        grouped[initial].sort(key=lambda s: (s['name'].split()[-1].upper(), s['name'].upper()))
    # Sort the groups by initial
    grouped_sorted = dict(sorted(grouped.items()))
    return jsonify(grouped_sorted)

if __name__ == "__main__":
    app.run(debug=True)