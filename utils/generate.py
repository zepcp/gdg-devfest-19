import random, string


def random_id(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits,
                                  k=length))
