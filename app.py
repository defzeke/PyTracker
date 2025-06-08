from flask import Flask, render_template, request, redirect, url_for, session
from db import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ezekieldb123@localhost/pytrack_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '123123123'

db.init_app(app)



@app.route("/", methods=["GET", "POST"])
def login():
    """
    Handles user login:
    - Shows the login page on GET.
    - Checks credentials on POST and redirects to the correct UI.
    - Shows an error if login fails.
    """
    error = None 
    if request.method == "POST":    # Only process login if form is submitted
        id_number = request.form.get("identification", "").strip()  # Get ID number
        password = request.form.get("password", "").strip()         # Get password
        user = User.query.filter_by(ID_number=id_number).first()    # Find user
        if user:
            if user.password == password:
                session['user'] = user.name     # Store user name in session
                
                # Redirect based on user type in ID number
                if "AD" in id_number:
                    return redirect(url_for('adminUI'))
                elif "TC" in id_number:
                    return redirect(url_for('profUI'))
                elif "SD" in id_number:
                    return redirect(url_for('studentUI'))
                else:
                    error = "Unknown user type."   # ID doesn't match any known type
            else:
                error = "Incorrect password."
        else:
            error = "Account not found."
            
    # Render login page, passing any error message to the template
    return render_template("login.html", error=error)    





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
    if request.method == "POST":
        return render_template("register2.html")
    return render_template("register2.html")

@app.route('/otp', methods=['GET', 'POST'])
def verify():
    return render_template("verify.html")

if __name__ == "__main__":
    app.run(debug=True)
    


