from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")

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
    


