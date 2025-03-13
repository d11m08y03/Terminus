import random
import asyncio
import string
from typing import Tuple

from bot.config import EMAIL_DOMAIN
from bot.database import (
    add_pending_verification,
    add_verified_email,
    delete_pending_verification,
    get_email_by_id,
    is_email_pending,
    is_email_verified,
    verify_code,
)
from bot.email import send_email


def generate_verification_code(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


async def verify_email(user_id: int, email: str) -> Tuple[str, bool]:
    if not email.endswith(EMAIL_DOMAIN):
        return "Invalid email", True

    if is_email_verified(email):
        return "Email already verified", True

    if is_email_pending(email):
        return "Verification code already sent", True

    verification_code = generate_verification_code()

    try:
        await asyncio.to_thread(send_email, email, verification_code)
    except Exception as e:
        return f"Failed to store verification in database: {e}", True

    try:
        await asyncio.to_thread(
            add_pending_verification, user_id, email, verification_code
        )
    except Exception as e:
        return f"Failed to store verification in database: {e}", True

    return "", False


def validate_verification_code(
    user_id: int, verification_code: str
) -> Tuple[str, bool]:
    if not verify_code:
        return "Verification code is invalid", True

    email = get_email_by_id(user_id)

    if email is None:
        return "Internal server error", True

    if not verify_code(user_id, verification_code):
        return "Invalid verification code", True

    delete_pending_verification(user_id)
    add_verified_email(user_id, email)

    return "", False
