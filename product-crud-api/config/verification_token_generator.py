import secrets

def generate_verification_token():
    return str(
        secrets.randbelow(900000) + 100000
    )