import pyotp


def get_current_totp(value):
    totp = pyotp.TOTP(value)
    current_totp = totp.now()
    return current_totp