from flask import Flask, render_template, request, redirect, url_for, session, make_response
from db import db, User
from flask_mail import Mail, Message
import random

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



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ezekieldb123@localhost/pytrack_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '123123123'

db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def login():
    # Initialize error message and get remembered credentials from cookies
    error = None
    remembered_id = request.cookies.get('remember_id', '')
    remembered_password = request.cookies.get('remember_password', '')
    if request.method == "POST":
        # Get form data from the login form
        id_number = request.form.get("identification", "").strip()
        password = request.form.get("password", "").strip()
        remember = request.form.get("remember_me")  # Checkbox value (None if unchecked)
        # Query the user from the database using the provided ID number
        user = User.query.filter_by(ID_number=id_number).first()
        if user:
            # If user exists, check if the password matches
            if user.password == password:
                # Set session for the logged-in user
                session['user'] = user.name
                # Prepare redirect response based on user role
                resp = make_response(
                    redirect(
                        url_for('adminUI') if "AD" in id_number else
                        url_for('profUI') if "TC" in id_number else
                        url_for('studentUI') if "SD" in id_number else
                        url_for('login')
                    )
                )
                # If "Remember Me" is checked, save ID and password in cookies for 30 days
                if remember:
                    resp.set_cookie('remember_id', id_number, max_age=60*60*24*30)
                    resp.set_cookie('remember_password', password, max_age=60*60*24*30)
                else:
                    # Otherwise, clear the cookies
                    resp.set_cookie('remember_id', '', expires=0)
                    resp.set_cookie('remember_password', '', expires=0)
                return resp
            else:
                # Password is incorrect
                error = "Incorrect password."
        else:
            # User not found in the database
            error = "Account not found."
    # Render the login page, passing error and remembered credentials to the template
    return render_template("login.html", error=error, remembered_id=remembered_id, remembered_password=remembered_password)




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

if __name__ == "__main__":
    app.run(debug=True)