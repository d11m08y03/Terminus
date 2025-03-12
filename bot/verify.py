def verify_email(email: str) -> bool:
    if "university.edu" in email:
        return True
    return False
