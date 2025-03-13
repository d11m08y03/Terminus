import os
from dotenv import load_dotenv

load_dotenv()

default = "Uninitialised"


def get_env_variable(var_name, default_value=default, cast_type=None):
    value = os.getenv(var_name, default_value)
    if value == default_value:
        raise RuntimeError(
            f"{var_name} not found. Please set {var_name} in your .env file."
        )

    if cast_type:
        try:
            return cast_type(value)
        except ValueError:
            raise ValueError(f"{var_name} must be a valid {cast_type.__name__}.")

    return value


DISCORD_BOT_TOKEN = get_env_variable("DISCORD_BOT_TOKEN", cast_type=str)
VERIFICATION_CHANNEL_ID = get_env_variable("VERIFICATION_CHANNEL_ID", cast_type=int)
SENDER_EMAIL = get_env_variable("SENDER_EMAIL", cast_type=str)
SENDER_EMAIL_PASSWORD = get_env_variable("SENDER_EMAIL_PASSWORD", cast_type=str)
EMAIL_DOMAIN = get_env_variable("EMAIL_DOMAIN", cast_type=str)
VERIFIED_ROLE_ID = get_env_variable("VERIFIED_ROLE_ID", cast_type=int)
