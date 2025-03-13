# Terminus

This is a Discord bot that verifies email addresses by sending a verification code and managing user roles based on their email verification status.

### Features

- Users can enter their university email address.
- The bot sends a verification code to the entered email.
- Users submit the verification code to verify their email.
- Verified users are assigned a "Verified" role in the Discord server.
- Logs errors and activities to a file for debugging.

## Requirements

Before setting up the bot, ensure you have the following:

- Python 3.9 or later
- Discord Developer Account and bot token
- SQLite for the database
- Email server credentials for sending verification emails

## Install Dependencies

Install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

## Setup Environment Variables

Create a `.env` file in the project root directory with the following variables:

```txt
DISCORD_BOT_TOKEN=your-discord-bot-token
VERIFICATION_CHANNEL_ID=your-verification-channel-id
VERIFIED_ROLE_ID=your-verified-role-id
SENDER_EMAIL=your-email@example.com
SENDER_EMAIL_PASSWORD=your-email-password
EMAIL_DOMAIN=your-email-domain
```

Replace the placeholders with actual values:

- `DISCORD_BOT_TOKEN`: Your bot token from the Discord Developer Portal.
- `VERIFICATION_CHANNEL_ID`: The ID of the channel where users can verify their emails.
- `VERIFIED_ROLE_ID`: The ID of the "Verified" role that users will be assigned after successful verification.
- `SENDER_EMAIL`: Your email address used to send verification emails.
- `SENDER_EMAIL_PASSWORD`: Your app password.
- `EMAIL_DOMAIN`: The domain of your email provider (e.g., `@gmail.com`).

## Troubleshooting

If you run into any issues, check the following common problems and solutions:

#### 1. **Bot Doesn't Start**

- Ensure that all environment variables are properly set in the `.env` file.
- If you're unsure, check the terminal for error messages when running `python bot.py`.

#### 2. **Email Not Sent**

- Double-check the email server credentials in the `.env` file.
- If you're using Gmail:
  - Enable "Less secure apps" or use an app password if two-factor authentication (2FA) is enabled.

#### 3. **Bot Not Assigning Roles**

- Ensure that the `VERIFIED_ROLE_ID` is set correctly in the `.env` file.
- Verify that the bot has the correct permissions in the Discord server to assign roles.

#### 4. Still Having Trouble?

If you’ve tried the above solutions and the problem persists, please open an issue.
