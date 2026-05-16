import secrets

def generate_verification_token():
    return secrets.token_hex(32) 