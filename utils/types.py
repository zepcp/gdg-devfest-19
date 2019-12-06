import datetime


def int_to_hex(value):
    return hex(value)


def hex_to_int(value):
    return int(value, 16)


def string_to_bytes(value):
    return value.encode("utf-8")


def bytes_to_string(value):
    return value.decode("utf-8")


def hex_to_bytes(value):
    return bytes.fromhex(value)


def bytes_to_hex(value):
    return value.hex()


def string_to_hex(value):
    return bytes_to_hex(string_to_bytes(value))


def hex_to_string(value):
    return bytes_to_string(hex_to_bytes(value))


def int_to_bytes(value):
    return value.to_bytes(32, byteorder='big')


def bytes_to_int(value):
    return hex_to_int("0x"+bytes_to_hex(value))


def unixtimestamp_to_datetime(value):
    return datetime.datetime.utcfromtimestamp(value)


def datetime_to_unixtimestamp(value):
    return int(value.timestamp())


def string_to_datetime(value, _format):
    return datetime.datetime.strptime(value, _format)


def datetime_to_string(value, _format):
    return value.strftime(_format)


def string_to_unixtimestamp(value, _format):
    return int(datetime_to_unixtimestamp(string_to_datetime(value, _format)))


def unixtimestamp_to_string(value, _format):
    return datetime_to_string(unixtimestamp_to_datetime(value), _format)
