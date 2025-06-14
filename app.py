from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import random
from dotenv import load_dotenv
import os
import mysql.connector
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
    msg = Message(
        'Your OTP Code',
        sender=("Pytracker", app.config['MAIL_USERNAME']),
        recipients=[recipient]
    )
    msg.body = f'Your OTP is: {otp}'  # Fallback for non-HTML clients
    msg.html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: auto; border: 1px solid #eee; border-radius: 8px; padding: 32px 24px;">
        <h2 style="color: #d32f2f; text-align: center;">Register to Pytracker</h2>
        <p style="font-size: 16px; text-align: center;">Welcome! Enter this code within the next 10 minutes to log in:</p>
        <div style="font-size: 32px; font-weight: bold; letter-spacing: 4px; background: #f5f5f5; border-radius: 6px; padding: 16px; text-align: center; margin: 24px 0;">
            {otp}
        </div>
        <p style="font-size: 12px; color: #888; text-align: center;">
            You’re receiving this email because you requested a register code for your Pytracker account.<br>
            If you did not request this, you can safely ignore this email.
        </p>
        <div style="text-align: center; margin-top: 32px; font-size: 12px; color: #bbb;">
            Made for you with ❤️<br>
            Pytracker Team
        </div>
    </div>
    """
    mail.send(msg)
       
@app.route('/resend_otp', methods=['POST'])
def resend_otp():
    """
    Handles AJAX request to resend OTP.
    """
    email = session.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'No email found in session.'}), 400
    otp_code = generate_otp()
    session['otp'] = otp_code
    send_otp_email(email, otp_code)
    return jsonify({'success': True, 'message': 'A new code has been sent to your email.'})

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

app.secret_key = '123123123'




@app.route("/", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    - On GET: renders the login form.
    - On POST: authenticates user and redirects based on role.
    """
    
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



@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    error = None
    show_otp = False
    id_number = ""
    if request.method == "POST":
        id_number = request.form.get("identification", "").strip()
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT 1 FROM login_main WHERE id_number = %s", (id_number,))
        found = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        if found:
            show_otp = True
        else:
            error = "No such ID number is registered."
    return render_template("forgot_password.html", show_otp=show_otp, error=error, id_number=id_number)


@app.route('/check_id', methods=['POST'])
def check_id():
    id_number = request.json.get('id_number')
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM login_main WHERE id_number = %s", (id_number,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        email = row['email']
        otp_code = generate_otp()
        session['otp'] = otp_code
        session['email'] = email
        session['id_number'] = id_number   
        send_otp_email(email, otp_code)
        return jsonify({'exists': True, 'email': email})
    else:
        return jsonify({'exists': False})

@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    error = None
    if request.method == 'POST':
        new_password = request.form.get('new-password')
        confirm_password = request.form.get('confirm-password')
        if new_password != confirm_password:
            error = "Passwords do not match."
        else:
            id_number = session.get('id_number') 
            try:
                conn = get_mysql_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE login_main SET password = %s WHERE id_number = %s", (new_password, id_number))
                conn.commit()
                cursor.close()
                conn.close()
                session.pop('otp', None)
                session.pop('email', None)
                session.pop('id_number', None)
                return redirect(url_for('changepasswordcomplete'))
            except mysql.connector.Error:
                error = "Cannot connect to the database. Please try again later."
    return render_template('change_password.html', error=error)

@app.route('/check_otp', methods=['POST'])
def check_otp():
    input_otp = request.json.get('otp')
    if input_otp == session.get('otp'):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Incorrect OTP. Please try again.'})

@app.route('/changepasswordcomplete')
def changepasswordcomplete():
    return render_template('changepasswordcomplete.html')



@app.route("/admin")
def adminUI():
    return render_template("adminUI.html")

@app.route("/prof")
def profUI():
    return render_template("profUI.html")

@app.route("/student")
def studentUI():
    return render_template("studentUI.html")




@app.route("/step2")
def step2():
    return render_template("role.html")


@app.route("/credentials", methods=["GET", "POST"])
def register():
    """
    Handles the role selection step of registration.
    - On GET: renders the role selection form.
    - On POST: retrieves the selected role and passes it to the next step.
    """
    
    role = None
    error = None
    if request.method == "POST":
        # Get the selected role from the form submission
        role = request.form.get("role")
    # Render the registration form, passing the selected role and any error
    return render_template("register.html", role=role, error=error)

