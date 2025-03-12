import os
import discord
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
        "Verification channel id not found. Please set DISCORD_BOT_TOKEN in your .env file."
    )

try:
    CHANNEL_ID = int(VERIFICATION_CHANNEL_ID)
except ValueError:
    raise ValueError("VERIFICATION_CHANNEL_ID must be a valid integer.")


class View(discord.ui.View):
    @discord.ui.button(label="Click Me", style=discord.ButtonStyle.red)
    async def callback(self, button, interaction):
        await button.response.send_message("Hello")


class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

        verification_channel = self.get_channel(CHANNEL_ID)

        if verification_channel is None:
            raise RuntimeError("Verification channel not found")

        if not isinstance(verification_channel, discord.TextChannel):
            raise RuntimeError("Verification channel is not a text channel")

        await verification_channel.purge(check=lambda m: m.author == self.user)

        await verification_channel.send(content="Click to verify umail.", view=View())


intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)

client.run(DISCORD_BOT_TOKEN)
