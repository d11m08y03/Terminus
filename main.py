import discord
from bot.config import DISCORD_BOT_TOKEN
from bot.client import Client

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)

client.run(DISCORD_BOT_TOKEN)
