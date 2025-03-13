import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bot.config import SENDER_EMAIL, SENDER_EMAIL_PASSWORD


def send_email(recipient_email: str, verification_code: str) -> bool:
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = "Gamer's Guild Verification Code"

    msg.attach(MIMEText(verification_code, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)

        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())

        print(f"Email sent successfully to {recipient_email}")

        return True

    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        return False

    finally:
        server.quit()  # type: ignore
