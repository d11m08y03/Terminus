import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
VERIFICATION_CHANNEL_ID = os.getenv("VERIFICATION_CHANNEL_ID")

if DISCORD_BOT_TOKEN is None:
    raise ValueError(
        "Bot token not found. Please set DISCORD_BOT_TOKEN in your .env file."
    )

if VERIFICATION_CHANNEL_ID is None:
    raise ValueError(
        "Verification channel ID not found. Please set VERIFICATION_CHANNEL_ID in your .env file."
    )

try:
    VERIFICATION_CHANNEL_ID = int(VERIFICATION_CHANNEL_ID)
except ValueError:
    raise ValueError("VERIFICATION_CHANNEL_ID must be a valid integer.")
