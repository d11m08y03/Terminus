import discord
from bot.config import VERIFICATION_CHANNEL_ID, VERIFIED_ROLE_ID
from bot.database import (
    is_id_pending,
    is_id_verified,
)
from bot.verify import validate_verification_code, verify_email
from bot.logging import log_info, log_warning, log_error, log_exception


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

        log_info(f"User {user_id} submitted email for verification: {email}")

        try:
            message, is_error = await verify_email(user_id, email)

            if is_error:
                log_error(
                    f"Email verification failed for {user_id} with email {email}: {message}"
                )
                await interaction.followup.send(message, ephemeral=True)
            else:
                log_info(
                    f"Verification code sent successfully to {user_id} with email {email}"
                )
                await interaction.followup.send(
                    "Verification code sent successfully! Check your email.",
                    ephemeral=True,
                )
        except Exception as e:
            log_exception(f"Error while verifying email for user {user_id}: {e}")
            await interaction.followup.send(
                "An error occurred while processing your request.", ephemeral=True
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

        user_id = interaction.user.id
        verification_code = self.verification_code.value

        log_info(f"User {user_id} submitted verification code: {verification_code}")

        try:
            message, is_error = validate_verification_code(user_id, verification_code)

            if is_error:
                log_error(f"Verification failed for user {user_id}: {message}")
                await interaction.followup.send(message, ephemeral=True)
            else:
                role = interaction.guild.get_role(VERIFIED_ROLE_ID)  # type: ignore

                if role is None:
                    log_warning(
                        f"Role with ID {VERIFIED_ROLE_ID} not found for user {user_id}"
                    )
                    await interaction.followup.send(
                        "Email verified. Welcome!", ephemeral=True
                    )
                    return

                await interaction.user.add_roles(role)  # type: ignore
                log_info(f"Added verified role to user {user_id}")
                await interaction.followup.send(
                    "Email verified. Welcome!", ephemeral=True
                )
        except Exception as e:
            log_exception(f"Error while verifying code for user {user_id}: {e}")
            await interaction.followup.send(
                "An error occurred while processing your request.", ephemeral=True
            )


class View(discord.ui.View):
    def __init__(self):
        super()__init__(timeout=None)

    @discord.ui.button(label="Verify University Email", style=discord.ButtonStyle.green)
    async def callback(self, interaction: discord.Interaction, button):
        user_id = interaction.user.id

        log_info(f"User {user_id} clicked on verify button.")

        try:
            if is_id_pending(user_id):
                log_info(f"User {user_id} has a pending verification.")
                modal = VerificationCodeInputModal()
            elif is_id_verified(user_id):
                log_info(f"User {user_id} is already verified.")
                await interaction.response.send_message(
                    "Email is already verified", ephemeral=True
                )
                return
            else:
                log_info(f"User {user_id} needs to input email for verification.")
                modal = EmailInputModal()

            await interaction.response.send_modal(modal)

        except Exception as e:
            log_exception(f"Error during verification process for user {user_id}: {e}")
            await interaction.response.send_message(
                "An error occurred while processing your request.", ephemeral=True
            )


class Client(discord.Client):
    async def on_ready(self):
        log_info(f"Logged in as {self.user}")

        try:
            verification_channel = self.get_channel(VERIFICATION_CHANNEL_ID)  # type: ignore

            if verification_channel is None:
                log_error(
                    f"Verification channel with ID {VERIFICATION_CHANNEL_ID} not found."
                )
                raise RuntimeError("Verification channel not found.")

            if not isinstance(verification_channel, discord.TextChannel):
                log_error(
                    f"Verification channel with ID {VERIFICATION_CHANNEL_ID} is not a text channel."
                )
                raise RuntimeError("Verification channel is not a text channel.")

            await verification_channel.purge(check=lambda m: m.author == self.user)
            log_info("Purged previous verification messages.")

            verification_message = "Click to verify your university email."
            await verification_channel.send(content=verification_message, view=View())
            log_info("Verification message sent to channel.")

        except Exception as e:
            log_exception(f"Error during bot startup: {e}")
