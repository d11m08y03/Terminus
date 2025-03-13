import os
from dotenv import load_dotenv

load_dotenv()

default = "Uninitialised"

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", default)
VERIFICATION_CHANNEL_ID = os.getenv("VERIFICATION_CHANNEL_ID", default)
SENDER_EMAIL = os.getenv("SENDER_EMAIL", default)
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD", default)
EMAIL_DOMAIN = os.getenv("EMAIL_DOMAIN", default)
VERIFIED_ROLE_ID = int(os.getenv("VERIFIED_ROLE_ID", 0))

if DISCORD_BOT_TOKEN == default:
    raise RuntimeError(
        "Bot token not found. Please set DISCORD_BOT_TOKEN in your .env file."
    )

if VERIFICATION_CHANNEL_ID == default:
    raise RuntimeError(
        "Verification channel ID not found. Please set VERIFICATION_CHANNEL_ID in your .env file."
    )

if SENDER_EMAIL == default:
    raise RuntimeError(
        "Sender email not found. Please set SENDER_EMAIL in your .env file."
    )

if SENDER_EMAIL_PASSWORD == default:
    raise RuntimeError(
        "Sender email password not found. Please set SENDER_EMAIL_PASSWORD in your .env file."
    )

if EMAIL_DOMAIN == default:
    raise RuntimeError(
        "Email domain not found. Please set EMAIL_DOMAIN in your .env file."
    )

if VERIFIED_ROLE_ID == 0:
    raise RuntimeError(
        "Verified role id not found. Please set VERIFIED_ROLE_ID in your .env file."
    )

try:
    VERIFICATION_CHANNEL_ID = int(VERIFICATION_CHANNEL_ID)
except ValueError:
    raise ValueError("VERIFICATION_CHANNEL_ID must be a valid integer.")
