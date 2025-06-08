import discord
from bot.config import DISCORD_BOT_TOKEN
from bot.client import Client
from bot.database import init_db
from bot.logging import log_info

init_db()

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)

log_info("Bot starting...")

client.run(DISCORD_BOT_TOKEN)
