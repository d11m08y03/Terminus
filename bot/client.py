import discord
from bot.config import VERIFICATION_CHANNEL_ID, VERIFIED_ROLE_ID
from bot.database import (
    is_id_pending,
    is_id_verified,
)
from bot.verify import validate_verification_code, verify_email


class EmailInputModal(discord.ui.Modal, title="Verify University Email"):
    def __init__(self):
        super().__init__()

        self.email = discord.ui.TextInput(
            label="Enter your umail:",
            placeholder="example@umail.uom.ac.mu",
            style=discord.TextStyle.short,
            required=True,
            max_length=50,
        )

        self.add_item(self.email)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

        user_id = interaction.user.id
        email = self.email.value

        message, is_error = await verify_email(user_id, email)

        if is_error:
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.followup.send(
                "Verification code sent successfully! Check your email.", ephemeral=True
            )


class VerificationCodeInputModal(discord.ui.Modal, title="Verify University Email"):
    def __init__(self):
        super().__init__()

        self.verification_code = discord.ui.TextInput(
            label="Enter your verification code",
            placeholder="000000",
            style=discord.TextStyle.short,
            required=True,
            max_length=6,
        )

        self.add_item(self.verification_code)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

        verification_code = self.verification_code.value

        message, is_error = validate_verification_code(
            interaction.user.id, verification_code
        )

        if is_error:
            await interaction.followup.send(message, ephemeral=True)
        else:
            role = interaction.guild.get_role(VERIFIED_ROLE_ID)  # type: ignore

            if role is None:
                await interaction.followup.send(
                    "Email verified. Welcome!", ephemeral=True
                )
                return

            await interaction.user.add_roles(role)  # type: ignore
            await interaction.followup.send("Email verified. Welcome!", ephemeral=True)


class View(discord.ui.View):
    @discord.ui.button(label="Verify University Email", style=discord.ButtonStyle.green)
    async def callback(self, interaction: discord.Interaction, button):
        user_id = interaction.user.id

        if is_id_pending(user_id):
            modal = VerificationCodeInputModal()
        elif is_id_verified(user_id):
            await interaction.response.send_message(
                "Email is already verified", ephemeral=True
            )
            return
        else:
            modal = EmailInputModal()

        await interaction.response.send_modal(modal)


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
