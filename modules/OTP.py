import random
import smtplib
from email.mime.text import MIMEText

def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp_email(receiver_email, otp):

    sender_email = "pytrackers@gmail.com"         
    sender_password = "fokk udxv gigq uyuz"    

    subject = "Your PyTracker Registration OTP"
    body = f"Your OTP for PyTracker registration is: {otp}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    print("Attempting to send OTP to:", receiver_email)  

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("OTP sent successfully!")  
        return True
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return False