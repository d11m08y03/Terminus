import discord
from bot.config import VERIFICATION_CHANNEL_ID
from bot.verify import verify_email


class View(discord.ui.View):
    @discord.ui.button(label="Verify University Email", style=discord.ButtonStyle.green)
    async def callback(self, button, interaction):
        await button.response.send_message(
            "Your university email has been successfully verified! 🎉",
            ephemeral=True,
        )


class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

        verification_channel = self.get_channel(VERIFICATION_CHANNEL_ID)

        if verification_channel is None:
            raise RuntimeError("Verification channel not found.")

        if not isinstance(verification_channel, discord.TextChannel):
            raise RuntimeError("Verification channel is not a text channel.")

        await verification_channel.purge(check=lambda m: m.author == self.user)

        verification_message = "Click to verify your university email."
        await verification_channel.send(content=verification_message, view=View())
        print("Verification message sent to channel.")
