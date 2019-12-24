import time
import json
import base64

from utils.blockchain import sign, verify, get_account


def _base64urlencode(value):
    encoded = base64.b64encode(str(value).encode('utf8')).decode("utf-8")
    return encoded.split("=")[0].replace("+", "-").replace("/", "_")


def _base64urldecode(value):
    decoded = value.replace("-", "+").replace("_", "/")
    decoded += "==" if len(decoded) % 4 == 2 else ""
    decoded += "=" if len(decoded) % 4 == 3 else ""
    return base64.b64decode(decoded).decode("utf-8").replace("'", '"')


def ewt_sign(password, payload):
    """EWT sign method"""
    wallet = payload["iss"]
    header = _base64urlencode(str({"typ": "EWT"}))
    payload = _base64urlencode(str(payload))

    signature = sign(get_account(wallet, password), payload)

    return ".".join([header, payload, signature])


def ewt_validate(args, payload, sig):
    """EWT verify method"""
    try:
        decoded = json.loads(_base64urldecode(payload))
        if not verify(decoded["iss"], payload, sig):
            return False

        if decoded["exp"] < int(time.time()):
            return False

        for element in args:
            if element == "Authorization" or not args[element]:
                continue

            if args[element] != decoded[element]:
                try:
                    if str(args[element].lower()) != str(decoded[element]):
                        return False
                except AttributeError:
                    return False
    except (KeyError, json.decoder.JSONDecodeError):
        return False
    return True
