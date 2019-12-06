import qrcode


def make(info, border=1):
    return qrcode.make(info, border=border)


def save(code, file):
    return code.save(file)
