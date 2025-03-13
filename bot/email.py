import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bot.config import SENDER_EMAIL, SENDER_EMAIL_PASSWORD
from bot.logging import log_info, log_error, log_exception


def send_email(recipient_email: str, verification_code: str) -> bool:
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = "Gamer's Guild Verification Code"

    msg.attach(MIMEText(verification_code, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        log_info("Attempting to login to SMTP server.")
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)

        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())

        log_info(f"Email sent successfully to {recipient_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        log_error(f"SMTP Authentication Error: {e}")
    except smtplib.SMTPConnectError as e:
        log_error(f"SMTP Connection Error: {e}")
    except smtplib.SMTPException as e:
        log_error(f"SMTP Error: {e}")
    except Exception as e:
        log_exception(f"An unexpected error occurred: {e}")

    finally:
        try:
            server.quit()  # type: ignore
            log_info("SMTP connection closed.")
        except Exception as e:
            log_error(f"Failed to close the SMTP connection: {e}")

    return False