@app.route("/register2", methods=["GET", "POST"])
def register2():
    """
    Handles the first registration step:
    - For students: validates ID and name against enrollment DB.
    - For teachers: only checks ID format.
    """
    error = None
    # Get the selected role from the form or session
    role = request.form.get("role") or session.get("role")
    if request.method == "POST":
        # Get name and ID fields from the form
        first_name = request.form.get("first_name", "").strip()
        middle_name = request.form.get("middle_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        id_number = request.form.get("id-number", "").strip()
        # Combine names for comparison
        input_name = f"{first_name} {middle_name} {last_name}".replace("  ", " ").strip().lower()

        if role and role.lower() == "teacher":
            # Only check ID format for professors
            if "TC" not in id_number:
                error = "Professor ID must contain 'TC'."
            elif len(id_number) != 15:
                error = "Invalid ID number."
        else:
            # Student validation: check if already registered
            conn = get_mysql_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM login_main WHERE ID_number = %s", (id_number,))
            if cursor.fetchone():
                error = "This student ID is already registered."
            else:
                # Check if student is enrolled and name matches
                cursor.execute("SELECT name FROM enrollment_database WHERE student_ID = %s", (id_number,))
                row = cursor.fetchone()
                if not row:
                    error = "This student ID is not enrolled in the school."
                else:
                    db_name = row[0].strip().lower()
                    if db_name != input_name:
                        error = "The name you entered does not match our enrollment records."
            cursor.close()
            conn.close()

        if error:
            # If any error, re-render the form with error message
            return render_template("register.html", role=role, error=error)

        # Passed all checks, store registration info in session for next step
        session['name'] = f"{first_name} {middle_name} {last_name}".replace("  ", " ").strip()
        session['id_number'] = id_number
        session['role'] = role
        # Redirect to the next registration step (details)
        return redirect(url_for('register2_details'))

    # Render the registration form for GET or if not POST
    return render_template("register2.html", role=role)


@app.route("/register_details", methods=["GET", "POST"])
def register2_details():
    """
    Handles the second registration step:
    - For students: requires all fields.
    - For teachers: only requires email and password, and enforces gmail.com domain.
    """
    
    error = None
    if request.method == "POST":
        # Get form data
        email = request.form.get("email", "").strip()
        course = request.form.get("course", "").strip()
        year_section = request.form.get("year_section", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        role = session.get('role')

        # Teacher/professor logic
        if role and str(role).lower() in ["teacher", "professor"]:
            # Enforce gmail.com domain for teachers/professors
            if not email.lower().endswith("@gmail.com"):
                error = "Professors must use a gmail.com email address."
            # Set course and year_section to None for teachers/professors
            course = None
            year_section = None
            # Only require email, password, confirm_password for teachers
            if not all([email, password, confirm_password]):
                error = "All fields are required."
        else:
            # For students, require all fields
            if not all([email, course, year_section, password, confirm_password]):
                error = "All fields are required."

        # Check if passwords match
        if not error and password != confirm_password:
            error = "Passwords do not match."
            
        # If any error, re-render the form with error message
        if error:
            return render_template("register2.html", role=session.get('role'), error=error)

        # Store registration details in session for next step
        session['email'] = email
        session['course'] = course
        session['year_section'] = year_section
        session['password'] = password
        # Redirect to OTP verification
        return redirect(url_for('verify'))

    # Render the registration details form
    return render_template("register2.html", role=session.get('role'))


@app.route('/otp', methods=['GET', 'POST'])
def verify():
    """
    Handles OTP verification.
    - On GET: generates and sends OTP to the user's email.
    - On POST: checks the submitted OTP against the session value.
    - After 3 wrong attempts, user must wait (cooldown) before retrying.
    - Cooldown increases by 1 minute every 3 failed attempts.
    """
    # Initialize attempt and cooldown tracking in session if not present
    if 'otp_attempts' not in session:
        session['otp_attempts'] = 0
    if 'otp_cooldown_until' not in session:
        session['otp_cooldown_until'] = None
    if 'otp_cooldown_level' not in session:
        session['otp_cooldown_level'] = 1  # in minutes

    now = datetime.now()
    cooldown_until = session.get('otp_cooldown_until')
    cooldown_active = False

    # Check if cooldown is active
    if cooldown_until:
        cooldown_until_dt = datetime.fromisoformat(cooldown_until)
        if now < cooldown_until_dt:
            cooldown_active = True
            remaining = (cooldown_until_dt - now).seconds
        else:
            # Cooldown expired, reset attempts and cooldown
            session['otp_attempts'] = 0
            session['otp_cooldown_until'] = None

    if request.method == 'POST':
        if cooldown_active:
            # Still in cooldown, don't allow attempts
            mins = (remaining // 60) + 1
            return render_template("verify.html", email=session.get('email'),
                                   error=f"Too many incorrect attempts. Please wait {mins} minute(s) before trying again.")
        input_otp = request.form.get('otp')
        if input_otp:
            if input_otp == session.get('otp'):
                # Success: reset attempts and cooldown
                session['otp_attempts'] = 0
                session['otp_cooldown_level'] = 10
                session['otp_cooldown_until'] = None
                return redirect(url_for('complete_registration'))
            else:
                # Wrong OTP: increment attempts
                session['otp_attempts'] += 1
                if session['otp_attempts'] >= 3:
                    # Set cooldown: increases by 1 min each time
                    cooldown_minutes = session.get('otp_cooldown_level', 10)
                    session['otp_cooldown_until'] = (now + timedelta(minutes=cooldown_minutes)).isoformat()
                    session['otp_cooldown_level'] = cooldown_minutes + 10
                    return render_template("verify.html", email=session.get('email'),
                                           error=f"Too many incorrect attempts. Please wait {cooldown_minutes} minute(s) before trying again.")
                else:
                    return render_template("verify.html", email=session.get('email'),
                                           error="Incorrect OTP. Please try again.")
    else:
        # GET request: generate and send a new OTP to the user's email if not in cooldown
        if cooldown_active:
            mins = (remaining // 60) + 1
            return render_template("verify.html", email=session.get('email'),
                                   error=f"Too many incorrect attempts. Please wait {mins} minute(s) before trying again.")
        email = session.get('email')
        if email:
            otp_code = generate_otp()
            session['otp'] = otp_code
            send_otp_email(email, otp_code)
            print("OTP sent to", email, "with code", otp_code)

    # Render the OTP verification page (with or without error)
    return render_template("verify.html", email=session.get('email'))


@app.route('/complete_registration', methods=['GET', 'POST'])
def complete_registration():
    """
    Finalizes registration:
    - Students: inserts into login_main.
    - Teachers: generates TMP-XXX, inserts as pending into registration_main.
    """
    
    # Retrieve registration data from session
    name = session.get('name')
    email = session.get('email')
    role = session.get('role')
    password = session.get('password')
    id_number = session.get('id_number')
    course = session.get('course')
    year_section = session.get('year_section')

    # Normalize role to match ENUM in DB
    role_map = {"student": "Student", "teacher": "Teacher", "admin": "Admin"}
    role = role_map.get(str(role).lower(), role)

    conn = get_mysql_connection()
    cursor = conn.cursor()
    error = None

    if role == "Student":
        # Insert student registration directly into login_main
        try:
            cursor.execute("""
                INSERT INTO login_main (name, id_number, role, password, email, course, year_section)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, id_number, role, password, email, course, year_section))
            conn.commit()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            error = f"MySQL Error: {err}"
            
    elif role == "Teacher":
        # Generate next TMP-XXX ID for teacher registration
        cursor.execute("SELECT temp_ID FROM registration_main WHERE temp_ID LIKE 'TMP-%' ORDER BY Control_No DESC LIMIT 1")
        row = cursor.fetchone()
        if row and row[0]:
            try:
                # Extract the numeric part and increment
                last_num = int(row[0].split('-')[1])
            except (IndexError, ValueError):
                last_num = 0
        else:
            last_num = 0
        new_tmp_id = f"TMP-{last_num+1:03d}"
        
        # Insert teacher registration as pending into registration_main
        cursor.execute("""
            INSERT INTO registration_main (temp_ID, name, email, role, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (new_tmp_id, name, email, role, "Pending"))
        
   # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()
    return render_template("registration_complete.html", role=role, error=error)


if __name__ == "__main__":
    app.run(debug=True)