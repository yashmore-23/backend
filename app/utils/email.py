import smtplib
from email.mime.text import MIMEText
from app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = to_email

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, to_email, msg.as_string())
            print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

