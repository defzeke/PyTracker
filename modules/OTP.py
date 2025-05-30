import random
import smtplib
from email.mime.text import MIMEText

def generate_otp(length=6):
    """
    Generate a numeric OTP of the specified length.
    Returns a string of random digits.
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp_email(receiver_email, otp):
    """
    Send an OTP email to the specified receiver_email.
    Uses Gmail SMTP with the sender's credentials.
    Returns True if sent successfully, False otherwise.
    """

    # Sender's Gmail credentials (use an app password for security)
    sender_email = "pytrackers@gmail.com"         
    sender_password = "fokk udxv gigq uyuz"    

    # Email subject and body
    subject = "Your PyTracker Registration OTP"
    body = f"Your OTP for PyTracker registration is: {otp}"

    # Create the email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        # Connect to Gmail SMTP server using SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password) # Login to Gmail
            server.sendmail(sender_email, receiver_email, msg.as_string()) # Send the email
        return True
    except Exception as e:
        # Print the error if sending fails
        return False