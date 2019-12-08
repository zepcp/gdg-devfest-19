import re


def is_email(my_email):
    return re.fullmatch(r"[a-zA-Z0-9_.+-]{1,64}"
                        r"@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
                        my_email) is not None and len(my_email) <= 320


def is_wallet(my_wallet):
    return re.fullmatch(r"0x[0-9a-f]{40}", my_wallet.lower()) is not None


def email(value):
    if is_email(value):
        username, domain = value.split("@")
        return "@".join([username, domain.lower()])
    else:
        raise ValueError("Not an email address")


def wallet(value):
    if is_wallet(value):
        return value.lower()
    else:
        raise ValueError("Not a valid wallet address")
